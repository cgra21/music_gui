from PyQt5.QtWidgets import QGraphicsView
from piano_roll_grid import PianoRollGrid
from PyQt5.QtCore import Qt
from pathlib import Path

from actions.synth_manager import SynthManager
from actions.grid_manager import GridManager

class Viewer(QGraphicsView):
    def __init__(self, synth: SynthManager):
        super().__init__()
        self.setScene(PianoRollGrid(107, 20, 100, 40, synth=synth))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)