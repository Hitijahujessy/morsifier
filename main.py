import os

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty  # type : ignore
from kivy.uix.widget import Widget

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
root_widget = Builder.load_file('app.kv')


# threading multiprocessing

class MainWidget(Widget):
    string = ObjectProperty()
    loop = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.typewriter = Clock.create_trigger(self.translate_to_morse, .25)
        self.morse_loop = Clock.create_trigger(self.repeat, .25)

    def translate_to_morse(self, dt):
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




class MorsifierApp(App):
    MainWidget = MainWidget()

    def build(self):
        return self.MainWidget


MorsifierApp().run()
