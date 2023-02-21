import struct
import wave

import numpy as np
from pydub import AudioSegment
from playsound import playsound

RATE = 44100


def sine_samples(freq, dur):
    x = (2*np.pi*freq/RATE) * np.arange(RATE*dur)

    s = (32767*np.sin(x)).astype(int)

    as_packed_bytes = (map(lambda v: struct.pack('h', v), s))
    return as_packed_bytes


def output_wave(path, frames):
    output = wave.open(path, 'w')
    output.setparams((2, 2, RATE, 0, 'NONE', 'not compresses'))
    output.writeframes(frames)
    output.close()


def output_sound(path, freq, dur):
    frames = b''.join(sine_samples(freq, dur))

    output_wave(path, frames)

time_unit = 0.1
output_sound('sine440s.wav', 440, time_unit)
output_sound('sine440l.wav', 440, time_unit * 3)
output_sound('sine0.wav', 0, time_unit)

def create_wav_file(morse_string):
    play_sound = AudioSegment.from_wav('sine0.wav')
    for morse in morse_string:
        if morse == '.':
            tone = AudioSegment.from_wav('sine440s.wav')
            play_sound += tone
        elif morse == '-':
            tone = AudioSegment.from_wav('sine440l.wav')
            play_sound += tone
        elif morse == ' ':
            tone = AudioSegment.from_wav('sine0.wav')
            play_sound += tone * 2
        elif morse == '/':
            tone = AudioSegment.from_wav('sine0.wav')
            play_sound += tone * 6
        tone = AudioSegment.from_wav('sine0.wav')
        play_sound += tone
    play_sound.export("morse_code.wav", format='wav')

