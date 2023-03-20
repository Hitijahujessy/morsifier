import os
import shutil

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import Sound, SoundLoader
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

import morse_code_sound as ms

# os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'  # Enable to prevent OpenGL error
root_widget = Builder.load_file('app.kv')
os.environ["KIVY_AUDIO"] = "avplayer"

MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ',': '--..--', '·': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '–': '-....-',
                   '(': '-.--.', ')': '-.--.-', "'": '.----.',
                   '"': '.-..-.', '!': '-·-·--'}

REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

# threading multiprocessing


class MainWidget(Widget):
    string = ObjectProperty()
    clipboard = ObjectProperty()
    loop = BooleanProperty(False)
    sound = BooleanProperty(True)
    savefile = ObjectProperty(None)
    morse_sound = ObjectProperty(None)
    downtime = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.typewriter = Clock.create_trigger(self.type_morse, self.downtime)
        self.morse_loop = Clock.create_trigger(self.repeat, self.downtime)

    def translate_to_morse(self):
        self.string = self.string.strip()
        self.string = self.string.replace(" ", "+")
        self.string = self.string.replace(".", "·")
        self.string = self.string.replace("-", "–")
        for char in self.string:
            if char in MORSE_CODE_DICT:
                self.string = self.string.replace(
                    char, MORSE_CODE_DICT[char] + " ")
        self.string = self.string.replace(" +", " / ")
        self.string = self.string.replace("+", "")
        self.clipboard = self.string  # Make sure that copy_morse copies the correct string
        ms.create_wav_file(self.string)
        self.morse_sound = SoundLoader.load('sounds/morse_code.wav')
        self.play_sound()

    def type_morse(self, dt):
        self.get_downtime()

        self.ids.morse_label.text += self.string[0]
        self.string = self.string[1:]
        self.typewriter = Clock.create_trigger(self.type_morse, self.downtime)
        if len(self.string) > 0:
            self.typewriter()

    def repeat(self, dt):
        self.typewriter.cancel()
        if self.loop:
            if self.morse_sound.state == "stop":
                self.play_sound(restart=True)
                self.ids.scroll_view.scroll_to(self.ids.morse_label) # Enable to have it scroll to the top when it restarts
            self.get_downtime()
            
            self.ids.morse_label.text = self.clipboard
            self.highlight()
            self.string = self.string[1:]

            if len(self.string) == 0:
                self.downtime = 1
            self.morse_loop = Clock.create_trigger(self.repeat, self.downtime)
            if len(self.string) > 0:
                self.morse_loop()
            elif len(self.string) == 0:
                if self.ids.loop_toggle.state == "down":
                    self.string = self.clipboard
                    self.morse_loop()

    def get_downtime(self):
        if self.string[0] == '.':
            self.downtime = .01#.132
        elif self.string[0] == '-':
            self.downtime = .01#.132 * 2
        if self.string[0] == ' ':
            self.downtime = .01#.132 * 2
        if self.string[0] == '/':
            self.downtime = .01#.132 * 1
                    
    def highlight(self):
        index = abs(len(self.string) - len(self.clipboard))
        list1 = list(self.clipboard)
        character = list1[index]
        list1[index] = "[color=ff0000]" + character + "[/color]"
        self.ids.morse_label.text = ''.join(list1)
        return list1

    def loop_toggle(self):
        check = self.ids.loop_toggle

        if check.state == "normal":
            self.loop = False
            try:
                self.morse_sound.stop()
            except AttributeError:
                pass
        elif check.state == "down":

            self.loop = True
            if self.clipboard:
                self.string = self.clipboard
                self.ids.morse_label.text = self.string
                self.morse_loop()

    def do_proceed(self):
        if not self.loop:
            self.typewriter()
        else:
            self.morse_loop()

    def play_sound(self, restart=False):
        if restart:
            self.morse_sound.stop()
        if self.morse_sound.state != "play":
            self.morse_sound.play()

        if self.sound is False:
            self.morse_sound.volume = 0
        else:
            self.morse_sound.volume = 1

    def mute_sound(self):
        if self.sound is True:
            self.sound = False
            try:
                self.morse_sound.volume = 0
            except AttributeError:
                print("self.morse_sound doesnt exist")
        else:
            self.sound = True
            try:
                self.morse_sound.volume = 1
            except AttributeError:
                print("self.morse_sound doesnt exist")

    def delete_file(self, f="sounds/morse_code.wav"):
        if os.path.exists(f):
            os.remove(f)
            if self.morse_sound:
                self.morse_sound.unload()
        else:
            print("failed to delete: ", f)
            print("file not found")

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        src_dir = "sounds/morse_code.wav"
        dst_dir = path + "//" + filename + ".wav"
        shutil.copy(src_dir, dst_dir)

        self.dismiss_popup()


class SaveDialog(Widget):
    save = ObjectProperty()
    text_input = ObjectProperty()
    cancel = ObjectProperty()


class MorsifierApp(App):
    MainWidget = MainWidget()

    def build(self):
        return self.MainWidget


MorsifierApp().run()
