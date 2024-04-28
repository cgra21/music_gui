from PyQt5.QtWidgets import QMenuBar, QWidget
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction, QActionGroup

from actions.synth_manager import SynthManager

class Menu(QMenuBar):

    def __init__(self, parent: QWidget | None,
                 synth_manager: SynthManager,
                 midi_callback=None, 
                 tensor_callback=None, 
                 new_callback = None,
                 instrument_callback=None,
                 add_callback=None,
                 remove_callback=None) -> None:
        super().__init__(parent)
        self.synth_manager = synth_manager

        self.midi_callback = midi_callback
        self.tensor_callback = tensor_callback
        self.new_callback = new_callback
        self.instrument_callback = instrument_callback
        self.add_callback = add_callback
        self.remove_callback = remove_callback

        self._create_actions()
        self._create_menu_bar()

    def _create_menu_bar(self):
        fileMenu = QMenu('&File', self)
        self.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        fileMenu.addAction(self.toMidiAction)
        fileMenu.addAction(self.toTensorAction)


        if self.new_callback:
            print("Added new callback")
            self.newAction.triggered.connect(self.new_callback)
            fileMenu.addAction(self.newAction)
            
        if self.midi_callback:
            print("Added MIDI callback")
            self.toMidiAction.triggered.connect(self.midi_callback)  # Connect to MIDI conversion callback
            fileMenu.addAction(self.toMidiAction)
        
        if self.tensor_callback:
            print("Added Tensor callback")
            self.toTensorAction.triggered.connect(self.tensor_callback)
            fileMenu.addAction(self.toTensorAction)


        editMenu = QMenu('&Edit', self)
        self.addMenu(editMenu)
        editMenu.addAction(self.addMeasure)
        editMenu.addAction(self.removeMeasure)
        if self.add_callback:
            print("Added addMeasure callback")
            self.addMeasure.triggered.connect(self.add_callback)
            editMenu.addAction(self.addMeasure)
        
        if self.remove_callback:
            print("Added removeMeasure")
            self.removeMeasure.triggered.connect(self.remove_callback)
            editMenu.addAction(self.removeMeasure)

        # editMenu.addAction(self.copyAction)
        # editMenu.addAction(self.pasteAction)
        # editMenu.addAction(self.cutAction)


        helpMenu = QMenu('&Help', self)
        self.addMenu(helpMenu)
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

        instrumentMenu = QMenu('&Instruments',self)
        self.addMenu(instrumentMenu)
        self.add_instrument_actions(instrumentMenu)


    def _create_actions(self):
        # Creating action using the first constructor
        self.newAction = QAction('&New', self)
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("&Cut", self)

        self.addMeasure = QAction('&Add Measure', self)
        self.removeMeasure = QAction('&Remove Measure', self)

        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)
        self.toMidiAction = QAction("To Midi", self)
        self.toTensorAction = QAction("To Tensor", self)

    def add_instrument_actions(self, instrumentMenu):
        # Example instruments from each category
        instruments = [
            (0, "Piano - Acoustic Grand Piano"),
            (8, "Chromatic Percussion - Celesta"),
            (16, "Organ - Drawbar Organ"),
            (24, "Guitar - Acoustic Guitar"),
            (32, "Bass - Acoustic Bass"),
            (40, "Strings - Violin"),
            (48, "Ensemble - String Ensemble"),
            (56, "Brass - Trumpet"),
            (64, "Reed - Soprano Sax"),
            (72, "Pipe - Piccolo"),
            (80, "Synth Lead - Lead 1 (square)"),
            (88, "Synth Pad - Pad 1 (new age)"),
            (96, "Synth Effects - FX 1 (rain)"),
            (104, "Ethnic - Sitar"),
            (112, "Percussive - Tinkle Bell"),
            (120, "Sound Effects - Guitar Fret Noise")
        ]

        instrument_group = QActionGroup(self)
        instrument_group.setExclusive(True)

        for program, name in instruments:
            action = QAction(name, self, checkable=True)
            instrumentMenu.addAction(action)
            instrument_group.addAction(action)
            # Pass the program number to the callback
            action.triggered.connect(lambda checked, program=program: self.change_program(program))

    def change_program(self, program):
        # Default to bank 0 for GM compatibility
        bank = 0
        if self.synth_manager:
            self.synth_manager.change_instrument(bank, program)