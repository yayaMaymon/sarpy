#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Sarpy imports ---
from sarpy.io.complex.converter import open_complex    # open SICD input
from sarpy.io.product.converter import open_product    # open the resulting SIDD
from sarpy.processing.ortho_rectify import NearestNeighborMethod
from sarpy.processing.sidd.sidd_product_creation import (
    create_detected_image_sidd,
    create_csi_sidd,
    create_dynamic_image_sidd
)

##############################################################################
# 1) Set paths/files
##############################################################################

infile = "/Users/user/Downloads/sicd_example_1_PFA_RE32F_IM32F_HH.nitf"   # <-- CHANGE ME: path to your SICD file
out_dir = "output_dir"    # <-- CHANGE ME: directory where SIDD files will be written
os.makedirs(out_dir, exist_ok=True)  # ensure the directory exists

# We'll define filenames for our three output SIDD products:
detected_sidd_file = os.path.join(out_dir, "detected_sidd.nitf")
csi_sidd_file = os.path.join(out_dir, "csi_sidd.nitf")
dynamic_sidd_file = os.path.join(out_dir, "dynamic_sidd.nitf")


##############################################################################
# 2) Open the raw (complex) data and create an ortho-rectification helper
##############################################################################

# Open the complex (SICD) file
reader = open_complex(infile)

# Create an ortho rectification helper (nearest-neighbor for simplicity)
# index=0 means use the first SICD in the file if multiple are present
ortho_helper = NearestNeighborMethod(reader, index=0)


##############################################################################
# 3) Generate the three SIDD products
##############################################################################

# --- 3A) A standard grayscale “detected” product ---
create_detected_image_sidd(
    ortho_helper,
    output_directory=out_dir,
    output_file=os.path.basename(detected_sidd_file),  # e.g. "detected_sidd.nitf"
    block_size=10,   # read in ~10 MB blocks
    version=2        # produce a SIDD version 2, for example
)

# --- 3B) A color sub-aperture image (3-band) ---
create_csi_sidd(
    ortho_helper,
    output_directory=out_dir,
    output_file=os.path.basename(csi_sidd_file),
    dimension=0,  # which dimension of the radar data is split into sub-apertures
    version=2
)

# --- 3C) A dynamic image (sub-aperture stack, multiple frames) ---
create_dynamic_image_sidd(
    ortho_helper,
    output_directory=out_dir,
    output_file=os.path.basename(dynamic_sidd_file),
    dimension=0,
    version=2,
    frame_count=5,         # produce 5 frames
    aperture_fraction=0.2  # sub-apertures each ~20% of the total aperture
)


##############################################################################
# 4) Open the generated SIDDs and visualize with matplotlib
##############################################################################

# Helper function to display single-band or multi-band images
def display_image(data, title=""):
    """
    data: a numpy ndarray
    title: plot title
    """
    plt.figure()
    if data.ndim == 2:
        # single band => grayscale
        plt.imshow(data, cmap='gray')
    elif data.ndim == 3:
        # either color (RGB) or multi-frame
        # We'll guess it's color if shape[2] is 3 or 4, or multi-frame otherwise
        if data.shape[2] in (3, 4):
            # color
            plt.imshow(data)
        else:
            # multi-frame => just show the first frame
            plt.imshow(data[:, :, 0], cmap='gray')
            plt.title(title + " (Showing first frame only)")
            return
    else:
        # fallback
        plt.imshow(data, cmap='gray')
    plt.title(title)

# --- 4A) Detected Image (grayscale) ---
detected_reader = open_product(detected_sidd_file)
detected_data = detected_reader[:]  # read entire product
display_image(detected_data, title="Detected Image SIDD")

# --- 4B) CSI (color sub-aperture image) ---
csi_reader = open_product(csi_sidd_file)
csi_data = csi_reader[:]
display_image(csi_data, title="CSI Image SIDD")

# --- 4C) Dynamic Image (multi-frame) ---
dynamic_reader = open_product(dynamic_sidd_file)
dynamic_data = dynamic_reader[:]
# dynamic_data might be shape (rows, cols, frames) or (frames, rows, cols).
# Typically, Sarpy SIDD reading yields (rows, cols, frames).
# We'll do a quick shape check
print(f"Dynamic data shape = {dynamic_data.shape}")

# We'll animate if it's truly multi-frame in the last dimension:
if dynamic_data.ndim == 3 and dynamic_data.shape[2] > 1:
    fig, ax = plt.subplots()
    implot = ax.imshow(dynamic_data[:, :, 0], cmap='gray')

    def update(frame_index):
        implot.set_data(dynamic_data[:, :, frame_index])
        ax.set_title(f"Dynamic Image Frame {frame_index+1}")
        return [implot]

    ani = animation.FuncAnimation(
        fig, update, frames=dynamic_data.shape[2], interval=500, blit=True
    )
    plt.show()
else:
    # If it's single-band or single-frame, just display a static image
    display_image(dynamic_data, title="Dynamic Image SIDD")

# Show all figures
plt.show()
