import os
import shutil

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
import platform

import morse_code_sound as ms

if "macOS" in platform.platform():
    root_widget = Builder.load_file("app_mac.kv")
    os.environ["KIVY_AUDIO"] = "avplayer"
else:
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'  # Enable to prevent OpenGL error
    root_widget = Builder.load_file('app.kv')


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
    morse_string = ObjectProperty()
    text_string = ObjectProperty()
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
        self.check_loop = Clock.schedule_once(self.activate_loop, 0)

    def translate_to_morse(self):
        self.morse_string = self.create_morse_string(self.text_string)
        self.create_labels(self.morse_string)
        # Make sure that copy_morse copies the correct string
        self.clipboard = self.morse_string
        ms.create_wav_file(self.morse_string)
        self.morse_sound = SoundLoader.load('sounds/morse_code.wav')
        self.play_sound()

    def create_labels(self, string_to_label):
        string_list = []
        words = 3
        split_string = string_to_label.split("/")
        lines = len(split_string) / words
        index = 0
        endex = words
        for s in range(len(split_string)):
            if s != (len(split_string)-1):
                split_string[s] = split_string[s] + ' /'
                print(split_string)
        while lines > 0:
            lines -= 1
            string_list.append(split_string[index:endex])
            index += words
            endex += words
        
        print(string_list)

        for i, string in enumerate(string_list):
            morse_label = Factory.MorseLabel()
            self.ids.scroll_layout.add_widget(morse_label)
            morse_label.hidden_text = ' '.join(string)
            morse_label.id = "morse" + str(i)

    def get_label(self):
        """Returns a label if its displayed text is different than its hidden text"""
        for label in reversed(self.ids.scroll_layout.children):
            if label.text == label.hidden_text:
                continue
            print(label.id)
            return label
        print("no labels have a hidden text")

    def delete_labels(self):
        temp = self.ids.scroll_layout.children[:]
        for label in temp:
            self.ids.scroll_layout.remove_widget(label)
        if len(self.ids.scroll_layout.children) == 0:
            print("succesfully deleted all scroll labels")
        else:
            for label in self.ids.scroll_layout.children:
                print("failed to delete label:" + label.id)

    def create_morse_string(self, string):
        string = string.strip()
        string = string.replace(" ", "+")
        string = string.replace(".", "·")
        string = string.replace("-", "–")
        for char in string:
            if char in MORSE_CODE_DICT:
                string = string.replace(
                    char, MORSE_CODE_DICT[char] + " ")
        string = string.replace(" +", " / ")
        string = string.replace("+", "")
        string = string.strip()

        return string

    def type_morse(self, dt):
        label = self.get_label()
        if label:
            self.morse_string = label.hidden_text
            index = len(label.hidden_text) - len(label.text)
            label.text += label.hidden_text[-index]
            self.get_downtime(label.hidden_text[-(index-1)])
            self.typewriter = Clock.create_trigger(
                self.type_morse, self.downtime)

            self.typewriter()
            
        else:
            print("finished type writing")

    def repeat(self, dt):
        self.typewriter.cancel()
        if self.loop:

            if dt >= 1:
                self.play_sound(restart=True)
                self.ids.scroll_view.scroll_y = 1
            else:
                self.play_sound()

            t = self.highlight()
            print(t)

            self.morse_string = self.morse_string[1:]

            try:
                self.get_downtime(self.morse_string[0])
            except IndexError:
                self.downtime = 1
            if len(self.morse_string) == 0:
                self.downtime = 1
            self.morse_loop = Clock.create_trigger(self.repeat, self.downtime)
            if len(self.morse_string) > 0:
                self.morse_loop()
            elif len(self.morse_string) == 0:
                if self.ids.loop_toggle.state == "down":
                    self.morse_string = self.clipboard
                    self.morse_loop()

    def get_downtime(self, char):
        if char == '.':
            self.downtime = .132
        elif char == '-':
            self.downtime = .132 * 2
        elif char == ' ':
            self.downtime = .132 * 2
        elif char == '/':
            self.downtime = .132 * 1
        # self.downtime = 0.05

    def highlight(self):

        next_line = self.ids.scroll_layout.children[-1]
        next_label = False
        for label in reversed(self.ids.scroll_layout.children):
            if "[color=ff0000]" in label.text:
                i = list(label.text).index("[") + 1
                try:
                    label.text = label.hidden_text[:i] + "[color=ff0000]" + \
                        label.hidden_text[i] + "[/color]" + \
                        label.hidden_text[i+1:]
                    return "changed inline highlight at index: " + str(i) + " of label: " + str(label.id)
                except IndexError:
                    label.text = label.hidden_text[:]
                    next_label = True
            elif next_label:
                next_line = label
                break

        if len(self.ids.scroll_layout.children) > 0:
            if next_line.id == "morse0" and next_label is True:
                return "Got to the end of the loop"
            else:
                next_line.text = "[color=ff0000]" + next_line.hidden_text[0] + \
                    "[/color]" + next_line.hidden_text[1:]
                return "started highlight at the beginging of the label: " + str(next_line.id)
        else:
            print("No labels exist")

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
            self.check_loop()

    def activate_loop(self, dt):
        """Waits for the full morse string to appear on screen"""
        for label in self.ids.scroll_layout.children:
            if label.text != label.hidden_text:
                self.check_loop()
            elif self.clipboard:
                self.morse_string = self.clipboard
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
