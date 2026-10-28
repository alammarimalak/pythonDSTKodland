import math
import pgzrun
WIDTH = 720
HEIGHT = 520
TITLE = "Coin Collector - Learning Reference"
ARENA = Rect(20, 90, 680, 390)
START_BUTTON = Rect(230, 225, 260, 52)
SOUND_BUTTON = Rect(230, 295, 260, 52)
EXIT_BUTTON = Rect(230, 365, 260, 52)
COIN_POSITIONS = [(80, 130), (220, 205), (380, 430),(500, 310), (650, 130)]

class Character:
    def __init__(self, name, position, area, speed):
        self.name = name
        self.actor = Actor(name + "_idle_0", position)
        self.area = area
        self.speed = speed
        self.mode = "idle"
        self.frame = 0
        self.timer = 0

    def move(self, dx, dy, dt):
        old_position = self.actor.pos
        self.actor.x += dx * self.speed * dt
        self.actor.y += dy * self.speed * dt
        half_width = self.actor.width / 2
        half_height = self.actor.height / 2
        self.actor.x = max(self.area.left + half_width,
                           min(self.actor.x, self.area.right - half_width))
        self.actor.y = max(self.area.top + half_height,
                           min(self.actor.y, self.area.bottom - half_height))
        return self.actor.pos != old_position

    def animate(self, moving, dt):
        mode = "walk" if moving else "idle"
        if mode != self.mode:
            self.mode = mode
            self.frame = 0
            self.timer = 0
        self.timer += dt
        interval = 0.18 if moving else 0.35
        if self.timer >= interval:
            self.timer -= interval
            self.frame = (self.frame + 1) % 2
        self.actor.image = f"{self.name}_{self.mode}_{self.frame}"

class Enemy(Character):
    def __init__(self, name, position, area, dx, dy):
        super().__init__(name, position, area, 90)
        self.dx = dx
        self.dy = dy
        self.pause = 0.7

    def update(self, dt):
        moving = False
        if self.pause > 0:
            self.pause = max(0, self.pause - dt)
        else:
            moving = self.move(self.dx, self.dy, dt)
            if self.actor.left <= self.area.left or \
                    self.actor.right >= self.area.right:
                self.dx = -self.dx
                self.pause = 0.7
            if self.actor.top <= self.area.top or \
                    self.actor.bottom >= self.area.bottom:
                self.dy = -self.dy
                self.pause = 0.7
        self.animate(moving, dt)

game_state = "menu"
sound_enabled = True
player = None
enemies = []
coins = []
lives = 3
damage_timer = 0

def start_game():
    global player, enemies, coins, lives, damage_timer, game_state
    player = Character("player", (60, 440), ARENA, 180)
    enemies = [
        Enemy("crab", (150, 205), Rect(110, 150, 220, 110), 1, 0),
        Enemy("monster", (500, 250), Rect(430, 210, 140, 210), 0, 1)]
    coins = []
    for position in COIN_POSITIONS:
        coins.append(Actor("coin", position))
    lives = 3
    damage_timer = 0
    game_state = "playing"

def play_sound(name):
    if sound_enabled:
        if name == "coin":
            sounds.coin.play()
        elif name == "damage":
            sounds.damage.play()

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        music.play("meadow")
    else:
        music.stop()
        sounds.coin.stop()
        sounds.damage.stop()

def update(dt):
    global lives, damage_timer, game_state
    if game_state != "playing":
        return
    dt = min(dt, 0.05)  # Avoid large jumps after dragging the window.
    damage_timer = max(0, damage_timer - dt)
    dx = int(keyboard.d or keyboard.right) - int(keyboard.a or keyboard.left)
    dy = int(keyboard.s or keyboard.down) - int(keyboard.w or keyboard.up)
    if dx and dy:
        dx /= math.sqrt(2)
        dy /= math.sqrt(2)
    moving = player.move(dx, dy, dt)
    player.animate(moving, dt)
    for enemy in enemies:
        enemy.update(dt)
        if damage_timer == 0 and player.actor.colliderect(enemy.actor):
            lives -= 1
            damage_timer = 1.2
            play_sound("damage")
    if lives <= 0:
        game_state = "lost"
        return
    for coin in coins[:]:
        if player.actor.colliderect(coin):
            coins.remove(coin)
            play_sound("coin")
    if not coins:
        game_state = "won"

def draw_button(rect, label):
    screen.draw.filled_rect(rect, "#e3bf63")
    screen.draw.text(label, center=rect.center, fontsize=30, color="#19362c")

def draw():
    screen.fill("#19362c")
    if game_state == "playing":
        screen.draw.filled_rect(ARENA, "#77a65a")
        for enemy in enemies:
            screen.draw.rect(enemy.area, "#496b3d")
        for coin in coins:
            coin.draw()
        for enemy in enemies:
            enemy.actor.draw()
        player.actor.draw()
        if damage_timer > 0:
            screen.draw.circle(player.actor.pos, 25, "white")
        label = f"Lives: {lives}     Coins: {5 - len(coins)}/5"
        screen.draw.text(label, (25, 30), fontsize=32, color="white")
        screen.draw.text("WASD / arrows: move    Esc: menu", (25, 490),
                         fontsize=22, color="white")
    else:
        title = "Coin Collector"
        subtitle = "Collect five coins. Avoid the two patrols."
        if game_state == "won":
            title = "You win!"
            subtitle = "All five coins collected."
        elif game_state == "lost":
            title = "Game over"
            subtitle = "No lives left. Try a fresh round."
        screen.draw.text(title, center=(360, 110), fontsize=60,
                         color="#f3d479")
        screen.draw.text(subtitle, center=(360, 165), fontsize=25,
                         color="white")
        if game_state == "menu":
            draw_button(START_BUTTON, "Start Game")
            label = "Sound: On" if sound_enabled else "Sound: Off"
            draw_button(SOUND_BUTTON, label)
        else:
            draw_button(START_BUTTON, "Back to Menu")
        draw_button(EXIT_BUTTON, "Exit")

def on_mouse_down(pos, button):
    global game_state
    if button != mouse.LEFT or game_state == "playing":
        return
    if EXIT_BUTTON.collidepoint(pos):
        raise SystemExit
    if START_BUTTON.collidepoint(pos):
        if game_state == "menu":
            start_game()
        else:
            game_state = "menu"
    elif game_state == "menu" and SOUND_BUTTON.collidepoint(pos):
        toggle_sound()

def on_key_down(key):
    global game_state
    if key == keys.ESCAPE:
        game_state = "menu"

music.set_volume(0.25)
music.play("meadow")
pgzrun.go()