# piano_roll_grid.py
import os

os.environ['PATH'] += os.pathsep + 'C:\\Users\\cjgra\\Documents\\FluidSynth\\bin'

import fluidsynth
import time
import threading

from PyQt5.QtWidgets import QGraphicsSceneMouseEvent, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor

import sys
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt

from noteButton import noteButton

class PianoRollGrid(QGraphicsScene):
    def __init__(self, rows, cols, x_size, y_size, soundfont_path, driver = 'dsound') -> None:
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.x_size = x_size
        self.y_size = y_size
        self.key_width = x_size

        self.synth = fluidsynth.Synth()
        # Start synthesizer
        self.synth.start(driver=driver)
        # Load a SoundFont (replace 'soundfont.sf2' with the path to your SoundFont file)
        sfid = self.synth.sfload(soundfont_path)
        self.synth.program_select(0, sfid, 0, 0)

        self.note_buttons = []

        self.setSceneRect(0, 0, cols * x_size + self.key_width, rows * y_size)
        self.updateGrid()

    def updateGrid(self):
        '''Function to create background grid, and piano keys on left of screen'''
        for i in range(self.rows):
            y = i * self.y_size

            # Used to calculate position of C note labels
            note_number = (self.rows - i - 1) + 21
            note_name, octave = self.noteName(note_number)

            if ((i + 21) % 12) in [1,3,6,8,10]:
                bg_color = QColor('lightblue')  # Background color for black keys
            else:
                bg_color = QColor('white')  # Background color for white keys

            # Create a full-width background rectangle for each row
            bg_rect = QGraphicsRectItem(0, y, self.cols * self.x_size + self.key_width, self.y_size)
            bg_rect.setBrush(bg_color)
            bg_rect.setPen(QPen(Qt.NoPen))
            self.addItem(bg_rect)   


            key = QGraphicsRectItem(0, y, self.key_width, self.y_size)
            if ((i+21) % 12) in [1, 3, 6, 8, 10]:  
                key.setBrush(QColor('black'))
            else:
                key.setBrush(QColor('white'))
            key.setData(0, 127 - i)
            self.addItem(key)

        
            if note_name == 'C':
                label = QGraphicsTextItem(f'{note_name}{octave}')
                label.setPos(5, y + (self.y_size - label.boundingRect().height()) / 2)  # Adjust label position
                self.addItem(label)


        self.drawMeasures(self.cols)
        self.drawHorizontalLines()

    def noteName(self, midi_number):
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note_index = (midi_number - 12) % 12  # MIDI note 12 is C1
        octave = (midi_number - 12) // 12
        return note_names[note_index], octave
    
    def mousePressEvent(self, event):
        items = self.items(event.scenePos())
        for item in items:
            if isinstance(item, QGraphicsRectItem):
                note_number = item.data(0)
                if note_number is not None:
                    self.play_note(note_number)
                    return
        super().mousePressEvent(event)

    # Handles creating new noteButton objects
    def mouseDoubleClickEvent(self, event):
        pos = event.scenePos()
        x = pos.x() - self.key_width
        y = pos.y()
        items = self.items(pos)
        if isinstance(items[0], noteButton): # check if there already exists a note, if so, remove it
            note = items[0]
            self.removeItem(note)
            
            # Remove from note list
            if note in self.note_buttons:
                self.note_buttons.remove(note)
            return
        elif x >= 0:  # Ensure clicks are within the grid area past the key width
            col = int(x // self.x_size)
            row = int(y // self.y_size)
            if 0 <= col < self.cols and 0 <= row < self.rows:
                self.addNoteButton(row, col)
        
    def drawMeasures(self, cols):
        dark_pen = QPen(Qt.darkGray)
        dark_pen.setWidth(2)  # Optional: Make the line thicker for visibility
        for j in range(cols):
            if j % 4 == 0:  # Every 4th column
                x = j * self.x_size + self.key_width
                self.addLine(x, 0, x, self.rows * self.y_size, dark_pen)
        light_pen = QPen(QColor(140, 233, 236))
        light_pen.setWidth(1)
        for j in range(cols):
            if j % 4 != 0:
                x = j * self.x_size + self.key_width
                self.addLine(x, 0, x, self.rows * self.y_size, light_pen)
    
    def drawHorizontalLines(self):
        light_pen = QPen(QColor(140, 233, 236))
        for i in range(self.rows):
            y = i * self.y_size
            # Draw a line from the right edge of the keys to the end of the scene
            self.addLine(self.key_width, y, self.width(), y, light_pen)

    def addNoteButton(self, row_index, col_index):
        x = col_index * self.x_size + self.key_width
        y = row_index * self.y_size
        button = noteButton(x, y, self.x_size, self.y_size, row_index)
        self.addItem(button)
        self.note_buttons.append(button)
        return button
    
    def addColumn(self):
        # TODO
        pass

    def delColumn(self):
        # TODO
        pass

    def get_note_buttons(self):
        return self.note_buttons
    
    def clearNotes(self):
        for note_button in self.note_buttons:
            self.removeItem(note_button)
        self.note_buttons.clear() 

    def play_note(self, note, duration=1):
        # Play the note
        def note_thread():
            self.synth.noteon(0, note, 100)  # Channel 0, MIDI note number, velocity
            time.sleep(duration)  # Duration in milliseconds
            self.synth.noteoff(0, note)  # Turn off the note
        threading.Thread(target=note_thread).start()

if __name__ == '__main__':
    grid = PianoRollGrid(50, 50, 50, 20)  
    grid.run()

