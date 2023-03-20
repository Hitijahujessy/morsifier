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
        self.clipboard = self.morse_string  # Make sure that copy_morse copies the correct string
        ms.create_wav_file(self.morse_string)
        self.morse_sound = SoundLoader.load('sounds/morse_code.wav')
        self.play_sound()

    def create_labels(self, string_to_label):
        string_list = []
        words = 6
        split_string = string_to_label.split()
        lines = len(split_string) / words
        index = 0
        endex = words
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
        for label in self.ids.scroll_layout.children:
            self.ids.scroll_layout.remove_widget(label)
        if len(self.ids.scroll_layout.children) == 0:
            print("succesfully deleted labels")
        else:
            print("failed to delete labels")

    def create_morse_string(self, string):
        string = string.strip()
        string = string.replace(" ", "+")
        string = string.replace(".", "·")
        string = string.replace("-", "–")
        for char in string:
            if char in MORSE_CODE_DICT:
                string = string.replace(
                    char, MORSE_CODE_DICT[char] + " ")
            else:
                string = string.replace(
                    char, " ")
        string = string.replace(" +", " / ")
        string = string.replace("+", "")
        
        return string

    def type_morse(self, dt):
        label = self.get_label()
        if label:
            self.morse_string = label.hidden_text
            index = len(label.hidden_text) - len(label.text)
            label.text += label.hidden_text[-index]
            self.get_downtime(label.hidden_text[-(index-1)])
            self.typewriter = Clock.create_trigger(self.type_morse, self.downtime)
            self.typewriter()
        else:
            print("finished type writing")

    def repeat(self, dt):
        self.typewriter.cancel()
        if self.loop:
            self.play_sound(restart=True)
            if dt == 1:
                self.ids.scroll_view.scroll_y = 1
            label = self.get_label()

            colored_char = self.highlight(self.morse_string[0])
            self.morse_string[0] = ''.join(colored_char)
            self.morse_string = self.morse_string[1:]
            
            try:
                self.get_downtime(self.morse_string[0])
            except IndexError:
                self.get_downtime(self.clipboard[0])
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
            
    def highlight(self, char):
        for label in self.ids.scroll_layout.children:
            label.text.replace("[color=ff0000]", "")
            label.text.replace("[/color]", "")
            
        return "[color=ff0000]"+char+"[/color]"

    def highlight_old(self):
        try:
            self.ids.morse_label.text = self.ids.morse_label.text.replace(
                "[color=ff0000]", "")
            self.ids.morse_label.text = self.ids.morse_label.text.replace(
                "[/color]", "")
        except:
            pass
        index = abs(len(self.morse_string) - len(self.clipboard))
        list1 = list(self.clipboard)
        character = list1[index]
        list1[index] = "[color=ff0000]"+character+"[/color]"
        self.ids.morse_label.text = ''.join(list1)
        return list1

    def loop_toggle(self):
        check = self.ids.loop_toggle

        if check.state == "normal":
            self.loop = False
            self.ids.morse_label.text = self.ids.morse_label.text.replace(
                "[color=ff0000]", "")
            self.ids.morse_label.text = self.ids.morse_label.text.replace(
                "[/color]", "")
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
