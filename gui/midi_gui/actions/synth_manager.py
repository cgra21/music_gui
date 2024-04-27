# synth_manager.py
import os
from pathlib import Path

dir_path = Path(__file__).resolve().parent.parent

fluidsynth_path = dir_path / 'bin' / 'fluidsynth' / 'bin'

os.environ['PATH'] += os.pathsep + str(fluidsynth_path)

import fluidsynth
import threading
import time

class SynthManager:
    def __init__(self, soundfont_path, driver='dsound'):
        self.synth = fluidsynth.Synth()
        self.synth.start(driver=driver)
        self.sfid = self.synth.sfload(soundfont_path)
        self.program = 0
        self.change_instrument(0,self.program)
    
    def change_instrument(self, bank, program):
        """Change the instrument for the synthesizer."""
        self.synth.program_select(0, self.sfid, bank, program)
        self.program = program

    def play_note(self, note, duration=1):
        """Play a note on the synthesizer"""
        def note_thread():
            self.synth.noteon(0, note, 100)  # Channel 0, MIDI note number, velocity
            time.sleep(duration)  # Duration in milliseconds
            self.synth.noteoff(0, note)  # Turn off the note
        threading.Thread(target=note_thread).start()

    def get_instrument(self):
        return self.program