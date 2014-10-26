ControlCombo
============

**WHAT**

ControlCombo is a physical button matrix aimed at simulating tricky keyboard shortcuts or other mouse/keyboard interactions. In addition, with a system of plugin, it can perform (in an independant thread) more or less any action coded in Python.

ControlCombo is made of two parts:
- The Arduino-hosted part, with a matrix of buttons, sending messages to the computer
- The computer-hosted part, that receives the message and translate them into actions


**WHY**

ControlCombo was originally develop to perform tricky keyboard shortcuts used in software like Adobe Photoshop of Adobe Lightroom, in order to add a bit of automatisation and ease at use.
Then I realized it was a shame to limit ControlCombo to keyboard shortcut ony and decided to add a plugin management part. A plugin (written in Python) can perform everything, and does it in a parallel thread. This way, if the triggered action takes a while, it does not block the use of the button matrix.


**HOW**

At the very beginning, ControlCombo was developped on Windows, using the Win32com library to perform keyboard actions. This system was very convenient due to the flexibility provided by the Microsoft library. The keyboard sequences interpretation was the core of ControlCombo, and the plugin system was just an additional feature, a goody.
Then I had to switch to Mac OSX, not able to use Win32com anymore, I had to find an alternative. Hopefully guys at PyUserInput (https://github.com/SavinaRoja/PyUserInput) developed a pretty nice (and cross plateform) library to simulate keyboard and mouse actions from Python.

This library will be used now instead of Win32com, but involve a quite important refactoring in ControlCombo, for the best, making it cross-plateform as well!

Since keyboard sequences are not as easy to write with PyUserInput as with Win32com, the actions will be perform from plugins exclusivelly. So now, ControlCombo plugins are no longer a goody but a total part of the core.
