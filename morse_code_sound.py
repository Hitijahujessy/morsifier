import struct
import wave

import numpy as np
from pydub import AudioSegment

RATE = 44100


def sine_samples(freq, dur):
    x = (2*np.pi*freq/RATE) * np.arange(RATE*dur)

    sine = (32767*np.sin(x)).astype(int)

    as_packed_bytes = (map(lambda v: struct.pack('h', v), sine))
    return as_packed_bytes


def output_wave(path, frames):
    output = wave.open(path, 'w')
    output.setparams((2, 2, RATE, 0, 'NONE', 'not compresses'))
    output.writeframes(frames)
    output.close()


def output_sound(path, freq, dur):
    frames = b''.join(sine_samples(freq, dur))

    output_wave(path, frames)


TIME_UNIT = 0.132
output_sound('sounds/sine320s.wav', 320, TIME_UNIT)  # .
output_sound('sounds/sine320l.wav', 320, TIME_UNIT * 3)  # -
output_sound('sounds/sine0.wav', 0, TIME_UNIT)  # /


def create_wav_file(morse_string):
    play_sound = AudioSegment.from_wav('sounds/sine0.wav')
    for morse in morse_string:
        if morse == '.':
            tone = AudioSegment.from_wav('sounds/sine320s.wav')
            play_sound += tone
        elif morse == '-':
            tone = AudioSegment.from_wav('sounds/sine320l.wav')
            play_sound += tone
        elif morse == ' ':
            tone = AudioSegment.from_wav('sounds/sine0.wav')
            play_sound += tone * 2
        elif morse == '/':
            tone = AudioSegment.from_wav('sounds/sine0.wav')
            play_sound += tone * 6
        tone = AudioSegment.from_wav('sounds/sine0.wav')
        play_sound += tone
    play_sound.export("sounds/morse_code.wav", format='wav')
