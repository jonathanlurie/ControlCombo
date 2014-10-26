ControlCombo
============

## What is it?

ControlCombo is a physical button matrix aimed at simulating tricky keyboard shortcuts or other mouse/keyboard interactions. In addition, with a system of plugin, it can perform (in an independant thread) more or less any action coded in Python.

ControlCombo is made of two parts:
- The Arduino-hosted part, with a matrix of buttons, sending messages to the computer
- The computer-hosted part, that receives the message and translate them into actions



## Why was it made?

ControlCombo was originally develop to perform tricky keyboard shortcuts used in software like Adobe Photoshop of Adobe Lightroom, in order to add a bit of automatisation and ease at use.
Then I realized it was a shame to limit ControlCombo to keyboard shortcut only and decided to add a plugin management part. A plugin (written in Python) can perform everything, and does it in a parallel thread. This way, if the triggered action takes a while, it does not block the use of the other buttons.



## How does work the simulation?

At the very beginning, ControlCombo was developed on Windows, using the Win32com library to perform keyboard actions. This system was very convenient due to the flexibility provided by the Microsoft library. The keyboard sequence interpretation was the core of ControlCombo, and the plugin system was just an additional feature, a goody.
Then I had to switch to Mac OSX. Not able to use Win32com anymore, I had to find an alternative. Hopefully guys at [PyUserInput](https://github.com/SavinaRoja/PyUserInput) developed a pretty nice and cross platform library to simulate keyboard and mouse actions from Python.

This library will be used instead of Win32com, but involve a quite important refactoring in ControlCombo, for the best, making it cross-platform as well!

Since keyboard sequences are not as easy to write with PyUserInput as with Win32com, the actions will be perform from plugins exclusivelly. So now, ControlCombo plugins are no longer a goody but a total part of the core.



## How does the communication with Arduino work?

The Arduino board sends serial messages at 9600 bauds. At the initialization, the board sends a message containing the number of rows and column that composes the matrix, in order to calibrate the computer-hosted program. The test board contains 16 buttons, arranged in a 4x4 matrix, it's not too big, and not too small.

Every button within the matrix is indexed, starting from 1 (upper left corner) to 16 (lower right corner), this index is the basis of what composes the message to be sent to the computer-hosted program. Then, depending on the action performed on this button (pressed, released or hold), a factor is applied to the index, and the message is sent.
- For "pressed" the factor is 1 (no change)
- For "released" the factor is -1
- For "hold" the factor is 1000

For example, when the last button of the second row is pressed, the message "8" is sent, when it's released, the message "-8" is sent and if, in between, it was hold longer than 750ms, the message "8000" is send.

Since the computer-hosted program knows the size of the matrix, the message sent informs the computer of what button was "actioned", in which way and where it is located within the matrix.

Note: the 1000 factor for the "holding" action may be a limit if a huge matrix is built, containing more than 1000 buttons (more than size 31x32). Anyway, this limitation can be changed if really needed...



## How does the mapping of action work?

As said on the previous part, three actions per button are possible. Since we will mostly work with the plugin system (and no more with Win32com sequences), we will describe more extensively this part.

1- The map file
The map file is a text file located in the "input" subdirectory, and have the extension ".setting". It contains the mapping instructions: what button, what action, what plugin.


1- Spatial organization
We saw that the Arduino part indexes the button from 1 to N (N being the total number of buttons). The computer-hosted part does not deal with it the same way. Actually the mapping file considers the matrix, as a matrix, with letter-indexed rows and number-indexed columns (like in the battleship game, I guess)

A example is always better, here is a line you can find in the mapping file:

```
A 1 P plugin|samplePlugin|methodWithArguments|12|100

```

Explanations:
- A stands for the first row
- 1 stands for the first column
- P stands "for Pressed". It would have been "R" for "released" or "H" for "hold"
- plugin|samplePlugin|methodWithArguments|12|100 is the action associated with this behavior

Other example:

```
C 2 R plugin|samplePlugin|methodWithArguments|12|100
```
Here, the actioned is triggered when the 2nd button (2) from the 3rd row (C) is released (R).

_Important note : it looks like whitespace, but TABS are actually used for splitting arguments!_


The pluggin system and its syntax will be more described in the next part.


## How to use plugins?

Plugins are python source files, located in the "plugins" subdirectory. They contain functions that may have arguments (as you need).

Lets analyse the previously used mapping instruction:

```
C 2 R plugin|samplePlugin|methodWithArguments|12|100
```

So what does mean "plugin|samplePlugin|methodWithArguments|12|100" ?

1- Note the separator is a pipe ("|")
2- "plugin" as a firs part mean we are actually using a plugin (and not a Win32com string)
3- "samplePlugin" refers to the file "samplePlugin.py" present in the "plugin" subfolder.
4- "methodWithArguments" is a function written in the "samplePlugin.py" file
5- "12" and "100" are just two arguments for the function "methodWithArguments". You can use string with whitespaces, but not TAB!

Here is the content of the file __samplePlugin.py__

```python
# shows a simple plugin that takes arguments.
# just performs a sum and display it.
def methodWithArguments(number1, number2):
  result = int(number1) + int(number2)
  print(">> what about that: " + str(number1) +  " + " + str(number2) + " = " + str(result))
```


## Dependancies

TODO


## TODO

- Adding the PyUserInput library
- Getting rid of Win32com dependances
- Writing the list of dependancies
- Making an advanced plugin for Adobe Lightroom
- Integrating the bridge to AppleScript in a plugin (clearly not a priority)
