# MIDI GUI
This is a basic midi gui controller for use with the music_gen project.

# Installation

Download the repository:
- git clone https://github.com/cgra21/music_gui

Navigate to the repository on your local machine.

Install the dependencies
- pip install -r requirements.txt
Install the package
- pip install -e .

# Usage

The program has two main uses, creation of midi files, and creation of text tensors for input to text models.

Measures are divided into four beats, there is currently not support for time signatures other than 4/4
In order to create notes, double click on a place on the grid. This will create a quarter note at that beat.
You can adjust the size and position of the note by clicking on it and extending or shrinking it.

You can change the instrument with the "Instruments" menu.

You can add or remove measures within the "Edit" menu.

If you wish to hear the pitches, click on the keyboard on the left, and it will play the respective sound.

# Known Bugs and Updates

- You can move the notes outside of the grid, or on top of the keyboard, doing so and trying to generate a MIDI or tensor will cause an error.

- You cannot move notes up or down in pitch

- When moving a note, it will snap back to its original position when moved more than once


