# gridManager.py
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import Qt

from piano_roll_grid import PianoRollGrid

class GridManager:
    def __init__(self, grid: PianoRollGrid):
        self.grid = grid

    def addMeasure(self):
        measure_length = 4  # Assuming each measure adds 4 beats/columns
        self.grid.cols += measure_length  # Increase the number of columns
        self.extendGrid()

    def removeMeasure(self):
        measure_length = 4
        if self.grid.cols - measure_length >= self.grid.min_cols:
            self.grid.cols -= measure_length
            self.grid.reduceGrid()
        else:
            print("Minimum columns reached")

    def extendGrid(self):
        start_col = self.grid.cols - 4
        for i in range(self.grid.rows):
            y = i * self.grid.y_size
            for j in range(start_col, self.cols):
                x = j * self.grid.x_size + self.grid.key_width
                bg_color = QColor('lightblue') if ((i + 21) % 12) in [1,3,6,8,10] else QColor('white')
                bg_rect = QGraphicsRectItem(x, y, self.x_size, self.y_size)
                bg_rect.setBrush(bg_color)
                bg_rect.setPen(QPen(Qt.NoPen))
                self.grid.addItem(bg_rect)
        
        self.grid.drawHorizontalLines()
        self.grid.drawMeasures(self.grid.cols)


    def reduceGrid(self):
        # Implement the logic to reduce the grid size, similar to extendGrid but in reverse
        pass
