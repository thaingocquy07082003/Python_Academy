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
        return [pygame.transform.scale(img, (img.get_width() * 1.3, img.get_height() * 1.3)) for img in images]
    return pygame.transform.scale(images, (images.get_width() * 1.3, images.get_height() * 1.3))

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
BG = pygame.transform.scale(BG, (BG.get_width() * 1100 // BG.get_height(), 1100))

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
    JUMP_VEL = 36

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL

        # THÊM: vị trí thực tế là float
        self.y_pos = float(self.Y_POS)

        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        # Hitbox
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
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK   # cúi thì y cao hơn (hạ thấp nhân vật)

        self.y_pos = self.Y_POS_DUCK
        
        self.hitbox.center = self.dino_rect.center
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.y_pos = self.Y_POS

        self.hitbox.center = self.dino_rect.center
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        self.y_pos -= self.jump_vel      # lên nhanh hơn vì vel lớn
        self.jump_vel -= 3.9

        self.dino_rect.y = int(self.y_pos)
        self.hitbox.center = self.dino_rect.center
        if self.y_pos >= self.Y_POS:
            self.dino_jump = False
            self.y_pos = float(self.Y_POS)
            self.dino_rect.y = self.Y_POS
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 255, 0), self.dino_rect, 2)
            pygame.draw.rect(SCREEN, (255, 0, 255), self.hitbox, 2)


class Cloud:
    def __init__(self):
        self.x = float(SCREEN_WIDTH + random.randint(800, 1000))
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, speed):
        self.x -= speed
        if self.x < -self.width:
            self.x = float(SCREEN_WIDTH + random.randint(2500, 3000))
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (int(self.x), self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        
        # Float position cho smooth movement
        self.pos_x = float(SCREEN_WIDTH)
        self.pos_y = 0.0
        
        self.rect.x = self.pos_x
        self.rect.y = int(self.pos_y)

        # Tạo hitbox CỐ ĐỊNH size (chỉ tính 1 lần)
        w, h = self.rect.size
        self.hitbox_w = int(w * HITBOX_SCALE)
        self.hitbox_h = int(h * HITBOX_SCALE)
        self.hitbox = pygame.Rect(0, 0, self.hitbox_w, self.hitbox_h)
        self.hitbox.center = self.rect.center

    def update(self, speed,clock):
        delta = clock.get_time() / 40
        self.pos_x -= speed * delta 
        # Làm tròn khi vẽ
        self.rect.x = self.pos_x
        self.rect.y = int(self.pos_y)
        
        # CHỈ cập nhật vị trí hitbox (không tính lại size)
        self.hitbox.center = self.rect.center
        
        return self.pos_x < -self.rect.width

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2)
            pygame.draw.rect(SCREEN, (255, 0, 255), self.hitbox, 2)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.pos_y = 500.0
        self.rect.y = 500


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.pos_y = 475.0
        self.rect.y = 475


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.pos_y = 370.0
        self.rect.y = 370
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        
        current_image = self.image[self.index // 5]
        SCREEN.blit(current_image, self.rect)
        
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
    
    game_speed = 13
    x_pos_bg = 0.0
    y_pos_bg = 15
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
            game_speed += 0.1  
        
        text = SCORE_FONT.render(str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg
        image_width = BG.get_width()

        # Chỉ vẽ 2 lần (đủ để cover màn hình)
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg + image_width, y_pos_bg))

        x_pos_bg -= 10

        if x_pos_bg <= -image_width:
            x_pos_bg = 0.0

    def draw_full_background():
        SCREEN.blit(FULL_BG, (0, 0))

    def meteor_background():
        SCREEN.blit(METEOR_SHOWER, (0, 0))
    
    while run:
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
        
        # Vẽ backgrounds
        draw_full_background()
        meteor_background()
        background()
        
        cloud.draw(SCREEN)
        cloud.update(game_speed * 0.5)  # Cloud chậm hơn
        
        player.draw(SCREEN)
        player.update(userInput)

        # Spawn obstacles
        if (not game_over_pending) and frame_counter >= next_spawn_time:
            rand = random.randint(0, 2)
            frame_counter = 0
            next_spawn_time = 20
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))

        # Update và check collision
        for obstacle in list(obstacles):
            obstacle.draw(SCREEN)
            should_remove = obstacle.update(game_speed,clock)
            
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

        clock.tick(60)  # Giữ 60 FPS
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