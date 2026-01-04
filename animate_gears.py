# -*- coding: utf-8 -*-
"""
Animation for Pygear - GIF + Optional MP4 Export

- Always saves a GIF using Pillow (no ffmpeg needed)
- Saves MP4 automatically if ffmpeg is available
- Shows animation popup window
- One full 360-degree rotation

@author: Bo Bowman
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter
from tkinter import filedialog
from create_gear import getBlackPixels
from scipy.ndimage import label


# -------------------------------------------------
# Image utilities
# -------------------------------------------------

def loadGearImage(title="Select Gear Image"):
    """Ask user to select a PNG gear image and return as numpy array."""
    filename = filedialog.askopenfilename(
        title=title,
        filetypes=[("PNG Images", "*.png")]
    )
    if not filename:
        return None

    img = Image.open(filename).convert('L')
    data = np.asarray(img)

    array2d = np.array([
        [np.median(j) if isinstance(j, (list, np.ndarray)) else j for j in row]
        for row in data
    ])

    return array2d


def cleanGearImage(array2d, threshold=128):
    """Keep only the largest black region in a grayscale image."""
    binary = array2d < threshold
    labeled, num_features = label(binary)

    if num_features == 0:
        return array2d

    sizes = np.bincount(labeled.ravel())
    sizes[0] = 0
    largest_label = sizes.argmax()

    cleaned_binary = (labeled == largest_label)
    return np.where(cleaned_binary, 0, 255).astype(np.uint8)


# -------------------------------------------------
# Geometry utilities
# -------------------------------------------------

def rotatePtsArray(coords, origin, angle):
    """Vectorized rotation of Nx2 array around origin by angle (radians)."""
    coords = np.array(coords)
    ox, oy = origin
    x, y = coords[:, 0], coords[:, 1]

    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    x_new = ox + (x - ox) * cos_a - (y - oy) * sin_a
    y_new = oy + (x - ox) * sin_a + (y - oy) * cos_a

    return np.column_stack((x_new, y_new))


# -------------------------------------------------
# Animation
# -------------------------------------------------

def animateGears(
    inputGearArray,
    outputGearArray,
    ratio,
    overlap,
    frames=90,                 # short animation
    fps=30,
    downsample=2,
    gif_file="pygear_rotation.gif",
    mp4_file="pygear_rotation.mp4"
):
    """Animate gears and save GIF + optional MP4."""

    offset = (ratio + 1 - overlap, 0)

    inCoords, _ = getBlackPixels(inputGearArray, offset)
    outCoords, _ = getBlackPixels(cleanGearImage(outputGearArray), (0, 0))

    if downsample > 1:
        inCoords = inCoords[::downsample]
        outCoords = outCoords[::downsample]

    outCoords = [(ratio * x, ratio * y) for (x, y) in outCoords]

    inCoords = np.array(inCoords)
    outCoords = np.array(outCoords)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    scatter_in, = ax.plot(inCoords[:, 0], inCoords[:, 1], 'ro', markersize=2)
    scatter_out, = ax.plot(outCoords[:, 0], outCoords[:, 1], 'bo', markersize=2)

    def update(frame):
        theta = 2 * np.pi * frame / frames
        phi = -theta * ratio

        in_rot = rotatePtsArray(inCoords, offset, phi)
        out_rot = rotatePtsArray(outCoords, (0, 0), theta)

        scatter_in.set_data(in_rot[:, 0], in_rot[:, 1])
        scatter_out.set_data(out_rot[:, 0], out_rot[:, 1])
        return scatter_in, scatter_out

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=1000 / fps,
        blit=True
    )

    # -----------------------------
    # Save GIF (always)
    # -----------------------------
    print(f"Saving GIF: {gif_file}")
    gif_writer = PillowWriter(fps=fps)
    ani.save(gif_file, writer=gif_writer)
    print("GIF saved successfully.")

    # -----------------------------
    # Attempt MP4 (optional)
    # -----------------------------
    try:
        from matplotlib.animation import FFMpegWriter
        print(f"Saving MP4: {mp4_file}")
        mp4_writer = FFMpegWriter(fps=fps, bitrate=1800)
        ani.save(mp4_file, writer=mp4_writer)
        print("MP4 saved successfully.")
    except Exception as e:
        print("MP4 export skipped (ffmpeg not available).")

    plt.show()


# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()

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

    animateGears(
        inputGearArray,
        outputGearArray,
        ratio,
        overlap
    )
