# -*- coding: utf-8 -*-
"""
Animation for Pygear - Optimized

Uses vectorized rotations and fast plotting for smooth animations.

@author: Bo Bowman
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation
from tkinter import filedialog
from create_gear import getBlackPixels, rotatePts
from scipy.ndimage import label

def loadGearImage(title="Select Gear Image"):
    """Ask user to select a PNG gear image and return as numpy array."""
    filename = filedialog.askopenfilename(title=title,
                                          filetypes=[("PNG Images", "*.png")])
    if not filename:
        return None
    img = Image.open(filename).convert('L')
    img.load()
    data = np.asarray(img)
    # Ensure 2D grayscale
    array2d = np.array([[np.median(j) if isinstance(j,(list,np.ndarray)) else j for j in i] for i in data])
    return array2d

def cleanGearImage(array2d, threshold=128):
    """
    Keep only the largest black region in a grayscale image.
    """
    binary = array2d < threshold
    labeled, num_features = label(binary)

    if num_features == 0:
        return array2d  # nothing black, return original

    sizes = np.bincount(labeled.ravel())
    sizes[0] = 0  # background
    largest_label = sizes.argmax()
    cleaned_binary = (labeled == largest_label)
    cleaned_array = np.where(cleaned_binary, 0, 255).astype(np.uint8)
    return cleaned_array

def rotatePtsArray(coords, origin, angle):
    """Vectorized rotation of Nx2 array around origin by angle radians."""
    coords = np.array(coords)
    ox, oy = origin
    x, y = coords[:,0], coords[:,1]
    x_new = ox + (x-ox)*np.cos(angle) - (y-oy)*np.sin(angle)
    y_new = oy + (x-ox)*np.sin(angle) + (y-oy)*np.cos(angle)
    return np.column_stack((x_new, y_new))

def animateGears(inputGearArray, outputGearArray, ratio, overlap, frames=60, downsample=2):
    """Animate two gears rotating with teeth interlocking."""

    # Compute black pixel coordinates
    offset = (ratio + 1 - overlap, 0)
    inCoords, inScale = getBlackPixels(inputGearArray, offset)
    outCoords, outScale = getBlackPixels(cleanGearImage(outputGearArray), (0,0))

    # Optional downsampling for speed
    if downsample > 1:
        inCoords = inCoords[::downsample]
        outCoords = outCoords[::downsample]

    # Scale output gear
    outCoords = [(ratio*x, ratio*y) for (x,y) in outCoords]

    # Convert to NumPy arrays for fast rotation
    inCoords = np.array(inCoords)
    outCoords = np.array(outCoords)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect('equal')
    ax.axis('off')

    # Plot points initially
    scatter_in, = ax.plot(inCoords[:,0], inCoords[:,1], 'ro', markersize=2)
    scatter_out, = ax.plot(outCoords[:,0], outCoords[:,1], 'bo', markersize=2)

    def update(frame):
        theta = 2*np.pi*frame/frames
        phi = -theta*ratio

        inGearRot = rotatePtsArray(inCoords, offset, phi)
        outGearRot = rotatePtsArray(outCoords, (0,0), theta)

        scatter_in.set_data(inGearRot[:,0], inGearRot[:,1])
        scatter_out.set_data(outGearRot[:,0], outGearRot[:,1])
        return scatter_in, scatter_out

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=30, blit=True)
    plt.show()


if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Hide root window

    print("Select input gear image (driving gear).")
    inputGearArray = loadGearImage("Select Input Gear Image")
    if inputGearArray is None:
        print("No input gear selected. Exiting.")
        exit()

    print("Select output gear image (driven gear).")
    outputGearArray = loadGearImage("Select Output Gear Image")
    if outputGearArray is None:
        print("No output gear selected. Exiting.")
        exit()

    ratio = float(input("Enter gear ratio (output/input, e.g., 2): "))
    overlap = float(input("Enter gear overlap (e.g., 1.0): "))

    # Animate with optional downsampling for speed
    animateGears(inputGearArray, outputGearArray, ratio, overlap, frames=60, downsample=2)
