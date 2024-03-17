from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.graphics import Rectangle
from kivy.core.window import Window


class Cat(Widget):
    health = NumericProperty(100)
    speed = 180
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
        Clock.schedule_interval(self.playerMove,0)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down = self._on_keyboard_down)
        self._keyboard.bind(on_key_up = self._on_keyboard_up)
        self.keysPressed = set()
        self.cat = Cat()
        self.enemy = Enemy()
        self.cat.pos = self.width / 2 - 25, self.height / 2 - 25
        self.enemy.pos = randint(0, self.width - 50), randint(0, self.height - 50)
        self.cat.velocity = Vector(0, 0)
        self.enemy.velocity = Vector(4, 4)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        with self.canvas:
            self.cat.canvas = Rectangle(source=("./src/sprites/charactorSprite/test.png"), pos=(self.cat.pos), size=(self.cat.width, self.cat.height))
            self.enemy.canvas = Rectangle(pos=(self.enemy.pos), size=(self.enemy.width, self.enemy.height), )



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

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_keyboard_down)
        self._keyboard.unbind(on_key_up = self._on_keyboard_up)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(text)
        

    
    def _on_keyboard_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)
            pass

    def on_touch_move(self, touch):
        self.cat.velocity = Vector(touch.x - self.cat.center_x, touch.y - self.cat.center_y)

    def playerMove(self, trickSpeed):
        newPosX = self.cat.canvas.pos[0]
        newPosY = self.cat.canvas.pos[1]
        step_size = self.cat.speed * trickSpeed
        if "w" in self.keysPressed:
            newPosY += step_size
        if "s" in self.keysPressed:
            newPosY -= step_size
        if "a" in self.keysPressed:
            newPosX -= step_size
        if "d" in self.keysPressed:
            newPosX += step_size
        self.cat.pos = (newPosX, newPosY)
        self.cat.canvas.pos = self.cat.pos


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
