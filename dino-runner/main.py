import pygame
import os
import random
pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
SCREEN = window
pygame.display.set_caption("Dino Runner")

def scale_x2(images):
    # Dùng cho các list hình ảnh (RUNNING, DUCKING, SMALL_CACTUS, LARGE_CACTUS, BIRD)
    if isinstance(images, list):
        return [pygame.transform.scale(img, (int(img.get_width() * 1.3), int(img.get_height() * 1.3))) for img in images]
    return pygame.transform.scale(images, (int(images.get_width() * 1.3), int(images.get_height() * 1.3)))

RUNNING = scale_x2([pygame.image.load(os.path.join("Assets/Dino", "robot fly 1.png")),
                    pygame.image.load(os.path.join("Assets/Dino", "robot fly 2.png"))])
JUMPING = scale_x2(pygame.image.load(os.path.join("Assets/Dino", "robot jump 1.png")))
DUCKING = scale_x2([pygame.image.load(os.path.join("Assets/Dino", "robot fly 1.png")),
                    pygame.image.load(os.path.join("Assets/Dino", "robot fly 2.png"))])

# Thay đổi Kích thước Chướng ngại vật
SMALL_CACTUS = scale_x2([pygame.image.load(os.path.join("Assets/Cactus", "trap 1.png")),
                         pygame.image.load(os.path.join("Assets/Cactus", "trap 2.png")),
                         pygame.image.load(os.path.join("Assets/Cactus", "trap 3.png"))])
LARGE_CACTUS = scale_x2([pygame.image.load(os.path.join("Assets/Cactus", "trap 4.png")),
                         pygame.image.load(os.path.join("Assets/Cactus", "trap 5.png")),
                         pygame.image.load(os.path.join("Assets/Cactus", "trap 6.png"))])

BIRD = scale_x2([pygame.image.load(os.path.join("Assets/Bird", "planet 2.png")),
                 pygame.image.load(os.path.join("Assets/Bird", "planet 2.png"))])

CLOUD = pygame.image.load(os.path.join("Assets/Other", "cloudy.png"))
CLOUD = pygame.transform.scale(CLOUD, (250, 150))

BG = pygame.image.load(os.path.join("Assets/Other", "road.png"))
# giảm kích thước BG quá lớn — scale theo chiều cao 200 px (bạn có thể điều chỉnh)
BG = pygame.transform.scale(BG, (int(BG.get_width() * (400 / BG.get_height())), 400))

FULL_BG = pygame.image.load(os.path.join("Assets/Other", "Background.png"))
METEOR_SHOWER = pygame.image.load(os.path.join("Assets/Other", "meteor shower.png"))

jump_sound = pygame.mixer.Sound("Assets/sounds/sfx_wing.wav")
jump_sound.set_volume(1.0)
hit_sound = pygame.mixer.Sound("Assets/sounds/sfx_hit.wav")
hit_sound.set_volume(1.0)
gameover_sound = pygame.mixer.Sound("Assets/sounds/sfx_die.wav")
gameover_sound.set_volume(1.0)

DEBUG = False
HITBOX_SCALE = 0.6  # Tăng lên để collision dễ hơn

SCORE_FONT = pygame.font.Font('freesansbold.ttf', 48)
SMALL_FONT = pygame.font.Font('freesansbold.ttf', 20)


class Dinosaur:
    X_POS = 350
    Y_POS = 480
    Y_POS_DUCK = 340
    JUMP_VEL = 35

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL

        # Vị trí thật bằng float
        self.x_pos = float(self.X_POS)
        self.y_pos = float(self.Y_POS)

        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = int(self.x_pos)
        self.dino_rect.y = int(self.y_pos)

        # Hitbox (khoảng bằng)
        w, h = self.dino_rect.size
        hw, hh = int(w * HITBOX_SCALE), int(h * HITBOX_SCALE)
        self.hitbox = pygame.Rect(0, 0, hw, hh)
        self.hitbox.center = self.dino_rect.center

    def update(self, userInput, delta):
        # delta: hệ số tỉ lệ so với 60fps (dt / 16.67)
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump(delta)

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_RETURN] and not self.dino_jump:
            jump_sound.play()
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            self.jump_vel = self.JUMP_VEL   # reset velocity

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
        self.dino_rect.x = int(self.x_pos)
        self.dino_rect.y = int(self.Y_POS_DUCK)   # cúi thì y cao hơn (hạ thấp nhân vật)

        self.y_pos = float(self.Y_POS_DUCK)
        self.hitbox.center = self.dino_rect.center
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = int(self.x_pos)
        self.dino_rect.y = int(self.Y_POS)

        self.y_pos = float(self.Y_POS)
        self.hitbox.center = self.dino_rect.center
        self.step_index += 1

    def jump(self, delta):
        self.image = self.jump_img
        # dùng delta để mượt (sub-pixel)
        self.y_pos -= self.jump_vel * delta
        self.jump_vel -= 3.2 * delta

        # cập nhật rect (ép int cho draw/hitbox)
        self.dino_rect.y = int(self.y_pos)
        self.hitbox.center = self.dino_rect.center
        if self.y_pos >= self.Y_POS:
            self.dino_jump = False
            self.y_pos = float(self.Y_POS)
            self.dino_rect.y = self.Y_POS
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        # vẽ dùng float vị trí x_pos, y_pos cho mượt (pygame chấp nhận)
        SCREEN.blit(self.image, (self.x_pos, self.y_pos))
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 255, 0), self.dino_rect, 2)
            pygame.draw.rect(SCREEN, (255, 0, 255), self.hitbox, 2)


