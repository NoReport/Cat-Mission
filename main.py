from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class Cat(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class CatQuest(Widget):
    cat = ObjectProperty(None)

    def spawn_cat(self):
        self.cat = Cat()
        self.cat.center = self.center
        self.cat.velocity = Vector(4, 0).rotate(randint(0, 360))
        self.add_widget(self.cat)

    def update(self, dt):
        self.cat.move()


class CatApp(App):
    def build(self):
        game = CatQuest()
        game.spawn_cat()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    CatApp().run()
