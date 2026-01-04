# pygear

Let's make gears that look like whatever we want! Weird gears, organic gears, unique gears! 

This is a gear maker based on the video ["How to make Organically-Shaped Gears"](https://youtu.be/3LdlSAN1yks) by Clayton Boyer. This approach is not suited to gears that drastically change their gear ratios, for example [nautilus gears](https://youtu.be/IUR-T4Nw-Sk).

[![Gear Demos: one success, one failure](https://img.youtube.com/vi/2XJWHQcnk54/0.jpg)](https://www.youtube.com/watch?v=2XJWHQcnk54)

## Dependencies

Requires numpy, tkinter and PIL (pillow). Written in Python 3.12.7. 

To install these libraries, type the following into the Terminal on your computer: 

**pip install pillow

pip install numpy**

(Tkinter is part of the Python standard library)

## Operation

Run `main.py` and select your input gear shape. The program assumes the center of the image is the center of the gear. After some calculation time, the program will prompt you to save your output gear as an image file. It will then prompt you to save a "crossbar" image. So, for an input that looks like this:

![](https://github.com/settinger/pygear/blob/master/test_gear_in.png "Input")

...you'll get two outputs:

![](https://github.com/settinger/pygear/blob/master/test_gear_out.png "Output") ![](https://github.com/settinger/pygear/blob/master/test_crossbar.png "Crossbar")

If you want to change the gear generation parameters, edit the following variables at the start of `main.py`:
* `gearRatio` is the gear ratio. For example, a ratio of 2 means the input gear completes two rotations in the time it takes the output gear to complete one rotation. Right now, this has to be an integer value.
* `gearOverlap` controls how close the gears' axes are. It should be between 0.0 and 1.0. I'd say 1.0 is a good value to start with.
* `computationSteps` is the number of steps in the image processing process. Too few steps and you'll be left with lots of speckles and noise outside output gear perimeter. Too many steps and you'll waste computer time without seeing much of an effect. 1000 is a good value to start with.

## TODO:

* Set up animation (there is an aborted attempt in the file `animate.py`)
* Make a GUI (probably in someting other than python?)
