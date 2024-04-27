from PyQt5.QtWidgets import QGraphicsView
from piano_roll_grid import PianoRollGrid
from PyQt5.QtCore import Qt
from pathlib import Path

soundfont_path = Path(__file__).parent / 'soundfonts' / 'GU_GS.sf2'


class Viewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(PianoRollGrid(107, 20, 100, 40, str(soundfont_path)))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)