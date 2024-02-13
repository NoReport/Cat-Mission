from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector


class Sprite(Widget):
    x, y = 0, 0
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class CatQuest(Widget):
    pass


class CatApp(App):
    def build(self):
        return CatQuest()


if __name__ == "__main__":
    CatApp().run()
