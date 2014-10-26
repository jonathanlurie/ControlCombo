ControlCombo
============

**What is it?**

ControlCombo is a physical button matrix aimed at simulating tricky keyboard shortcuts or other mouse/keyboard interactions. In addition, with a system of plugin, it can perform (in an independant thread) more or less any action coded in Python.

ControlCombo is made of two parts:
- The Arduino-hosted part, with a matrix of buttons, sending messages to the computer
- The computer-hosted part, that receives the message and translate them into actions


**Why was it made?**

ControlCombo was originally develop to perform tricky keyboard shortcuts used in software like Adobe Photoshop of Adobe Lightroom, in order to add a bit of automatisation and ease at use.
Then I realized it was a shame to limit ControlCombo to keyboard shortcut ony and decided to add a plugin management part. A plugin (written in Python) can perform everything, and does it in a parallel thread. This way, if the triggered action takes a while, it does not block the use of the button matrix.


**How does work the simulation?**

At the very beginning, ControlCombo was developped on Windows, using the Win32com library to perform keyboard actions. This system was very convenient due to the flexibility provided by the Microsoft library. The keyboard sequences interpretation was the core of ControlCombo, and the plugin system was just an additional feature, a goody.
Then I had to switch to Mac OSX, not able to use Win32com anymore, I had to find an alternative. Hopefully guys at PyUserInput (https://github.com/SavinaRoja/PyUserInput) developed a pretty nice (and cross plateform) library to simulate keyboard and mouse actions from Python.

This library will be used now instead of Win32com, but involve a quite important refactoring in ControlCombo, for the best, making it cross-plateform as well!

Since keyboard sequences are not as easy to write with PyUserInput as with Win32com, the actions will be perform from plugins exclusivelly. So now, ControlCombo plugins are no longer a goody but a total part of the core.



**How does the communication with Arduino work?**

The Arduino board sends serial messages at 9600 bauds. At the initialization, the board sends a message containing the number of rows column that composes the matrix, in order to calibrate the computer-hosted program. The test board contains 16 buttons, arranged in a 4x4 matrix, it's not too big, and not too small.

Every button within the matrix is is indexed, starting from 1 (upper left corner) to 16 (lower right corner), this index is the basis of what compose to message to be sent to the computer-hosted program. Then, depending on the action performed on this button (pressed, released or hold), a a factor is applied on the index, and the message is sent.
- For "pressed" the factor is 1
- For "released" the factor is -1
- For "hold" the factor is 1000

For example, when the last button of the second row is pressed, the message "8" is sent, when it's released, the message "-8" is sent and if, in between, it was hold longer than 750ms, the message "8000" is send.

Since the computer-hosted program knows the size of the matrix, the message sent informs the computer of what button was "actioned", in which way and where it is located within the matrix.


**How the mapping of action does work?**
