# piano_roll_app.py
import sys
import os
from pathlib import Path

dir_path = Path(__file__).resolve().parent.parent

fluidsynth_path = dir_path / 'bin' / 'fluidsynth' / 'bin'

os.environ['PATH'] += os.pathsep + str(fluidsynth_path)

soundfont_path = Path(__file__).parent.parent / 'soundfonts' / 'GU_GS.sf2'

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from view import Viewer
from menuBar import Menu
from actions.toMidi import MidiConverter
from actions.toString import StringConverter
from actions.newAction import NewAction
from actions.synth_manager import SynthManager

import pickle

class Window(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.synth = SynthManager(soundfont_path=str(soundfont_path))
        self.setWindowTitle('MIDI Creation App')
        self.resize(900, 600)
        self.centralWidget = Viewer(synth=self.synth)
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)
        self.setMenuBar(Menu(self,
                             synth_manager=self.synth,
                             midi_callback=self.export_midi, 
                             tensor_callback=self.save_tensor, 
                             new_callback=self.newAction,
                             add_callback=self.addMeasure,
                             remove_callback=self.removeMeasure))

    def export_midi(self):
        print("Exporting MIDI...")
        grid = self.centralWidget.scene()
        converter = MidiConverter(grid, self.synth)
        converter.convert_to_midi("output.mid")
        print("MIDI file has been saved.")
    
    def save_tensor(self):
        print("Saving Tesnor...")
        grid = self.centralWidget.scene()
        converter = StringConverter(grid)
        tensor = converter.extract_string()
        with open('tensor.pkl', 'wb') as f:
            pickle.dump(tensor, f)

    def newAction(self):
        if NewAction.show_confirmation_dialog():
            grid = self.centralWidget.scene()
            grid.clearNotes()
            grid.updateGrid()
        else:
            print("Not Updating!")

    def addMeasure(self):
        grid = self.centralWidget.scene()
        grid.addMeasure()

    def removeMeasure(self):
        grid = self.centralWidget.scene()
        grid.removeMeasure()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())