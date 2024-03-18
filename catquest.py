from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.core.audio import SoundLoader


class Cat(Widget):
    direct = 0
    health = NumericProperty(100)
    speed = 180
    soundHurt = ["./src/sounds/sfx/cat/hurt/hurt1.mp3", "./src/sounds/sfx/cat/hurt/hurt2.mp3", "./src/sounds/sfx/cat/hurt/hurt3.mp3"]
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos    


class Enemy(Widget):
    health = NumericProperty(100)
    speed = 200
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class CatQuest(Widget):
    cat = ObjectProperty(None)
    enemy = ObjectProperty(None)
    

    def __init__(self, **kwargs):
        super(CatQuest, self).__init__(**kwargs)
        Clock.schedule_interval(self.playerMove,0)
        Clock.schedule_interval(self.playerAttack, 0.5)
        Clock.schedule_interval(self.playerDash, 0.2)
        Clock.schedule_interval(self.enemyMove, 0)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down = self._on_keyboard_down)
        self._keyboard.bind(on_key_up = self._on_keyboard_up)
        self.keysPressed = set()
        self.mousePressed = set()
        self.cat = Cat()
        self.enemy = Enemy()
        self.cat.pos = self.width / 2 - 25, self.height / 2 - 25
        self.enemy.pos = (Vector(self.cat.pos)+Vector(randint(500, 800), randint(500,800)))
        self.cat.velocity = Vector(0, 0)
        self.enemy.velocity = Vector(4, 4)
        Clock.schedule_interval(self.update, 1)
        self.mousePos = (0, 0)
        with self.canvas:
            self.cat.canvas = Rectangle(source=("./src/sprites/charactorSprite/test.png"), pos=(self.cat.pos), size=(84, 150))
            self.enemy.canvas = Rectangle(pos=(self.enemy.pos), size=(322, 200),source=("./src/sprites/charactorSprite/bob_sprite.png") )


    def update(self, dt):
        self.cat.move()
        self.enemy.move()

        if self.cat.collide_widget(self.enemy):
            x = randint(0,2)
            hurtsonud = SoundLoader.load(self.cat.soundHurt[x])
            hurtsonud.play()
            self.cat.health -= 10
            print("you got damage")
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
        self.cat.pos = 0,0
        self.cat.canvas.pos = self.cat.pos
        self.cat.canvas.source = "./src/sprites/charactorSprite/test.png"
        self.enemy.health = 100
        self.enemy.pos = (Vector(self.cat.pos)+Vector(randint(500, 800), randint(500,800)))
        self.enemy.canvas.pos = self.enemy.pos

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_keyboard_down)
        self._keyboard.unbind(on_key_up = self._on_keyboard_up)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if text == " ":
            self.keysPressed.add("dash")
        else:
            self.keysPressed.add(text)
        
    
    def _on_keyboard_up(self, keyboard, keycode):
        text = keycode[1]
        if text == "spacebar":
            self.keysPressed.remove("dash")
        elif text in self.keysPressed:
            self.keysPressed.remove(text)
            
    
    def on_touch_down(self, touch):
        self.mousePos = touch.pos
        self.mousePressed.add(touch.button)
    
    def on_touch_up(self, touch):
        button = touch.button
        if button in self.mousePressed:
            self.mousePressed.remove(button)

    def on_touch_move(self, touch):
        self.cat.velocity = Vector(touch.x - self.cat.center_x, touch.y - self.cat.center_y)

    def playerMove(self, trickSpeed):
        newPosX = self.cat.canvas.pos[0]
        newPosY = self.cat.canvas.pos[1]
        step_size = self.cat.speed * trickSpeed
        if "w" in self.keysPressed:
            if newPosY+step_size <= 900:
                newPosY += step_size
        if "s" in self.keysPressed:
            if newPosY-step_size >= 0:
                newPosY -= step_size
        if "a" in self.keysPressed:
            if self.cat.direct == 0:
                self.cat.direct = 1
                self.cat.canvas.source = "./src/sprites/charactorSprite/testLeft.png"
            if newPosX-step_size >=0 :
                newPosX -= step_size
        if "d" in self.keysPressed:
            if self.cat.direct == 1:
                self.cat.direct = 0
                self.cat.canvas.source = "./src/sprites/charactorSprite/test.png"
            if newPosX+step_size < 1850:
                newPosX += step_size
        self.cat.pos = (newPosX, newPosY)
        self.cat.canvas.pos = self.cat.pos

    def playerDash(self, trickSpeed):
        if "dash" in self.keysPressed:
            newPosX = self.cat.canvas.pos[0]
            newPosY = self.cat.canvas.pos[1]
            step_size = (self.cat.speed * trickSpeed) + 50
            if "w" in self.keysPressed:
                if newPosY+step_size <= 900:
                    newPosY += step_size
            if "s" in self.keysPressed:
                if newPosY-step_size >= 0:
                    newPosY -= step_size
            if "a" in self.keysPressed:
                if self.cat.direct == 0:
                    self.cat.direct = 1
                    self.cat.canvas.source = "./src/sprites/charactorSprite/testLeft.png"
                if newPosX-step_size >=0 :
                    newPosX -= step_size
            if "d" in self.keysPressed:
                if self.cat.direct == 1:
                    self.cat.direct = 0
                    self.cat.canvas.source = "./src/sprites/charactorSprite/test.png"
                if newPosX+step_size < 1850:
                    newPosX += step_size
            self.cat.pos = (newPosX, newPosY)
            self.cat.canvas.pos = self.cat.pos
            
    def playerAttack(self, trickSpeed):
        if "left" in self.mousePressed:
            direction = Vector(*self.mousePos) - Vector(*self.cat.pos)
            direction = direction.normalize()
            hitbox_range = 150
            hitbox_pos = (self.cat.pos[0] + direction.x * hitbox_range, self.cat.pos[1])
            hitbox_size = (abs(direction.x) * hitbox_range, self.cat.height)
            with self.canvas:
                self.hitbox = Rectangle(pos=hitbox_pos, size=hitbox_size)

            Clock.schedule_once(self.remove_hitbox, 0.2)
            
            if self.cat.direct == 0:
                if direction.x > 0 and abs(direction.y) < 0.2:
                    if 0 < direction.x * (self.enemy.x - self.cat.x) < hitbox_range:
                        self.enemy.health -= 10
                        print("attacked")
            else:
                if direction.x < 0 and abs(direction.y) < 0.2:
                    if 0 > direction.x * (self.enemy.x - self.cat.x) > -hitbox_range:
                        self.enemy.health -= 10
                        print("attacked")

        if self.enemy.health <= 0:
            print("you win")
            self.reset_game()

    def remove_hitbox(self, dt):
        # Remove the hitbox from the canvas
        self.canvas.remove(self.hitbox)
        
    
    def enemyMove(self, trickSpeed):
        newPosX = self.enemy.canvas.pos[0]
        newPosY = self.enemy.canvas.pos[1]
        step_size = self.enemy.speed * trickSpeed
        if newPosX < self.cat.pos[0]:
            newPosX += step_size
        elif newPosX > self.cat.pos[0]:
            newPosX -= step_size
        if newPosY < self.cat.pos[1]:
            newPosY += step_size
        elif newPosY > self.cat.pos[1]:
            newPosY -= step_size
        self.enemy.pos = (newPosX, newPosY)
        self.enemy.canvas.pos = self.enemy.pos

class CatApp(App):
    def build(self):
        self.root = CatQuest()
        Clock.schedule_once(self.start_game, 2)  # Delay the game start by 2 seconds
        bgMusic = SoundLoader.load("./src/sounds/bgSound/BADDAY_Minecraft Beat.wav")
        if bgMusic:
            bgMusic.play()
        return self.root

    def start_game(self, dt):
        print("Starting the game!")
        self.root.update(0)  # Start the game update loop


if __name__ == "__main__":
    CatApp().run()
