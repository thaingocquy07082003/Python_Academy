import pygame
import os
import random
pygame.init()

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
SCREEN = None

IS_FULLSCREEN = False

def setup_display(fullscreen=False):
    global SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, IS_FULLSCREEN
    IS_FULLSCREEN = bool(fullscreen)
    if IS_FULLSCREEN:
        info = pygame.display.Info()
        SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        SCREEN_WIDTH = 1100
        SCREEN_HEIGHT = 600
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    return SCREEN, (SCREEN_WIDTH, SCREEN_HEIGHT)

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "robot fly 1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "robot fly 2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "robot jump 1.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "robot fly 1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "robot fly 2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "trap 1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "trap 2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "trap 3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "trap 4.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "trap 5.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "trap 6.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "planet 2.png")),
        pygame.image.load(os.path.join("Assets/Bird", "planet 2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "cloudy.png"))
CLOUD = pygame.transform.scale(CLOUD, (180, 100))

BG = pygame.image.load(os.path.join("Assets/Other", "road.png"))

FULL_BG = pygame.image.load(os.path.join("Assets/Other", "Background.png"))
FULL_BG = pygame.transform.scale(FULL_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
METEOR_SHOWER = pygame.image.load(os.path.join("Assets/Other", "meteor shower.png"))
METEOR_SHOWER = pygame.transform.scale(METEOR_SHOWER, (SCREEN_WIDTH, SCREEN_HEIGHT))

jump_sound = pygame.mixer.Sound("Assets/sounds/sfx_wing.wav")
jump_sound.set_volume(1.0)
hit_sound = pygame.mixer.Sound("Assets/sounds/sfx_hit.wav")
hit_sound.set_volume(1.0)
gameover_sound = pygame.mixer.Sound("Assets/sounds/sfx_die.wav")
gameover_sound.set_volume(1.0)

DEBUG = False
HITBOX_SCALE = 0.85

SCORE_FONT = pygame.font.Font('freesansbold.ttf', 48)
SMALL_FONT = pygame.font.Font('freesansbold.ttf', 20)


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        # pixel-perfect mask for collisions
        self.mask = pygame.mask.from_surface(self.image)
        # create scaled hitbox
        w, h = self.dino_rect.size
        hw, hh = int(w * HITBOX_SCALE), int(h * HITBOX_SCALE)
        self.hitbox = pygame.Rect(0, 0, hw, hh)
        self.hitbox.center = self.dino_rect.center

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_SPACE] and not self.dino_jump:
            jump_sound.play()
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.mask = pygame.mask.from_surface(self.image)
        # update hitbox
        w, h = self.dino_rect.size
        hw, hh = int(w * HITBOX_SCALE), int(h * HITBOX_SCALE)
        self.hitbox = pygame.Rect(0, 0, hw, hh)
        self.hitbox.center = self.dino_rect.center
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.mask = pygame.mask.from_surface(self.image)
        # update hitbox
        w, h = self.dino_rect.size
        hw, hh = int(w * HITBOX_SCALE), int(h * HITBOX_SCALE)
        self.hitbox = pygame.Rect(0, 0, hw, hh)
        self.hitbox.center = self.dino_rect.center
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
            # mask doesn't change visually but recreate to stay consistent
            self.mask = pygame.mask.from_surface(self.image)
            # update hitbox position when jumping
            if hasattr(self, 'hitbox'):
                self.hitbox.center = self.dino_rect.center
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        if DEBUG:
            # draw bounding rect
            pygame.draw.rect(SCREEN, (0, 255, 0), self.dino_rect, 1)
            # draw hitbox
            if hasattr(self, 'hitbox'):
                pygame.draw.rect(SCREEN, (255, 0, 255), self.hitbox, 1)
            # draw a sample opaque pixel from mask (first found)
            if hasattr(self, 'mask') and self.mask is not None:
                w, h = self.mask.get_size()
                found = False
                for yy in range(h):
                    for xx in range(w):
                        if self.mask.get_at((xx, yy)):
                            pygame.draw.circle(SCREEN, (255, 0, 0), (self.dino_rect.x + xx, self.dino_rect.y + yy), 3)
                            found = True
                            break
                    if found:
                        break


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        # mask for pixel-perfect collision
        try:
            self.mask = pygame.mask.from_surface(self.image[self.type])
        except Exception:
            self.mask = None
        # create scaled hitbox
        w, h = self.rect.size
        hw, hh = int(w * HITBOX_SCALE), int(h * HITBOX_SCALE)
        self.hitbox = pygame.Rect(0, 0, hw, hh)
        self.hitbox.center = self.rect.center

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 0, 255), self.rect, 1)
            # draw hitbox
            if hasattr(self, 'hitbox'):
                pygame.draw.rect(SCREEN, (255, 165, 0), self.hitbox, 1)
            if hasattr(self, 'mask') and self.mask is not None:
                w, h = self.mask.get_size()
                found = False
                for yy in range(h):
                    for xx in range(w):
                        if self.mask.get_at((xx, yy)):
                            pygame.draw.circle(SCREEN, (255, 165, 0), (self.rect.x + xx, self.rect.y + yy), 3)
                            found = True
                            break
                    if found:
                        break


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        current_image = self.image[self.index//5]
        SCREEN.blit(current_image, self.rect)
        # update mask for current bird frame
        try:
            self.mask = pygame.mask.from_surface(current_image)
        except Exception:
            self.mask = None
        # update hitbox
        if hasattr(self, 'hitbox'):
            w, h = self.rect.size
            hw, hh = int(w * HITBOX_SCALE), int(h * HITBOX_SCALE)
            self.hitbox.size = (hw, hh)
            self.hitbox.center = self.rect.center
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    meteor_x = 0
    meteor_y = 0  
    run = True
    clock = pygame.time.Clock()
    # initialize display (start fullscreen)
    setup_display(fullscreen=True)
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("Assets/sounds/theme.mp3")
        pygame.mixer.music.set_volume(0.5)  # âm lượng 0.0 → 1.0
        pygame.mixer.music.play(-1)
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 175
    points = 0
    # use global fonts defined near module top
    global SCORE_FONT, SMALL_FONT
    score_font = SCORE_FONT
    small_font = SMALL_FONT
    obstacles = []
    death_count = 0
    # when a collision occurs we set a pending game-over state and
    # continue running the game for a short delay before showing menu
    game_over_pending = False
    game_over_start = 0
    GAME_OVER_DELAY_MS = 100  # milliseconds to wait after collision

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        # draw the current score centered at the top
        try:
            font_to_use = SCORE_FONT if SCORE_FONT is not None else score_font
        except NameError:
            font_to_use = SCORE_FONT
        text = font_to_use.render(str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        # center top (small vertical offset)
        textRect.center = (SCREEN_WIDTH // 2, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()

        # Vẽ 3 lần để không bị hở
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg + image_width, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg + image_width * 2, y_pos_bg))

        x_pos_bg -= game_speed

        # Reset lại khi x_pos_bg đi hết 1 ảnh nền
        if x_pos_bg <= -image_width:
            x_pos_bg = 0

    def draw_full_background():
        SCREEN.blit(FULL_BG, (0, 0))

    def meteor_background():
        nonlocal meteor_x, meteor_y
        width = METEOR_SHOWER.get_width()

        SCREEN.blit(METEOR_SHOWER, (meteor_x, meteor_y))
        SCREEN.blit(METEOR_SHOWER, (meteor_x + width, meteor_y))
        SCREEN.blit(METEOR_SHOWER, (meteor_x + width * 2, meteor_y))

        meteor_x -= game_speed - 5 

        if meteor_x <= -width:
            meteor_x = 0
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                # toggle debug overlay with D
                if event.key == pygame.K_d:
                    global DEBUG
                    DEBUG = not DEBUG

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        draw_full_background()
        meteor_background()
        background()
        cloud.draw(SCREEN)
        cloud.update()
        player.draw(SCREEN)
        player.update(userInput)

        # only spawn new obstacles if we're not in the post-collision linger
        if (not game_over_pending) and len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            # use pixel-perfect mask collision when available
            collided = False
            if hasattr(player, 'mask') and hasattr(obstacle, 'mask') and obstacle.mask is not None and player.mask is not None:
                offset = (obstacle.rect.x - player.dino_rect.x, obstacle.rect.y - player.dino_rect.y)
                try:
                    if player.mask.overlap(obstacle.mask, offset) is not None:
                        collided = True
                except Exception:
                    collided = False
            else:
                # fallback: use scaled hitboxes if available, otherwise bounding rect
                if hasattr(player, 'hitbox') and hasattr(obstacle, 'hitbox'):
                    if player.hitbox.colliderect(obstacle.hitbox):
                        collided = True
                else:
                    if player.dino_rect.colliderect(obstacle.rect):
                        collided = True

            if collided:
                # start the game-over linger once (don't restart timer on further collisions)
                if not game_over_pending:
                    hit_sound.play()
                    game_over_pending = True
                    game_over_start = pygame.time.get_ticks()
                    death_count += 1

        # if collision occurred, check whether linger time has elapsed
        if game_over_pending:
            elapsed = pygame.time.get_ticks() - game_over_start
            if elapsed >= GAME_OVER_DELAY_MS:
                # now show menu / handle death
                gameover_sound.play()
                pygame.mixer.music.stop()
                menu(death_count)
                return
        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            # use the larger score font for prominence
            # use the global SCORE_FONT
            score_text = SCORE_FONT.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score_text.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score_text, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


if __name__ == '__main__':
    # initialize display and start the menu (start in fullscreen)
    setup_display(fullscreen=True)
    menu(death_count=0)
