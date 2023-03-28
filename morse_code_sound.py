import struct
import wave
import os

import numpy as np
from pydub import AudioSegment

RATE = 44100


def sine_samples(freq, dur):
    x = (2*np.pi*freq/RATE) * np.arange(RATE*dur)

    sine = (32767*np.sin(x)).astype(int)

    as_packed_bytes = (map(lambda v: struct.pack('h', v), sine))
    return as_packed_bytes


def output_wave(path, frames):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
    output = wave.open(path, 'w')
    output.setparams((2, 2, RATE, 0, 'NONE', 'not compresses'))
    output.writeframes(frames)
    output.close()


def output_sound(path, freq, dur):
    frames = b''.join(sine_samples(freq, dur))

    output_wave(path, frames)



def create_sounds():
    output_sound('sounds/sine320s.wav', 320, TIME_UNIT)  # .
    output_sound('sounds/sine320l.wav', 320, TIME_UNIT * 3)  # -
    output_sound('sounds/sine0.wav', 0, TIME_UNIT)  # /
    print("Created wav files with TIME_UNIT: " + str(TIME_UNIT))
TIME_UNIT = 0.2
create_sounds()

def create_wav_file(morse_string):
    play_sound = AudioSegment.from_wav('sounds/sine0.wav')
    tone_short = AudioSegment.from_wav('sounds/sine320s.wav')
    tone_long = AudioSegment.from_wav('sounds/sine320l.wav')
    tone_silent = AudioSegment.from_wav('sounds/sine0.wav')
    
    for i, morse in enumerate(morse_string):
        if morse == '.':
            play_sound += tone_short
            try:
                if morse_string[i+1] == "." or morse_string[i+1] == "-":
                    play_sound += tone_silent
            except IndexError:
                pass
            
        elif morse == '-':
            play_sound += tone_long
            try:
                if morse_string[i+1] == "." or morse_string[i+1] == "-":
                    play_sound += tone_silent
            except IndexError:
                pass
            
        elif morse == ' ':
            try:
                if morse_string[i+1] == "/":
                    play_sound += tone_silent * 7
                elif morse_string[i-1 if i > 0 else i] == "/":
                    continue
                else:
                    play_sound += tone_silent * 3
            except IndexError:
                pass        
        
    play_sound.export("sounds/morse_code.wav", format='wav')