class Cloud:
    def __init__(self):
        self.x = float(SCREEN_WIDTH + random.randint(800, 1000))
        self.y = float(random.randint(50, 100))
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, speed, delta):
        # speed là speed truyền vào (game_speed * 0.5)
        self.x -= speed * delta
        if self.x < -self.width:
            self.x = float(SCREEN_WIDTH + random.randint(2500, 3000))
            self.y = float(random.randint(50, 100))

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image_list, type_index):
        self.image = image_list
        self.type = type_index
        self.current_image = self.image[self.type]
        self.rect = self.current_image.get_rect()

        # Float position cho smooth movement
        self.pos_x = float(SCREEN_WIDTH)
        self.pos_y = 0.0

        # rect dùng float positions (rect stores ints but we'll set using ints when needed)
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        # Tạo hitbox CỐ ĐỊNH size (chỉ tính 1 lần)
        w, h = self.rect.size
        self.hitbox_w = int(w * HITBOX_SCALE)
        self.hitbox_h = int(h * HITBOX_SCALE)
        self.hitbox = pygame.Rect(0, 0, self.hitbox_w, self.hitbox_h)
        self.hitbox.center = self.rect.center

    def update(self, speed, delta):
        # Cập nhật vị trí float
        self.pos_x -= speed * delta

        # cập nhật rect từ float (để blit mượt, cho phép float)
        self.rect.x = int(self.pos_x)  # rect requires ints for hitbox/rect, cast here for consistency
        self.rect.y = int(self.pos_y)

        # CHỈ cập nhật vị trí hitbox (không tính lại size)
        self.hitbox.center = (int(self.rect.centerx), int(self.rect.centery))

        return self.pos_x < -self.rect.width

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], (self.pos_x, self.pos_y))
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2)
            pygame.draw.rect(SCREEN, (255, 0, 255), self.hitbox, 2)


class SmallCactus(Obstacle):
    def __init__(self, image):
        t = random.randint(0, 2)
        super().__init__(image, t)
        self.pos_y = 500.0
        self.rect.y = int(self.pos_y)


class LargeCactus(Obstacle):
    def __init__(self, image):
        t = random.randint(0, 2)
        super().__init__(image, t)
        self.pos_y = 475.0
        self.rect.y = int(self.pos_y)


class Bird(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)
        self.pos_y = 370.0
        self.rect.y = int(self.pos_y)
        self.index = 0

    def update(self, speed, delta):
        return super().update(speed, delta)

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        current_image = self.image[self.index // 5]
        SCREEN.blit(current_image, (self.pos_x, self.pos_y))
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2)
            pygame.draw.rect(SCREEN, (255, 0, 255), self.hitbox, 2)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    next_spawn_time = 15
    frame_counter = 0
    clock = pygame.time.Clock()

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("Assets/sounds/theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    player = Dinosaur()
    cloud = Cloud()

    game_speed = 13.0
    x_pos_bg = 0.0
    y_pos_bg = 380
    points = 0

    obstacles = []
    death_count = 0

    game_over_pending = False
    game_over_start = 0
    GAME_OVER_DELAY_MS = 100

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 3

        text = SCORE_FONT.render(str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, 40)
        SCREEN.blit(text, textRect)

    def background(delta):
        global x_pos_bg
        image_width = BG.get_width()

        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg + image_width, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg + image_width*2, y_pos_bg))
        x_pos_bg -= game_speed * delta

        if x_pos_bg <= -image_width:
            x_pos_bg = 0.0

    def draw_full_background():
        SCREEN.blit(FULL_BG, (0, 0))

    def meteor_background():
        SCREEN.blit(METEOR_SHOWER, (0, 0))

    while run:
        dt = clock.tick(60)  # giữ tối đa 60 FPS, dt là ms elapsed
        delta = dt / 16.67   # hệ số trên chuẩn 60 FPS (16.67 ms)

        frame_counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_d:
                    global DEBUG
                    DEBUG = not DEBUG

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        draw_full_background()
        meteor_background()
        background(delta)

        cloud.draw(SCREEN)
        cloud.update(game_speed * 0.5, delta)  

        # Player
        player.draw(SCREEN)
        player.update(userInput, delta)

        # Spawn obstacles
        if (not game_over_pending) and frame_counter >= next_spawn_time:
            rand = random.randint(0, 2)
            frame_counter = 0
            next_spawn_time = random.randint(18, 30)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))

        # Update và check collision
        for obstacle in list(obstacles):
            obstacle.draw(SCREEN)
            should_remove = obstacle.update(game_speed, delta)

            if should_remove:
                obstacles.remove(obstacle)
                continue

            # Collision detection với hitbox
            if player.hitbox.colliderect(obstacle.hitbox):
                if not game_over_pending:
                    hit_sound.play()
                    game_over_pending = True
                    game_over_start = pygame.time.get_ticks()
                    death_count += 1

        # Check game over
        if game_over_pending:
            elapsed = pygame.time.get_ticks() - game_over_start
            if elapsed >= GAME_OVER_DELAY_MS:
                gameover_sound.play()
                pygame.mixer.music.stop()
                menu(death_count)
                return

        score()
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        else:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score_text = SCORE_FONT.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score_text.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score_text, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 160))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


def scale_cover(image, target_w, target_h):
    img_w, img_h = image.get_size()
    scale = max(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    scaled = pygame.transform.smoothscale(image, (new_w, new_h))
    x = (new_w - target_w) // 2
    y = (new_h - target_h) // 2
    cropped = scaled.subsurface((x, y, target_w, target_h))
    return cropped


if __name__ == '__main__':
    FULL_BG = scale_cover(FULL_BG, SCREEN_WIDTH, SCREEN_HEIGHT)
    METEOR_SHOWER = scale_cover(METEOR_SHOWER, SCREEN_WIDTH, SCREEN_HEIGHT)
    menu(death_count=0)
