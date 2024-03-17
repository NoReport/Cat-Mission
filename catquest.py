from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class Cat(Widget):
    health = NumericProperty(100)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos    


class Enemy(Widget):
    health = NumericProperty(50)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class CatQuest(Widget):
    cat = ObjectProperty(None)
    enemy = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CatQuest, self).__init__(**kwargs)
        self.cat = Cat()
        self.enemy = Enemy()
        self.cat.pos = self.width / 2 - 25, self.height / 2 - 25
        self.enemy.pos = randint(0, self.width - 50), randint(0, self.height - 50)
        self.cat.velocity = Vector(0, 0)
        self.enemy.velocity = Vector(4, 4)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        self.cat.move()
        self.enemy.move()

        if self.cat.collide_widget(self.enemy):
            self.cat.health -= 10

        if self.cat.health <= 0:
            print("You have been defeated by the enemy!")
            self.reset_game()

        if self.cat.right > self.width:
            self.cat.right = self.width
        if self.cat.x < 0:
            self.cat.x = 0
        if self.cat.top > self.height:
            self.cat.top = self.height
        if self.cat.y < 0:
            self.cat.y = 0

        if self.enemy.right > self.width or self.enemy.x < 0:
            self.enemy.velocity.x *= -1
        if self.enemy.top > self.height or self.enemy.y < 0:
            self.enemy.velocity.y *= -1 

    def reset_game(self):
        self.cat.health = 100
        self.cat.pos = self.width / 2 - 25, self.height / 2 - 25
        self.enemy.pos = randint(0, self.width - 50), randint(0, self.height - 50)

    def on_touch_move(self, touch):
        self.cat.velocity = Vector(touch.x - self.cat.center_x, touch.y - self.cat.center_y)


class CatApp(App):
    def build(self):
        self.root = CatQuest()
        Clock.schedule_once(self.start_game, 2)  # Delay the game start by 2 seconds
        return self.root

    def start_game(self, dt):
        print("Starting the game!")
        self.root.update(0)  # Start the game update loop


if __name__ == "__main__":
    CatApp().run()
