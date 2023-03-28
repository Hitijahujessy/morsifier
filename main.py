import morse_code_sound as ms
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.app import App
import os
import platform
import shutil

import kivy
kivy.require("2.1.0")


if "macOS" in platform.platform():
    root_widget = Builder.load_file('app.kv')
else:
    # Enable to prevent OpenGL error
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
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
                   '?': '..--..', '|': '-..-.', '–': '-....-',
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
    downtime_sum = NumericProperty(0)
    multiplier = NumericProperty(1)
    flashlight_color = ObjectProperty((0, 0, 0, 1))

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.typewriter = Clock.create_trigger(self.type_morse, self.downtime)
        self.morse_loop = Clock.create_trigger(self.repeat, self.downtime)
        self.create_buttons()

        # Set the default wpm to 12
        self.change_tempo(self.speed_multi_dict["12"])

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
        MAX_CHAR = 25
        lines = 1 + len(string_to_label) // MAX_CHAR

        while lines > 0:
            n = 0
            line = None
            while not line:
                try:
                    if string_to_label[MAX_CHAR+1-n] == " ":
                        line = string_to_label[:MAX_CHAR+1-n]
                    else:
                        n += 1
                        if n > 6:
                            print("n shouldnt be higher than 6, n ==: " + str(n))
                except IndexError:
                    line = string_to_label[:]
            string_to_label = string_to_label[MAX_CHAR+1-n:]
            string_list.append(line)
            lines -= 1
            if string_to_label == "":
                break

        print(string_list)

        for i, string in enumerate(string_list):
            morse_label = Factory.MorseLabel()
            self.ids.scroll_layout.add_widget(morse_label)
            morse_label.hidden_text = ''.join(string)
            morse_label.id = "morse" + str(i)

    def get_label(self):
        """Returns a label if its displayed text is different than its hidden text"""
        for label in reversed(self.ids.scroll_layout.children):
            if label.text == label.hidden_text:
                continue
            # print(label.id)
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

    def create_buttons(self):
        """Create wpm buttons"""
        speed_list = [6, 8, 10, 12, 14, 16, 20, 22, 24, 26]
        self.speed_multi_dict = {}
        for speed in speed_list:
            multi = 0.1
            while speed != int(self.get_wpm(multi)):
                multi += 0.01
            button = Factory.SpeedButton()
            self.ids.button_grid.add_widget(button)
            button.text = str(speed)
            button.multiplier = multi
            self.speed_multi_dict[str(speed)] = multi

    def update_buttons(self):
        for button in self.ids.button_grid.children:
            button.disabled = False
        for button in self.ids.button_grid.children:
            if button.multiplier == self.multiplier:
                button.disabled = True
                break

    def create_morse_string(self, string):
        string = string.strip()
        string = string.replace(" ", "+")
        string = string.replace(".", "·")
        string = string.replace("-", "–")
        string = string.replace("/", "|")
        for char in string:
            if char in MORSE_CODE_DICT:
                string = string.replace(
                    char, MORSE_CODE_DICT[char] + " ")
        string = string.replace(" +", " / ")
        string = string.replace("+", "")

        return string

    def type_morse(self, dt):
        label = self.get_label()
        if label:
            self.morse_string = label.hidden_text
            index = len(label.hidden_text) - len(label.text)
            label.text += label.hidden_text[-index]
            self.set_downtime(label.text[-1])
            if label.text == label.hidden_text:
                self.scroll(label)
            if self.ids.morse_light.active == True:
                if label.text[-1] == "." or label.text[-1] == "-":
                    self.set_light_bar(self.downtime)

            self.typewriter = Clock.create_trigger(
                self.type_morse, self.downtime)
            self.typewriter()

        else:
            print("finished type writing")
            self.downtime = 0
            self.loop_toggle()

    def repeat(self, dt):
        self.typewriter.cancel()

        if self.downtime >= 1.5:
            self.play_sound(restart=True)
            self.scroll(self.ids.scroll_layout.children[-1])
        else:
            self.play_sound()

        # Highlight the next character in red
        # t returns a string that tells you how it finished
        t = self.highlight()

        # Will set the downtime according the next occuring character
        # If there is none then the downtime will be set to 2
        try:
            self.set_downtime(self.morse_string[0])
        except IndexError:
            self.downtime = 2
        self.morse_loop = Clock.create_trigger(self.repeat, self.downtime)
        self.morse_loop()

        # Flash light if its active
        if self.ids.morse_light.active is True:
            if self.morse_string[0] == "." or self.morse_string[0] == "-":
                self.set_light_bar(self.downtime)

        # Remove the first character of the string
        self.morse_string = self.morse_string[1:]

        # If the morse string is finished decide if it will loop again
        if len(self.morse_string) == 0:
            if self.ids.loop_toggle.state == "down":
                self.morse_string = self.clipboard
            else:
                self.morse_loop.cancel()
            # make sure the label texts are correctly set
            for label in self.ids.scroll_layout.children:
                label.text = label.hidden_text[:]

    def set_downtime(self, char):

        # The sound generator halves the time [ms.TIME_UNIT] when creating the file so we do it again here
        TIME_UNIT = ms.TIME_UNIT / 2
        if char == '.':
            self.downtime = TIME_UNIT
            self.downtime += TIME_UNIT
        elif char == '-':
            self.downtime = TIME_UNIT * 3
            self.downtime += TIME_UNIT
        elif char == ' ':
            self.downtime = TIME_UNIT * 2
        elif char == '/':
            self.downtime = TIME_UNIT * 2

    def get_string_time(self, string, multiplier=1):
        """Returns the amount of time a string will take to finish playing with default wpm 12"""
        if isinstance(multiplier, int):
            multiplier = self.speed_multi_dict["12"]
        string = string.strip()
        time = 0
        self.time_multiplier(multiplier)
        for char in string:
            self.set_downtime(char)
            time += self.downtime
        if string[-1] != " ":
            time -= (ms.TIME_UNIT / 2)
        self.downtime = 0
        return time

    def time_multiplier(self, multiplier=1):
        """Sets the correct time unit according to the multiplier"""
        ms.TIME_UNIT = .2
        ms.TIME_UNIT = ms.TIME_UNIT / multiplier

    def change_tempo(self, multiplier):
        self.time_multiplier(multiplier)
        self.multiplier = multiplier
        ms.create_sounds()
        if self.clipboard:
            ms.create_wav_file(self.clipboard)
        if self.morse_sound:
            if self.morse_sound.state == "play":
                self.morse_sound.stop()
        self.morse_sound = SoundLoader.load('sounds/morse_code.wav')

        for label in self.ids.scroll_layout.children:
            if "[color" in label.text:
                label.text = label.hidden_text
                self.morse_loop.cancel()
                self.check_loop()
                break
            elif label.text != label.hidden_text and label.text != "":
                for label in self.ids.scroll_layout.children:
                    label.text = ""
                self.play_sound(restart=True)
                break

    def highlight(self):
        next_label = self.ids.scroll_layout.children[-1]
        do_next_label = False
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
                    do_next_label = True
            elif do_next_label:
                next_label = label
                self.scroll(label)
                break

        if len(self.ids.scroll_layout.children) > 0:
            if next_label.id == "morse0" and do_next_label is True:
                return "Got to the end of the loop"
            else:
                next_label.text = "[color=ff0000]" + next_label.hidden_text[0] + \
                    "[/color]" + next_label.hidden_text[1:]
                return "started highlight at index 0 of the label: " + str(next_label.id)
        else:
            print("No scroll labels exist")

    def scroll(self, label):
        self.ids.scroll_view.scroll_to(label)

    def set_light_bar(self, dt):
        if self.ids.morse_light.state == "down":
            if self.flashlight_color == (0, 0, 0, 1):
                self.flashlight_color = (1, 1, 1, 1)
                deactivate = Clock.schedule_once(self.set_light_bar, dt/2)
            elif self.flashlight_color == (1, 1, 1, 1):
                self.flashlight_color = (0, 0, 0, 1)

    def loop_toggle(self):
        check = self.ids.loop_toggle
        self.check_loop = Clock.create_trigger(self.activate_loop, 0)
        if check.state == "normal":
            self.loop = False
            try:
                self.morse_sound.stop()
            except AttributeError:
                pass
        elif check.state == "down":
            try:
                self.scroll(self.ids.scroll_layout.children[-1])
            except IndexError:
                pass
            self.check_loop()

    def activate_loop(self, dt):
        """Waits for the full morse string to appear on screen"""
        if len(self.ids.scroll_layout.children) > 0:
            listx = [True if x.text ==
                     x.hidden_text else False for x in self.ids.scroll_layout.children]
            if False in listx:
                self.check_loop()
            else:
                self.morse_string = self.clipboard
                self.loop = True
                self.morse_loop()
        else:
            self.check_loop()

    def do_proceed(self):
        if self.ids.scroll_layout.children[-1].text == '':
            self.downtime = 0
            self.typewriter = Clock.create_trigger(
                self.type_morse, self.downtime)
            self.typewriter()
        else:
            self.morse_loop()

    def get_wpm(self, multiplier=1) -> float:
        """Gets the words per minute according to the given time multiplier"""
        PARIS = self.create_morse_string("PARIS")
        PARIS_TIME = self.get_string_time(PARIS, multiplier)

        wpm = round(60 / PARIS_TIME, 2)
        self.time_multiplier()
        return wpm

    def play_sound(self, restart=False):
        if self.morse_sound:
            if restart:
                self.morse_sound.stop()
            if self.morse_sound.state != "play":
                self.morse_sound.play()

            if self.sound is False:
                self.morse_sound.volume = 0
            else:
                self.morse_sound.volume = 1
        else:
            print("Couldnt play sound; self.morse_sound is not defined")

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

    def delete_file(self, f="./sounds/morse_code.wav"):
        if os.path.exists(f):
            if self.morse_sound:
                self.morse_sound.unload()
            os.remove(f)
            
        else:
            print("failed to delete: ", f)
            print("file not found")

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        if os.path.exists("./sounds/morse_code.wav"):
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
MainWidget().delete_file()
