import argparse
import json
import logging
import typing

import neuroglancer
import numpy as np
import requests
from nuggt.utils.ngutils import *
from nuggt.point_annotator import PointAnnotator, to_um
import os
import pathlib
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port",
                        type=int,
                        help="HTTP port for neurglancer server",
                        default=0)
    parser.add_argument("--bind-address",
                        help="The IP address to bind to as a webserver. "
                        "The default is 127.0.0.1 which is constrained to "
                        "the local machine.",
                        default="127.0.0.1")
    parser.add_argument("--static-content-source",
                        default=None,
                        help="Obsolete, please don't use")
    return parser.parse_args()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, viewer):
        QtWidgets.QMainWindow.__init__(self)
        self.viewer = viewer
        self.point_annotator1 = PointAnnotator(viewer, name="points-1")
        self.x0 = None
        self.x1 = None
        self.y0 = None
        self.y1 = None
        self.z0 = None
        self.z1 = None
        self.points_file1 = None
        self.points_file2 = None
        self.points_time1 = None
        self.points_time2 = None
        self.all_points1 = np.zeros((0, 3), int)
        self.all_points2 = np.zeros((0, 3), int)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Neuroglancer display")
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.main_widget = QtWidgets.QWidget(self)
        l = QtWidgets.QVBoxLayout(self.main_widget)

        #
        # Points file UI
        #
        hls = []
        hl = QtWidgets.QHBoxLayout()
        hls.append(hl)
        hl.addWidget(QtWidgets.QLabel(text="Points file 1:"))
        self.points_file1_widget = QtWidgets.QLineEdit()
        self.points_file1_widget.setText("//media/share2/...")
        hl.addWidget(self.points_file1_widget)
        self.points_file1_browse_button = QtWidgets.QPushButton(text="Browse...")
        self.points_file1_browse_button.clicked.connect(
            self.on_points_file1_browse)
        hl.addWidget(self.points_file1_browse_button)
        self.points_file1_save_button = QtWidgets.QPushButton(text="Save...")
        self.points_file1_save_button.clicked.connect(
            self.on_points_file1_save
        )
        hl.addWidget(self.points_file1_save_button)
        #
        # Second points file UI
        #
        hl = QtWidgets.QHBoxLayout()
        hls.append(hl)
        hl.addWidget(QtWidgets.QLabel(text="Points file 2:"))
        self.points_file2_widget = QtWidgets.QLineEdit()
        self.points_file2_widget.setText("//media/share2/...")
        hl.addWidget(self.points_file2_widget)
        self.points_file2_browse_button = QtWidgets.QPushButton(text="Browse...")
        self.points_file2_browse_button.clicked.connect(
            self.on_points_file2_browse)
        hl.addWidget(self.points_file2_browse_button)
        self.points_file2_enable_widget = QtWidgets.QCheckBox(text="Enable")
        hl.addWidget(self.points_file2_enable_widget)

        #
        # X0, X1, Y0, Y1, Z0, Z1
        #
        self.coord_widgets = {}
        for xyz in "xyz":
            hl = QtWidgets.QHBoxLayout()
            hls.append(hl)
            for _01 in (0, 1):
                label = "%s%d" % (xyz, _01)
                hl.addWidget(QtWidgets.QLabel(text=label))
                self.coord_widgets[label] = QtWidgets.QLineEdit()
                self.coord_widgets[label].setText("0")
                hl.addWidget(self.coord_widgets[label])
        #
        # Neuroglancer data source
        #
        hl = QtWidgets.QHBoxLayout()
        hls.append(hl)
        hl.addWidget(QtWidgets.QLabel(text="Neuroglancer source:"))
        self.neuroglancer_source_widget = QtWidgets.QLineEdit()
        self.neuroglancer_source_widget.setText(
            "precomputed://https://leviathan-chunglab.mit.edu/precomputed/???")
        hl.addWidget(self.neuroglancer_source_widget)
        #
        # Shader config for first source
        #
        hl = QtWidgets.QHBoxLayout()
        hls.append(hl)
        hl.addWidget(QtWidgets.QLabel(text="Intensity: "))
        self.intensity_widget = QtWidgets.QLineEdit("40.0")
        hl.addWidget(self.intensity_widget)
        self.shader_widget = QtWidgets.QComboBox()
        hl.addWidget(self.shader_widget)
        self.shader_widget.addItems(["gray",
                                     "red",
                                     "green",
                                     "blue",
                                     "cubehelix"])
        self.shader_widget.setCurrentIndex(4)
        #
        # Second Neuroglancer source
        #
        hl = QtWidgets.QHBoxLayout()
        hls.append(hl)
        self.use_neuroglancer_second_source_widget = QtWidgets.QCheckBox(
            "Neuroglancer source #2")
        hl.addWidget(self.use_neuroglancer_second_source_widget)
        self.neuroglancer_second_source_widget = QtWidgets.QLineEdit()
        self.neuroglancer_second_source_widget.setText(
            "precomputed://https://leviathan-chunglab.mit.edu/precomputed/???")
        hl.addWidget(self.neuroglancer_second_source_widget)
        #
        # Shader for second source
        #
        hl = QtWidgets.QHBoxLayout()
        hls.append(hl)
        hl.addWidget(QtWidgets.QLabel(text="Intensity: "))
        self.second_intensity_widget = QtWidgets.QLineEdit("40.0")
        hl.addWidget(self.second_intensity_widget)
        self.second_shader_widget = QtWidgets.QComboBox()
        hl.addWidget(self.second_shader_widget)
        self.second_shader_widget.addItems([
            "gray",
            "red",
            "green",
            "blue",
            "cubehelix"])
        self.second_shader_widget.setCurrentIndex(2)

        #
        # Display button
        #
        hl = QtWidgets.QHBoxLayout()
        hls.append(hl)
        self.display_button_widget = QtWidgets.QPushButton(
            text="Update display")
        self.display_button_widget.clicked.connect(
            self.on_update_display)
        hl.addWidget(self.display_button_widget)
        for hl in hls:
            l.addLayout(hl)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def on_points_file1_browse(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open points file",
        filter="Coordinates (*.json);;All files (*)")
        self.points_file1_widget.setText(filename)

    def on_points_file2_browse(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open points file",
        filter="Coordinates (*.json);;All files (*)")
        self.points_file2_widget.setText(filename)

    def on_points_file1_save(self):
        if self.x0 is not None:
            self.replace_points()
        filename = self.points_file1_widget.text()

        if os.path.exists(filename):
            msg = QtWidgets.QMessageBox.question(
                self, "Overwriting file",
                "Are you sure you want to overwrite %s?" %
                os.path.split(filename)[1])
            if msg != QtWidgets.QMessageBox.Yes:
                return
        with open(filename, "w") as fd:
            json.dump(self.all_points1.tolist(), fd)
        self.points1_file = filename

    def on_update_display(self):
        try:
            url = self.neuroglancer_source_widget.text()
            if url.startswith("precomputed://"):
                precomputed_url = url[len("precomputed://"):]
                voxel_size = get_source_voxel_size(precomputed_url)
            else:
                voxel_size = default_voxel_size
            self.point_annotator1.voxel_size = voxel_size
        except:
            logging.info("Failed to read %s" % precomputed_url,
                         exc_info=True)
            QtWidgets.QMessageBox.critical(
                self, "I/O Error", "Failed to read %s" % precomputed_url)
            return

        try:
            x0 = int(self.coord_widgets["x0"].text())
            x1 = int(self.coord_widgets["x1"].text())
            y0 = int(self.coord_widgets["y0"].text())
            y1 = int(self.coord_widgets["y1"].text())
            z0 = int(self.coord_widgets["z0"].text())
            z1 = int(self.coord_widgets["z1"].text())
        except ValueError:
            QtWidgets.QMessageBox.critical(
                self, "Format error", "Coordinates must be integers")
            return
        points_file1 = self.points_file1_widget.text()
        try:
            points_time1 = pathlib.Path(points_file1).stat().st_mtime
        except:
            QtWidgets.QMessageBox.critical(
                self, "I/O Error",
                    "Could not open %s" % points_file1
            )
            return
        if points_file1 == self.points_file1 and\
                points_time1 <= self.points_time1:
            replace1 = True
        else:
            try:
                with open(points_file1, "r") as fd:
                    self.all_points1 = np.array(json.load(fd))
                self.points_file1 = points_file1
                self.points_time1 = points_time1
                replace1 = False
            except IOError:
                QtWidgets.QMessageBox.critical(
                    self,
                    "I/O Error",
                    "Could not open %s" % points_file1)
                return
            except json.JSONDecodeError:
                QtWidgets.QMessageBox.critical(
                    self,
                    "I/O Error",
                    "%s could not be read as a JSON file" % points_file1)
                return
            except UnicodeDecodeError:
                QtWidgets.QMessageBox.critical(
                    self,
                    "I/O Error",
                    "%s could not be read as a JSON file" % points_file1)
                return
        display_points2 = self.points_file2_enable_widget.isChecked()
        if display_points2:
            points_file2 = self.points_file2_widget.text()
            points_time2 = pathlib.Path(points_file2).stat().st_mtime
            if points_file2 != self.points_file2 or\
                    points_time2 > self.points_time2:
                try:
                    with open(points_file2, "r") as fd:
                        self.all_points2 = np.array(json.load(fd))
                    self.points_file2 = points_file2
                    self.points_time2 = points_time2
                except IOError:
                    QtWidgets.QMessageBox.critical(
                        self,
                        "I/O Error",
                        "Could not open %s" % points_file2)
                    return
                except json.JSONDecodeError:
                    QtWidgets.QMessageBox.critical(
                        self,
                        "I/O Error",
                        "%s could not be read as a JSON file" % points_file2)
                    return
                except UnicodeDecodeError:
                    QtWidgets.QMessageBox.critical(
                        self,
                        "I/O Error",
                        "%s could not be read as a JSON file" % points_file2)
                    return

        try:
            x02 = int(self.coord_widgets["x0"].text())
            x12 = int(self.coord_widgets["x1"].text())
            y02 = int(self.coord_widgets["y0"].text())
            y12 = int(self.coord_widgets["y1"].text())
            z02 = int(self.coord_widgets["z0"].text())
            z12 = int(self.coord_widgets["z1"].text())
        except ValueError:
            QtWidgets.QErrorMessage("Coordinates must be integers")
            return
        with self.viewer.txn() as txn:
            self.update_image(txn)
            self.update_points(txn, x0, x1, y0, y1, z0, z1, replace=replace1)
            self.x0, self.x1 = x0, x1
            self.y0, self.y1 = y0, y1
            self.z0, self.z1 = z0, z1
            low = np.array([[x02, y02, z02]])
            high = np.array([[x12, y12, z12]])
            idxs = np.where(np.all(self.all_points2 >= low, 1) &
                            np.all(self.all_points2 < high, 1))[0]
            xp, yp, zp = [self.all_points2[idxs, i] for i in range(3)]
            pointlayer(
                txn, "points-2", zp, yp, xp, color="red", voxel_size=voxel_size)
            txn.layers["points-2"].visible = display_points2

    def update_image(self, txn):
        shader_txt = self.shader_widget.currentText()
        if shader_txt == "gray":
            shader = gray_shader
        elif shader_txt == "red":
            shader = red_shader
        elif shader_txt == "green":
            shader = green_shader
        elif shader_txt == "blue":
            shader = blue_shader
        else:
            shader = cubehelix_shader
        try:
            intensity = float(self.intensity_widget.text())
        except ValueError:
            QtWidgets.QMessageBox.critical(
                self,
                "Format Error",
                "Intensity must be a number")
            return
        layer(txn, "image",
              self.neuroglancer_source_widget.text(),
              shader = shader,
              multiplier=intensity)
        if self.use_neuroglancer_second_source_widget.isChecked():
            shader_txt = self.second_shader_widget.currentText()
            if shader_txt == "gray":
                shader = gray_shader
            elif shader_txt == "red":
                shader = red_shader
            elif shader_txt == "green":
                shader = green_shader
            elif shader_txt == "blue":
                shader = blue_shader
            else:
                shader = cubehelix_shader
            try:
                intensity = float(self.second_intensity_widget.text())
            except ValueError:
                QtWidgets.QErrorMessage("Intensity must be a number")
                return
            layer(txn,
                  "image-2",
                  self.neuroglancer_second_source_widget.text(),
                  shader=shader,
                  multiplier=intensity)
        else:
            for i, l in enumerate(txn.layers):
                if l.name == "image-2":
                    del txn.layers[i]
                    break

    def update_points(self, txn,
                      x0, x1, y0, y1, z0, z1, replace):
        all_points = self.all_points1
        point_annotator = self.point_annotator1
        if replace:
            all_points = self.replace_points(all_points, point_annotator)
            self.all_points1 = all_points

        idxs = np.where(
            (all_points[:, 0] >= x0) & (all_points[:, 0] < x1) &
            (all_points[:, 1] >= y0) & (all_points[:, 1] < y1) &
            (all_points[:, 2] >= z0) & (all_points[:, 2] < z1))[0]
        if len(idxs) == 0:
            point_annotator.set_points(np.zeros((0, 3)), txn)
        else:
            point_annotator.set_points(all_points[idxs], txn)

    def replace_points(self, all_points, point_annotator):
        idxs = np.where(
            (all_points[:, 0] >= self.x0) &
            (all_points[:, 0] < self.x1) &
            (all_points[:, 1] >= self.y0) &
            (all_points[:, 1] < self.y1) &
            (all_points[:, 2] >= self.z0) &
            (all_points[:, 2] < self.z1))[0]
        return np.vstack((
            np.delete(all_points, idxs, 0),
            point_annotator.all_points
        ))


def main():
    app = QtWidgets.QApplication(sys.argv)
    args = parse_args()
    if args.static_content_source is not None:
        print("Please do not use --static-content-source."
              " It's no longer necessary and is disabled.",
              file=sys.stderr)
    neuroglancer.set_server_bind_address(
    args.bind_address, bind_port=args.port)
    viewer = neuroglancer.Viewer()
    print("Neuroglancer URL: %s" % str(viewer))
    window = ApplicationWindow(viewer)
    window.show()
    sys.exit(app.exec())


if __name__=="__main__":
    main()
