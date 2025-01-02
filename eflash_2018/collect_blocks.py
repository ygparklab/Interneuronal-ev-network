import h5py
import multiprocessing
import numpy as np
import os
from eflash_2018.utils.shared_memory import SharedMemory
import tifffile
import json
import argparse
import glob
import tqdm
from .utils import RollingBuffer

try:
    import mkl
    mkl.set_num_threads(1)
except:
    pass
               
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source",
                        required=True,
                        help="The glob expression for the stack")
    parser.add_argument("--points",
                        required=True,
                        help="A .json file containing the points in xyz order")
    parser.add_argument("--patch-size",
                        type=int,
                        default=31,
                        help="Size of a patch in pixels (an odd # please)")
    #patch size for this script should be constrained to 31
    parser.add_argument("--output",
                        required=True,
                        help="The location for an HDF file file containing "
                        "an NxMxM array where N is the number of points and "
                        "M is the patch size and 3 arrays containing the X,"
                             "Y and Z coordinates of each of N points.")
    parser.add_argument("--n-cores",
                        default=12,
                        type=int,
                        help="The number of cores to use")
    parser.add_argument("--n-io-cores",
                        default=12,
                        type=int,
                        help="The number of cores to use during I/O")
    return parser.parse_args()

def do_z(pz, offset, 
         patches_xy1, patches_xy2, patches_xy3, patches_xy4,
         patches_xy5, patches_xy6, patches_xy7, patches_xy8,
         patches_xy9, patches_xy10, patches_xy11, patches_xy12,
         patches_xy13, patches_xy14, patches_xy15, patches_xy16,
         patches_xy17, patches_xy18, patches_xy19, patches_xy20,
         patches_xy21, patches_xy22, patches_xy23, patches_xy24,
         patches_xy25, patches_xy26, patches_xy27, patches_xy28,
         patches_xy29, patches_xy30, patches_xy31,
         rb, z, half_patch_size):
    for x, y in pz[:, :-1]: #all the rows and columns except for the last column
        x, y = int(x), int(y)
        with patches_xy1.txn() as m:
            m[offset] = rb[
                z - half_patch_size,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy2.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 1,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy3.txn() as m:
            m[offset] = rb[
                z + half_patch_size + 2,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy4.txn() as m:
            m[offset] = rb[
                z + half_patch_size + 3,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy5.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 4,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy6.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 5,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy7.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 6,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy8.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 7,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy9.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 8,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy10.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 9,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy11.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 10,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy12.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 11,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy13.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 12,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy14.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 13,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy15.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 14,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy16.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 15,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy17.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 16,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy18.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 17,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy19.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 18,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy20.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 19,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy21.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 20,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy22.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 21,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy23.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 22,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy24.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 23,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy25.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 24,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy26.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 25,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy27.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 26,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy28.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 27,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy29.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 28,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy30.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 29,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        with patches_xy31.txn() as m:
            m[offset] = rb[
                z - half_patch_size + 30,
                y - half_patch_size: y + half_patch_size + 1,
                x - half_patch_size: x + half_patch_size + 1]
        offset += 1
    return offset


def main():
    args = parse_args()
    source_files = sorted(glob.glob(args.source))
    rb = RollingBuffer(source_files, args.n_io_cores)
    points = np.array(json.load(open(args.points)))
    patch_size = args.patch_size
    half_patch_size = patch_size // 2
    patches_xy1, patches_xy2, patches_xy3, patches_xy4, patches_xy5, patches_xy6, patches_xy7, patches_xy8, patches_xy9, patches_xy10, patches_xy11, patches_xy12, patches_xy13, patches_xy14, patches_xy15, patches_xy16, patches_xy17, patches_xy18, patches_xy19, patches_xy20, patches_xy21, patches_xy22, patches_xy23, patches_xy24, patches_xy25, patches_xy26, patches_xy27, patches_xy28, patches_xy29, patches_xy30, patches_xy31 = \
        [SharedMemory((len(points), patch_size, patch_size), rb.dtype)
        for _ in range(31)]
    points_out = []
    offset = 0
    x1 = rb.shape[2] - half_patch_size
    y1 = rb.shape[1] - half_patch_size
    with multiprocessing.Pool(args.n_cores) as pool:
        it = tqdm.tqdm(
                range(half_patch_size, len(source_files) - half_patch_size))
        for z in it:
            it.set_description("Releasing @ %d" % (z - half_patch_size))
            rb.release(z - half_patch_size)
            it.set_description("Waiting for %d" % (z + half_patch_size))
            rb.wait(z + half_patch_size)
            pz = points[(points[:, 2] >= z) & (points[:, 2] < z+1)]
            if len(pz) == 0:
                continue
            mask = np.all(pz[:, 0:2] >= half_patch_size, 1) &\
                   (pz[:, 0] < x1) &\
                   (pz[:, 1] < y1)
            pz = pz[mask]
            if len(pz) == 0:
                continue
            points_out.append(pz)
            if len(pz) < args.n_cores * 10 or args.n_cores == 1:
                offset = do_z(pz, offset,
                              patches_xy1, patches_xy2, patches_xy3, patches_xy4,
                              patches_xy5, patches_xy6, patches_xy7, patches_xy8,
                              patches_xy9, patches_xy10, patches_xy11,patches_xy12,
                              patches_xy13, patches_xy14, patches_xy15,
                              patches_xy16, patches_xy17, patches_xy18,
                              patches_xy19, patches_xy20, patches_xy21,
                              patches_xy22, patches_xy23, patches_xy24,
                              patches_xy25, patches_xy26, patches_xy27,
                              patches_xy28, patches_xy29, patches_xy30,
                              patches_xy31,
                              rb, z, half_patch_size)
            else:
                idxs = np.linspace(0, len(pz), args.n_cores+1).astype(int)
                it.set_description("Freezing buffer")
                frb = rb.freeze()
                fnargs = [(pz[i0:i1], offset + i0,
                           patches_xy1, patches_xy2, patches_xy3, patches_xy4,
                           patches_xy5, patches_xy6, patches_xy7, patches_xy8,
                           patches_xy9, patches_xy10, patches_xy11,patches_xy12,
                           patches_xy13, patches_xy14, patches_xy15,
                           patches_xy16, patches_xy17, patches_xy18,
                           patches_xy19, patches_xy20, patches_xy21,
                           patches_xy22, patches_xy23, patches_xy24,
                           patches_xy25, patches_xy26, patches_xy27,
                           patches_xy28, patches_xy29, patches_xy30,
                           patches_xy31,
                           frb, z, half_patch_size)
                   for i0, i1 in zip(idxs[:-1], idxs[1:])]
                it.set_description("Processing %d patches @ %d" % (len(pz), z))
                pool.starmap(do_z, fnargs)
                offset += len(pz)

    points_out = np.vstack(points_out)
    with h5py.File(args.output, "w") as f:
        with patches_xy1.txn() as m:
            old_patches = f.create_dataset("patches_xy1", data=m[:offset])
        with patches_xy2.txn() as m:
            f.create_dataset("patches_xy2", data=m[:offset])
        with patches_xy3.txn() as m:
            f.create_dataset("patches_xy3", data=m[:offset])
        with patches_xy4.txn() as m:
            f.create_dataset("patches_xy4", data=m[:offset])
        with patches_xy5.txn() as m:
            f.create_dataset("patches_xy5", data=m[:offset])
        with patches_xy6.txn() as m:
            f.create_dataset("patches_xy6", data=m[:offset])
        with patches_xy7.txn() as m:
            f.create_dataset("patches_xy7", data=m[:offset])
        with patches_xy8.txn() as m:
            f.create_dataset("patches_xy8", data=m[:offset])
        with patches_xy9.txn() as m:
            f.create_dataset("patches_xy9", data=m[:offset])
        with patches_xy10.txn() as m:
            f.create_dataset("patches_xy10", data=m[:offset])
        with patches_xy11.txn() as m:
            f.create_dataset("patches_xy11", data=m[:offset])
        with patches_xy12.txn() as m:
            f.create_dataset("patches_xy12", data=m[:offset])
        with patches_xy13.txn() as m:
            f.create_dataset("patches_xy13", data=m[:offset])
        with patches_xy14.txn() as m:
            f.create_dataset("patches_xy14", data=m[:offset])
        with patches_xy15.txn() as m:
            f.create_dataset("patches_xy15", data=m[:offset])
        with patches_xy16.txn() as m:
            f.create_dataset("patches_xy16", data=m[:offset])
        with patches_xy17.txn() as m:
            f.create_dataset("patches_xy17", data=m[:offset])
        with patches_xy18.txn() as m:
            f.create_dataset("patches_xy18", data=m[:offset])
        with patches_xy19.txn() as m:
            f.create_dataset("patches_xy19", data=m[:offset])
        with patches_xy20.txn() as m:
            f.create_dataset("patches_xy20", data=m[:offset])
        with patches_xy21.txn() as m:
            f.create_dataset("patches_xy21", data=m[:offset])
        with patches_xy22.txn() as m:
            f.create_dataset("patches_xy22", data=m[:offset])
        with patches_xy23.txn() as m:
            f.create_dataset("patches_xy23", data=m[:offset])
        with patches_xy24.txn() as m:
            f.create_dataset("patches_xy24", data=m[:offset])
        with patches_xy25.txn() as m:
            f.create_dataset("patches_xy25", data=m[:offset])
        with patches_xy26.txn() as m:
            f.create_dataset("patches_xy26", data=m[:offset])
        with patches_xy27.txn() as m:
            f.create_dataset("patches_xy27", data=m[:offset])
        with patches_xy28.txn() as m:
            f.create_dataset("patches_xy28", data=m[:offset])
        with patches_xy29.txn() as m:
            f.create_dataset("patches_xy29", data=m[:offset])
        with patches_xy30.txn() as m:
            f.create_dataset("patches_xy30", data=m[:offset])
        with patches_xy31.txn() as m:
            f.create_dataset("patches_xy31", data=m[:offset])
        f.create_dataset("x", data=points_out[:, 0])
        f.create_dataset("y", data=points_out[:, 1])
        f.create_dataset("z", data=points_out[:, 2])
        f["patches"] = old_patches



if __name__ == "__main__":
    main()
