import os

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import Sound, SoundLoader
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget

import morse_code_sound as ms

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'  # Enable to prevent OpenGL error
root_widget = Builder.load_file('app.kv')

MORSE_CODE_DICT = {'A': ' .- ', 'B': ' -... ',
                   'C': ' -.-. ', 'D': ' -.. ', 'E': ' . ',
                   'F': ' ..-. ', 'G': ' --. ', 'H': ' .... ',
                   'I': ' .. ', 'J': ' .--- ', 'K': ' -.- ',
                   'L': ' .-.. ', 'M': ' -- ', 'N': ' -. ',
                   'O': ' --- ', 'P': ' .--. ', 'Q': ' --.- ',
                   'R': ' .-. ', 'S': ' ... ', 'T': ' - ',
                   'U': ' ..- ', 'V': ' ...- ', 'W': ' .-- ',
                   'X': ' -..- ', 'Y': ' -.-- ', 'Z': ' --.. ',
                   '1': ' .---- ', '2': ' ..--- ', '3': ' ...-- ',
                   '4': ' ....- ', '5': ' ..... ', '6': ' -.... ',
                   '7': ' --... ', '8': ' ---.. ', '9': ' ----. ',
                   '0': ' ----- ', ', ': ' --..-- ', '.': ' .-.-.- ',
                   '?': ' ..--.. ', '/': ' -..-. ', '-': ' -....- ',
                   '(': ' -.--. ', ')': ' -.--.- '}

# threading multiprocessing


class MainWidget(Widget):
    string = ObjectProperty()
    loop = BooleanProperty(False)
    sound = True

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.typewriter = Clock.create_trigger(self.type_morse, .1)
        self.morse_loop = Clock.create_trigger(self.repeat, .25)

    def translate_to_morse(self):

        self.string = self.string.replace(" ", "+")

        for char in self.string:
            if char in MORSE_CODE_DICT:
                self.string = self.string.replace(char, MORSE_CODE_DICT[char])

        self.string = self.string.replace("+", "/")
        self.string += " "
        ms.create_wav_file(self.string)
        self.morse_sound = SoundLoader.load('morse_code.wav')
        if self.sound:
            self.morse_sound.play()

    def type_morse(self, dt):
        self.ids.morse_label.text += self.string[0]
        self.string = self.string[1:]
        if len(self.string) > 0:
            self.typewriter()

    def repeat(self, dt):
        if self.ids.string_morsify.text != "":
            if self.loop:
                self.ids.morse_label.text += self.string[0]
                self.string = self.string[1:]
                if len(self.string) > 0:
                    self.morse_loop()
                elif len(self.string) == 0:
                    if self.ids.loop_checkbox.active:

                        self.string = self.ids.string_morsify.text + " "
                        self.ids.morse_label.text = ""
                        self.morse_loop()
                    else:
                        pass

    def mute_sound(self):
        if self.sound == True:
            self.sound = False
            try:
                self.morse_sound.stop()
            except AttributeError:
                pass
        else:
            self.sound = True
            try:
                self.morse_sound.play()
            except AttributeError:
                pass

    def delete_wav_file(self):
        f = "sounds/morse_code.wav"
        if os.path.exists(f):
            os.remove(f)
        else:
            print("failed to delete: ", f)


class MorsifierApp(App):
    MainWidget = MainWidget()

    def build(self):
        return self.MainWidget


MorsifierApp().run()
