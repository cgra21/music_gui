from PyQt5.QtWidgets import QMenuBar, QWidget
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction


class Menu(QMenuBar):

    def __init__(self, parent: QWidget | None, midi_callback=None, tensor_callback=None, new_callback = None) -> None:
        super().__init__(parent)
        self.midi_callback = midi_callback
        self.tensor_callback = tensor_callback
        self.new_callback = new_callback

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
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)


        helpMenu = QMenu('&Help', self)
        self.addMenu(helpMenu)
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)


    def _create_actions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        self.newAction.setText("&New")
        # Creating actions using the second constructor
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)
        self.toMidiAction = QAction("To Midi", self)
        self.toTensorAction = QAction("To Tensor", self)