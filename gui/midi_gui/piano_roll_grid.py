# piano_roll_grid.py
import os
from pathlib import Path

dir_path = Path(__file__).resolve().parent.parent

fluidsynth_path = dir_path / 'bin' / 'fluidsynth' / 'bin'

os.environ['PATH'] += os.pathsep + str(fluidsynth_path)

from PyQt5.QtGui import QPen, QColor

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF

from noteButton import noteButton
from actions.synth_manager import SynthManager

class PianoRollGrid(QGraphicsScene):
    def __init__(self, rows, cols, x_size, y_size, synth: SynthManager) -> None:
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.x_size = x_size
        self.y_size = y_size
        self.key_width = x_size

        self.synth = synth

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

        self.drawHorizontalLines()
        self.drawMeasures(self.cols)

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
                    self.synth.play_note(note_number)
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
        for j in range(cols + 1):
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
        for i in range(self.rows):
            y = i * self.y_size
            for j in range(self.cols):
                x = j * self.x_size + self.key_width
                bg_color = QColor('lightblue') if ((i + 21) % 12) in [1,3,6,8,10] else QColor('white')
                bg_rect = QGraphicsRectItem(x, y, self.x_size, self.y_size)
                bg_rect.setBrush(bg_color)
                bg_rect.setPen(QPen(Qt.NoPen))
                self.addItem(bg_rect)
    
        light_pen = QPen(QColor(140, 233, 236))
        for i in range(self.rows):
            y = i * self.y_size
            # Draw a line from the right edge of the keys to the end of the scene
            self.addLine(self.key_width, y, self.width(), y, light_pen)

    def drawVerticalLines(self, start_col=0):
        dark_pen = QPen(Qt.darkGray)
        dark_pen.setWidth(2)
        for j in range(start_col, self.cols):
            if j % 4 == 0:
                x = j * self.x_size + self.key_width
                self.addLine(x, 0, x, self.rows * self.y_size, dark_pen)

    def addNoteButton(self, row_index, col_index):
        x = col_index * self.x_size + self.key_width
        y = row_index * self.y_size
        button = noteButton(x, y, self.x_size, self.y_size, row_index)
        self.addItem(button)
        self.note_buttons.append(button)
        return button

    def get_note_buttons(self):
        return self.note_buttons
    
    def clearNotes(self):
        for note_button in self.note_buttons:
            self.removeItem(note_button)
        self.note_buttons.clear() 

    def addMeasure(self):
        self.extendGrid()

    def removeMeasure(self):
        self.reduceGrid()

    def extendGrid(self):
        self.cols += 4

        new_width = self.cols * self.x_size + self.key_width
        self.setSceneRect(0, 0, new_width, self.height())

        self.drawHorizontalLines()
        self.drawMeasures(self.cols)

    def reduceGrid(self):
        measure_length = 4  # This should match the measure length used in extendGrid
        if self.cols > measure_length:
            # Calculate the x-coordinate from where to start removing items
            start_col = self.cols - measure_length
            x_start = start_col * self.x_size + self.key_width

            # Reduce the number of columns
            self.cols -= measure_length

            # Update the scene rectangle to the new dimensions
            new_width = self.cols * self.x_size + self.key_width
            new_height = self.rows * self.y_size
            self.setSceneRect(0, 0, new_width, new_height)

            # Collect all items whose bounding rectangles extend beyond the new grid width
            items_to_remove = [item for item in self.items() if item.sceneBoundingRect().right() >= x_start]
            for item in items_to_remove:
                self.removeItem(item)
            
            self.drawHorizontalLines()
            self.drawMeasures(self.cols)
        else:
            print("Cannot reduce grid further without having fewer than measure length columns.")

if __name__ == '__main__':
    grid = PianoRollGrid(50, 50, 50, 20)  
    grid.run()

