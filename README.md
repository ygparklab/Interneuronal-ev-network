# Interneuronal-ev-network

Official code repository for NBML's **"A brain-wide interneuronal network mediated by extracellular vesicle"** paper.  
This repository also contains software developed for the Chung Lab's **EFlash** paper.

## Analysis Pipeline

1. Find putative positive cells using `detect-blobs`.
2. Check whether the threshold is optimal using Fiji.
3. Make a list of patches for training using `collect-patches`.
4. Generate manually labeled ground truth data for a model using `eflash-train` (optional, as a pre-trained model is provided).
5. Classify the patches with the pre-trained model using `cell_classification_new.py` (built by PyTorch).
6. Get a brain alignment file using Neuroglancer (`Image_align_auto1.sh`, `Image_align_auto2.sh`).
7. Perform co-positivity analysis using Jupyter Notebook (if needed).
8. Count cells for each region using `count_cell_new.sh`.
9. Post-process results using `makeCSV` and `sort_colormap.ipynb`.

---

## detect-blobs

`detect-blobs` is a simple blob detector. It identifies peaks in the local maximum using a difference of Gaussians followed by a static threshold.

### Usage

```bash
detect-blobs \
    --source <source-expr> \
    --output <coords-file> \
    [--dog-low <dog-low-sigma>] \
    [--dog-low-xy <dog-low-sigma-xy>] \
    [--dog-low-z <dog-low-sigma-z>] \
    [--dog-high <dog-high-sigma>] \
    [--dog-high-xy <dog-high-sigma-xy>] \
    [--dog-high-z <dog-high-sigma-z>] \
    [--threshold <threshold>] \
    [--min-distance <min-distance>] \
    [--min-distance-xy <min-distance-xy>] \
    [--min-distance-z <min-distance-z>] \
    [--block-size-xy <block-size-xy>] \
    [--block-size-z <block-size-z>] \
    [--padding-xy <padding-xy>] \
    [--padding-z <padding-z>]

Parameters
source-expr: GLOB expression for collecting .tiff files (e.g., /path/*.tiff).
output: JSON file with X, Y, Z coordinates of detected cells.
dog-low-sigma: Standard deviation for foreground Gaussian smoothing.
dog-high-sigma: Standard deviation for background Gaussian smoothing.
threshold: Absolute cutoff for peak detection.
min-distance: Minimum distance in voxels between adjacent peaks.
block-size-xy: Block size in X and Y directions for processing.
block-size-z: Block size in Z direction for processing.
padding-xy: Padding for X and Y directions.
padding-z: Padding for Z direction.


collect-patches
collect-patches extracts rectangular 2D patches around detected centers using coordinates provided by detect-blobs.

### Usage
```bash
Copy code
collect-patches \
    --source <source-expr> \
    --points <points> \
    --output <output> \
    [--patch-size <patch-size>] \
    [--n-cores <n-cores>]
Parameters
source-expr: GLOB expression for .tiff files.
points: Input file from detect-blobs.
output: HDF5 file containing patches and their coordinates.
patch-size: Size of each patch (recommended odd number).
n-cores: Number of parallel processes.
eflash-train
eflash-train allows interactive training of a classifier using patches created by collect-patches. It uses dimensionality reduction and a random forest classifier.

Usage
bash
Copy code
eflash-train \
    --patch-file <patch-file> \
    --output <output> \
    [--neuroglancer <image-source>] \
    [--port <port>] \
    [--bind-address <bind-address>] \
    [--static-content-source <static-content-source>]
Parameters
patch-file: Input file from collect-patches.
output: File to save the trained model.
neuroglancer: Optional Neuroglancer data source (e.g., precomputed://http://localhost:81).
port: Port number for the Neuroglancer view.
bind-address: IP address to bind Neuroglancer's listening port.
static-content-source: URL for Neuroglancer's assets.
GUI Commands
File Menu
Save (Ctrl+S): Save the model and ground truth.
Write: Export positive coordinates to JSON.
Train: Train the model.
Quit: Exit the program.
Image Menu
Next (X): Show an unclassified patch.
Next Positive (Ctrl+P): Show a patch predicted as positive.
Next Negative (Ctrl+N): Show a patch predicted as negative.
Next Unsure (U): Show a patch with low prediction confidence.
Mark Menu
Positive: Mark the patch as positive.
Negative: Mark the patch as negative.
Training Workflow
Classify ~10-20 cells using Image → Next and mark as Positive or Negative.
Train the model using File → Train.
Classify unsure patches using Image → Next Unsure.
Repeat until sufficient accuracy is achieved.
