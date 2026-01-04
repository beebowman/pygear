# -*- coding: utf-8 -*-
"""
pygear GUI
Author: beebowman
Updated Jan 4, 2026

Based on original gear math by Sam Ettinger (2016)
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import math
import os

# Default parameters
gearRatio = 2
gearOverlap = 1.0
computationSteps = 1000

# =======================
# Gear math functions
# =======================

def loadGearImage():
    filename = filedialog.askopenfilename(
        filetypes=[("PNG Images", ("*.png",))]  # Only PNG allowed
    )
    if not filename:
        return None
    img = Image.open(filename).convert('L')
    img.load()
    data = np.asarray(img)
    array2d = np.array([[np.median(j) if isinstance(j,(list,np.ndarray)) else j for j in i] for i in data])
    return array2d, img

def getBlackPixels(image, offset):
    rows = len(image)
    cols = len(image[0])
    size = max(rows, cols)
    scale = 2./size
    coords = []
    for row in range(rows):
        for col in range(cols):
            if image[row][col] == 0:
                x = scale*(col - (cols-1)/2.) + offset[0]
                y = scale*(row - (rows-1)/2.) + offset[1]
                coords.append((x, y))
    return coords, size

def rotatePts(points, axis, theta):
    return [(((x - axis[0])*math.cos(theta) - (y - axis[1])*math.sin(theta)) + axis[0],
             ((x - axis[0])*math.sin(theta) + (y - axis[1])*math.cos(theta)) + axis[1])
            for (x,y) in points]

def outputGearImage(image, coords, size, ratio):
    newImage = image
    for (x,y) in coords:
        row = int((y+ratio)*size/(2*ratio))
        col = int((x+ratio)*size/(2*ratio))
        try:
            newImage[row][col] = 255.0
        except:
            pass
    return newImage

def dist(x, y):
    return math.sqrt(x*x + y*y)

def outputCleanup(image):
    newImage = image
    size = len(image)
    radius = size/2.
    for row in range(size):
        for col in range(size):
            if dist(row-radius, col-radius) >= radius-.5:
                newImage[row][col] = 255.0
    markRadius = max(2., size/200.)
    for i in range(50):
        theta = i*2*math.pi/50
        x = int(round(radius + markRadius*math.cos(theta)))
        y = int(round(radius + markRadius*math.sin(theta)))
        newImage[y, x] = 255.0
    return newImage

def writeOutputGear(gear, filename):
    img = Image.fromarray(gear)
    img = img.convert('RGB')
    img.save(filename)

# =======================
# Correct Crossbar Function
# =======================
def drawCrossbar(distance):
    distance = int(distance) # ensure integer
    '''Draws the image of the crossbar that holds the two gear axles'''
    # Size of the image:
    height = int(round(distance/6.))
    width = int(np.ceil(distance*7./6))
    # Coordinates of the axle holes' centers:
    radius = height/2. - 0.5
    holeOne = (radius, radius)
    holeTwo = (distance + radius, radius)
    # Initialize image as all white
    crossbarImage = 255.0 * np.ones((height, width))
    # Draw main horizontal bar (top and bottom rows)
    crossbarImage[(0, height-1), int(np.ceil(holeOne[0])):int(np.floor(holeTwo[0])+1)] = 0.0
    # Draw rounded ends along the sides
    for i in range(distance):
        theta = np.pi*i/distance - np.pi/2
        rows = (int(round(holeOne[1] - radius*np.sin(theta))), int(round(holeTwo[1] + radius*np.sin(theta))))
        cols = (int(round(holeOne[0] - radius*np.cos(theta))), int(round(holeTwo[0] + radius*np.cos(theta))))
        crossbarImage[rows, cols] = 0.0
    # Draw axle holes
    markRadius = max(2., distance/200.) # hole radius
    for i in range(50):
        theta = i*2*np.pi/50
        x = int(round(holeOne[0] + markRadius*np.cos(theta)))
        y = int(round(holeOne[1] + markRadius*np.sin(theta)))
        crossbarImage[y, x] = 0.0
        crossbarImage[y, x+distance] = 0.0
    return crossbarImage

# =======================
# GUI
# =======================

class PygearGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pygear GUI")
        self.geometry("750x800")
        self.resizable(False, False)

        self.inputGearArray = None
        self.inputGearImage = None
        self.tk_image = None
        self.outputGear = None
        self.crossbar = None

        self.ratio = None
        self.overlap = None
        self.steps = None

        self.progress_label = None
        self.progress_bar = None

        self.showMainPage()

    # ---------------- Main Page ----------------
    def showMainPage(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Pygear", font=("Arial", 32, "bold")).pack(pady=20)
        tk.Label(self, text="Author: beebowman", font=("Arial", 16)).pack(pady=10)

        # Instructions
        instructions_text = (
            "Welcome to Pygear!\n\n"
            "This tool allows you to take an input gear image (PNG) and generate a new gear\n"
            "that meshes with it based on your specified parameters. You can adjust:\n"
            "- Gear Ratio: determines the relative size of the generated gear.\n"
            "- Gear Overlap: controls how closely the gears mesh together.\n"
            "- Computation Steps: affects smoothness and accuracy of the rotation.\n\n"
            "Workflow:\n"
            "1. Create a PNG black outline of a gear (e.g. you can draw it in Word, then take a screenshot and convert to PNG).\n"
            "2. Click 'Load Gear Image' to select your input gear PNG.\n"
            "3. Adjust the gear parameters on the next page.\n"
            "4. Click 'Run' to generate the output gear.\n"
            "5. Preview and save the generated gear (gear that meshes with your inputted gear) and crossbar (line between gear centers) images.\n"
            "6. Use 'Download All' on the final page to save all images at once.\n\n"
            "Tips:\n"
            "- Higher Gear Ratio = larger output gear, lower = smaller.\n"
            "- Adjust Gear Overlap to avoid gaps or collisions between gears.\n"
            "- Higher Computation Steps = smoother gear output (slower computation)."
        )
        tk.Label(self, text=instructions_text, font=("Arial", 11), justify="left", fg="gray").pack(pady=20, padx=20)

        tk.Button(self, text="Load Gear Image", font=("Arial", 14), command=self.loadGearSafe).pack(pady=20)

    # ---------------- Load Gear ----------------
    def loadGearSafe(self):
        try:
            result = loadGearImage()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{e}")
            return
        if result is None:
            messagebox.showinfo("Cancelled", "No image loaded.")
            return
        self.inputGearArray, self.inputGearImage = result
        self.showGearPage()

    # ---------------- Gear Parameter Page ----------------
    def showGearPage(self):
        for widget in self.winfo_children():
            widget.destroy()

        max_size = 500
        w, h = self.inputGearImage.size
        scale = min(max_size/w, max_size/h, 1.0)
        new_w, new_h = int(w*scale), int(h*scale)
        img_resized = self.inputGearImage.resize((new_w, new_h))
        self.tk_image = ImageTk.PhotoImage(img_resized)
        tk.Label(self, image=self.tk_image).pack(pady=10)

        param_frame = tk.Frame(self)
        param_frame.pack(pady=10)

        # Subtle background color
        box_bg = "#f0f0f0"

        # ---- Gear Ratio ----
        tk.Label(param_frame, text="Gear Ratio:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        gear_ratio_box = tk.Frame(param_frame, bd=2, relief="solid", bg=box_bg, padx=2, pady=2)
        gear_ratio_box.grid(row=0, column=1, padx=5, pady=5)
        self.gearRatioEntry = tk.Entry(gear_ratio_box, width=10, bg="white", relief="flat")
        self.gearRatioEntry.insert(0, str(gearRatio))
        self.gearRatioEntry.pack()
        tk.Label(param_frame, text=(
            "Determines the relative size between input (driving) and output (driven) gear.\n"
            "1 = both gears are the same size.\n"
            "2 = generated gear (driven output gear) is twice as large as the input gear.\n"
            "Higher ratio = larger output gear, lower ratio = smaller output gear."
        ), font=("Arial", 9), fg="gray", justify="left").grid(row=0, column=2, sticky="w", padx=5)

        # ---- Gear Overlap ----
        tk.Label(param_frame, text="Gear Overlap:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        gear_overlap_box = tk.Frame(param_frame, bd=2, relief="solid", bg=box_bg, padx=2, pady=2)
        gear_overlap_box.grid(row=1, column=1, padx=5, pady=5)
        self.gearOverlapEntry = tk.Entry(gear_overlap_box, width=10, bg="white", relief="flat")
        self.gearOverlapEntry.insert(0, str(gearOverlap))
        self.gearOverlapEntry.pack()
        tk.Label(param_frame, text=(
            "Controls how closely the gears mesh.\n"
            "Higher values bring gears closer together.\n"
            "Lower values move them apart.\n"
            "Adjust to ensure gears fit without gaps or collisions."
        ), font=("Arial", 9), fg="gray", justify="left").grid(row=1, column=2, sticky="w", padx=5)

        # ---- Computation Steps ----
        tk.Label(param_frame, text="Computation Steps:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        computation_steps_box = tk.Frame(param_frame, bd=2, relief="solid", bg=box_bg, padx=2, pady=2)
        computation_steps_box.grid(row=2, column=1, padx=5, pady=5)
        self.computationStepsEntry = tk.Entry(computation_steps_box, width=10, bg="white", relief="flat")
        self.computationStepsEntry.insert(0, str(computationSteps))
        self.computationStepsEntry.pack()
        tk.Label(param_frame, text=(
            "Number of steps to compute the gear rotation.\n"
            "Higher numbers give smoother, more accurate output.\n"
            "Lower numbers run faster but may be less precise."
        ), font=("Arial", 9), fg="gray", justify="left").grid(row=2, column=2, sticky="w", padx=5)

        tk.Button(self, text="Run", font=("Arial", 14), command=self.showRunningMessage).pack(pady=20)

    # ---------------- Running Page ----------------
    def showRunningMessage(self):
        try:
            self.ratio = int(self.gearRatioEntry.get())
            self.overlap = float(self.gearOverlapEntry.get())
            self.steps = int(self.computationStepsEntry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input parameters.")
            return

        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Running... please wait a full minute,\nit takes a while to process...", font=("Arial", 16)).pack(pady=20)
        self.progress_label = tk.Label(self, text="Progress: 0%", font=("Arial", 14))
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self, length=400, mode='determinate')
        self.progress_bar.pack(pady=10)

        self.update()
        self.after(100, self.runComputationStepwise, 0, None, None)

    # ---------------- Stepwise Computation ----------------
    def runComputationStepwise(self, step=0, outputGear=None, inputCoords=None):
        ratio = self.ratio
        overlap = self.overlap
        steps = self.steps

        if inputCoords is None:
            offset = (ratio + 1 - overlap, 0)
            inputCoords, inputImageSize = getBlackPixels(self.inputGearArray, offset)
            outputImageSize = inputImageSize * ratio
            outputGear = np.zeros([outputImageSize, outputImageSize])
            self.inputCoords = inputCoords
            self.outputGearSize = outputImageSize
            self.inputImageSize = inputImageSize
            self.theta = 2*math.pi / steps
            self.phi = 2*math.pi / (steps*ratio)

        if step < steps:
            coords = rotatePts(self.inputCoords, (ratio + 1 - overlap, 0), self.theta*step)
            addPoints = [c for c in coords if dist(*c) < ratio]
            for extra in range(ratio):
                rotateBy = self.phi*step + 2*math.pi*extra/ratio
                addPointsRot = rotatePts(addPoints, (0,0), rotateBy)
                outputGear = outputGearImage(outputGear, addPointsRot, self.outputGearSize, ratio)

            percent = int((step+1)/steps*100)
            self.progress_label.config(text=f"Progress: {percent}%")
            self.progress_bar['value'] = percent
            self.update()
            self.after(1, self.runComputationStepwise, step+1, outputGear, self.inputCoords)
        else:
            outputGear = outputCleanup(outputGear)
            self.outputGear = outputGear
            self.showGearPreview()

    # ---------------- Gear Preview + Save ----------------
    def showGearPreview(self):
        preview_img = Image.fromarray(self.outputGear).convert('RGB')
        max_preview = 500
        w, h = preview_img.size
        scale = min(max_preview/w, max_preview/h, 1.0)
        preview_img = preview_img.resize((int(w*scale), int(h*scale)))
        self.tk_image = ImageTk.PhotoImage(preview_img)

        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Preview of Generated Gear", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, image=self.tk_image).pack(pady=10)
        tk.Button(self, text="Save Gear", font=("Arial", 14), command=self.saveGearFile).pack(pady=20)

    def saveGearFile(self):
        outFile = filedialog.asksaveasfilename(defaultextension=".png", initialfile="gear_output.png")
        if outFile:
            writeOutputGear(self.outputGear, outFile)
        self.showCrossbarPage()

    # ---------------- Crossbar Preview + Save ----------------
    def showCrossbarPage(self):
        ratio = self.ratio
        overlap = self.overlap
        inputImageSize = len(self.inputGearArray)
        self.crossbar = drawCrossbar(inputImageSize*(ratio+1-overlap)/2)

        preview_img = Image.fromarray(self.crossbar).convert('RGB')
        max_preview = 500
        w, h = preview_img.size
        scale = min(max_preview/w, max_preview/h, 1.0)
        preview_img = preview_img.resize((int(w*scale), int(h*scale)))
        self.tk_image = ImageTk.PhotoImage(preview_img)

        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Preview of Crossbar (Line Between Gear Centers)", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, image=self.tk_image).pack(pady=10)
        tk.Button(self, text="Save Crossbar", font=("Arial", 14), command=self.saveCrossbarFile).pack(pady=20)

    def saveCrossbarFile(self):
        outFile = filedialog.asksaveasfilename(defaultextension=".png", initialfile="crossbar.png")
        if outFile:
            writeOutputGear(self.crossbar, outFile)
        self.showFinalPreviewPage()

    # ---------------- Final Preview Page ----------------
    def showFinalPreviewPage(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Final Preview", font=("Arial", 18, "bold")).pack(pady=10)

        # Images with captions and filenames
        images = [
            (self.inputGearImage, "Input Gear Image", "input_gear.png"),
            (Image.fromarray(self.outputGear).convert('RGB'), "Output Gear Image", "output_gear.png"),
            (Image.fromarray(self.crossbar).convert('RGB'), "Crossbar Image (Line Between Gear Centers)", "crossbar.png")
        ]

        frame = tk.Frame(self)
        frame.pack(pady=10)
        self.final_tk_images = []

        for img, caption, _ in images:
            max_size = 200
            w, h = img.size
            scale = min(max_size/w, max_size/h, 1.0)
            resized = img.resize((int(w*scale), int(h*scale)))
            tk_img = ImageTk.PhotoImage(resized)
            self.final_tk_images.append(tk_img)

            img_frame = tk.Frame(frame)
            img_frame.pack(side='left', padx=10)

            tk.Label(img_frame, image=tk_img).pack()
            tk.Label(img_frame, text=caption, font=("Arial", 12)).pack(pady=5)

        # Download all button
        def download_all():
            downloads_dir = os.path.expanduser("~/Downloads")
            for img, _, filename in images:
                path = os.path.join(downloads_dir, filename)
                if isinstance(img, np.ndarray):
                    Image.fromarray(img).convert('RGB').save(path)
                else:
                    img.save(path)
            messagebox.showinfo("Download Complete", f"All images saved to {downloads_dir}")

        tk.Button(self, text="Download All", font=("Arial", 14), command=download_all).pack(pady=10)
        tk.Button(self, text="Start Over", font=("Arial", 14), command=self.showMainPage).pack(pady=10)

# ---------------- Run App ----------------
if __name__ == "__main__":
    app = PygearGUI()
    app.mainloop()
