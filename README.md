# pygear

How to make organically-shaped gears? How to make weird gears, unique gears? You've come to the right place! 

This is a gear maker (with gui!) based on the video ["How to make Organically-Shaped Gears"](https://youtu.be/3LdlSAN1yks) by Clayton Boyer. This approach is not suited to gears that drastically change their gear ratios, for example [nautilus gears](https://youtu.be/IUR-T4Nw-Sk).

[![Gear Demos: one success, one failure](https://img.youtube.com/vi/2XJWHQcnk54/0.jpg)](https://www.youtube.com/watch?v=2XJWHQcnk54)

## Credit To
Credit to Sam Ettinger for inspiring me to make this pygear GUI! For more info on Sam's work, here's a link to non-GUI versions: 
https://www.settinger.net/projects.php?project=gears 

[create_gear.py.zip](https://github.com/user-attachments/files/24424404/create_gear.py.zip)


## Dependencies

Written in Python 3.12.7. Requires numpy, tkinter and PIL (pillow). 

To install these libraries, type the following into the Terminal on your computer: 
* pip install pillow
* pip install numpy

(Tkinter is part of the Python standard library)

## Operation

Before running the app code, manually create your input gear as a PNG image. 
1) Open Word Document (or equivalent)
2) Use Draw feature to draw a black outline of an organic/weird/unique gear
<img width="700" height="721" alt="HowToCreateInputGearPNG" src="https://github.com/user-attachments/assets/9e8f1ea6-1239-4809-8b40-b4e45f9ec15d" />


4) Take a screenshot of just the gear outline
5) Save the screenshot as a PNG image type (e.g. File > Export > PNG on Mac) 
6) Confirm that you have python installed on your computer (open Terminal, type in python --version), you should see output such as "Python 3.12.7".
7) Download create_gear.py (keep track of location where you download it)
8) In the Terminal app on your computer, navigate to the folder containing create_gear.py 
9) Run `create_gear.py` (type "python create_gear.py" in the Terminal)
10) Click on "Load Gear Image" to select your input gear shape (it will prompt you to select a file, so select your png gear file). The program assumes the center of the image is the center of the gear.
<img width="400" alt="Load Gear Image" src="https://github.com/user-attachments/assets/f0c21d1f-929e-4dff-a27e-bec24e581de8" />

12) Keep parameters as-is (or modify) and click Run.
<img width="500" alt="EnterParameters" src="https://github.com/user-attachments/assets/e829dbcb-1e88-4a68-a559-eab2a0b5f99c" />

14) After some time, the program will output a gear that will functional work together with your original gear image. Save it. 
<img width="410" alt="GeneratedGear" src="https://github.com/user-attachments/assets/237eb6a5-2ac1-4e64-a5b8-1f85bb4fe7f0" />

16) You'll be prompted to save a "crossbar" image. Save it. 
<img width="350" alt="Crossbar" src="https://github.com/user-attachments/assets/c1abcdc4-24ca-4092-a69b-76b7889f290c" />

17) Last, you have the option to download all files.
<img width="580" alt="Screenshot 2026-01-04 at 12 50 29 PM" src="https://github.com/user-attachments/assets/2a40a48e-3279-42e7-a398-a61b592c85a6" />

19) So, for an input that looks like this:

<img width="303.5" alt="weirdgear_input_image" src="https://github.com/user-attachments/assets/f50bb307-c287-4531-8074-69be5c4c657a" />

...you'll get two outputs (generated gear, and crossbar distance between gear centers):

<img width="1214" alt="weirdgear_output_image" src="https://github.com/user-attachments/assets/b9edb4df-818c-4b60-9458-a72ed12bde9c" />

<img width="708.5" alt="crossbar" src="https://github.com/user-attachments/assets/36d83ed4-75c0-4a07-8de4-b9e92d6b0e4c" />

... and you can save them, convert them to 2D Sketches (svg, dxf) to physically create your own pair of functioning weird gears! 

If you want to change the gear generation parameters, edit the following variables at the start of `create_gear.py`:
* `gearRatio` is the gear ratio. For example, a ratio of 2 means the input gear completes two rotations in the time it takes the output gear to complete one rotation. Right now, this has to be an integer value.
* `gearOverlap` controls how close the gears' axes are. It should be between 0.0 and 1.0. I'd say 1.0 is a good value to start with.
* `computationSteps` is the number of steps in the image processing process. Too few steps and you'll be left with lots of speckles and noise outside output gear perimeter. Too many steps and you'll waste computer time without seeing much of an effect. 1000 is a good value to start with.

## ANIMATION:

To run an animation of your gears together: 
1) In the Terminal app, run animate_gears.py (type in python animate_gears.py)
2) Select your input gear PNG image, then your output gear PNG image
3) Enter the gear ratio and gear overlap that you used when creating your gears:
   <img width="316" height="29" alt="Screenshot 2026-01-04 at 1 28 27 PM" src="https://github.com/user-attachments/assets/0c316bfb-b094-494a-84c4-e0b03ce8b77e" />

5) View your pretty weird gears animation! :)
<img width="524" height="373" alt="Screenshot 2026-01-04 at 1 28 30 PM" src="https://github.com/user-attachments/assets/c8c3b3ac-9cd9-4baa-b6a6-ac6af7a8ad08" />

