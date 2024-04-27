import os

os.environ['PATH'] += os.pathsep + 'C:\\Users\\cjgra\\Documents\\FluidSynth\\bin'

import fluidsynth
import time

def play_piano_note(note, duration=0.3):
    fs = fluidsynth.Synth()
    # Load a SoundFont (replace 'soundfont.sf2' with the path to your SoundFont file)
    sfid = fs.sfload(r"C:\Users\cjgra\Documents\GitHub\Music-Generation\gui\sound_font\GeneralUser GS v1.471.sf2")
    fs.program_select(0, sfid, 0, 0)

    # Start synthesizer
    fs.start()

    # Play the note
    fs.noteon(0, note, 100)  # Channel 0, MIDI note number, velocity
    time.sleep(duration * 10)  # Duration in milliseconds
    fs.noteoff(0, note)  # Turn off the note

    # Stop the synthesizer and clean up
    fs.delete()

if __name__ == '__main__':
    # Play middle C (MIDI note number 60)
    play_piano_note(60)
