import pygame
import random
import os
pygame.init()

man_hinh_x = 800
man_hinh_y = 600
man_hinh = pygame.display.set_mode((man_hinh_x, man_hinh_y))
pygame.display.set_caption("Lái tàu vũ trụ")

tau = pygame.image.load('spaceship_icon.png')
pygame.display.set_icon(tau)
anh_nen = pygame.image.load('space_background.png')

pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
coin_sound = pygame.mixer.Sound('coin.mp3')
coin_sound.set_volume(0.3)
explosion_sound = pygame.mixer.Sound('explosion.wav')
explosion_sound.set_volume(0.05)
bullet_sound = pygame.mixer.Sound('laser.wav')
bullet_sound.set_volume(0.2)

dongxus = []
currentcoinframe = 0
for i in range(9):
    frame = pygame.image.load(f'coin00{i}.png').convert_alpha()
    frame = pygame.transform.scale(frame, (30, 30))
    dongxus.append(frame)

enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

bullet_img = pygame.image.load('bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (15, 40))


lives = 3
game_over = False
tau_x = 375
tau_y = 500
score = 0

highscore_file = "highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0

dong_xu_x = 500
dong_xu_y = 50
def reset_dong_xu():
    global dong_xu_x, dong_xu_y
    dong_xu_x = random.randint(0, man_hinh_x - 30)
    dong_xu_y = -50

enemy_x = random.randint(0, man_hinh_x - 50)
enemy_y = -50
def reset_enemy():
    global enemy_x, enemy_y
    enemy_x = random.randint(0, man_hinh_x - 50)
    enemy_y = -50

font = pygame.font.Font("04B_19.TTF", 36)
tocdo = 300
clock = pygame.time.Clock()
FPS = 60
bg_y1 = 0
bg_y2 = -man_hinh_y
tocdo_nen = 100

COIN_ANIMATION_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(COIN_ANIMATION_EVENT, 120)

running = True

dan_list = []
tocdo_dan = 500

def hien_thi_game_over():
    man_hinh.fill((0, 0, 0))
    text1 = font.render("GAME OVER", True, (255, 0, 0))
    text2 = font.render(f"Score: {score}", True, (255, 255, 255))
    text3 = font.render("R to restart", True, (255, 255, 0))
    text4 = font.render(f"High Score: {high_score}", True, (0, 200, 255))

    text1_rect = text1.get_rect(center=(man_hinh_x / 2, 200))
    text2_rect = text2.get_rect(center=(man_hinh_x / 2, 270))
    text3_rect = text3.get_rect(center=(man_hinh_x / 2, 350))
    text4_rect = text4.get_rect(center=(man_hinh_x / 2, 420))

    man_hinh.blit(text1, text1_rect)
    man_hinh.blit(text2, text2_rect)
    man_hinh.blit(text3, text3_rect)
    man_hinh.blit(text4, text4_rect)
    pygame.display.update()

while running:
    dt = clock.tick(FPS)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == COIN_ANIMATION_EVENT:
            currentcoinframe = (currentcoinframe + 1) % len(dongxus)
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bullet_sound.play()
                dan_rect = bullet_img.get_rect(midbottom=(tau_x + tau.get_width()/2, tau_y))
                dan_list.append(dan_rect)

    keys = pygame.key.get_pressed()
    
    if game_over:
        if keys[pygame.K_r]:
            tau_x, tau_y = 375, 500
            score = 0
            lives = 3
            game_over = False
            reset_dong_xu()
            reset_enemy()
            dan_list.clear()
        else:
            hien_thi_game_over()
            continue

    if keys[pygame.K_LEFT]:
        tau_x -= tocdo * dt
    if keys[pygame.K_RIGHT]:
        tau_x += tocdo * dt
    if keys[pygame.K_UP]:
        tau_y -= tocdo * dt
    if keys[pygame.K_DOWN]:
        tau_y += tocdo * dt

    if tau_x <= 0:
        tau_x = 0
    elif tau_x >= man_hinh_x - tau.get_width():
        tau_x = man_hinh_x - tau.get_width()
    if tau_y <= 0:
        tau_y = 0
    elif tau_y >= man_hinh_y - tau.get_height():
        tau_y = man_hinh_y - tau.get_height()

    dong_xu_y += 200 * dt
    enemy_y += 250 * dt
    if dong_xu_y > man_hinh_y:
        reset_dong_xu()
    if enemy_y > man_hinh_y:
        reset_enemy()

    bg_y1 += tocdo_nen * dt
    bg_y2 += tocdo_nen * dt
    if bg_y1 >= man_hinh_y:
        bg_y1 = bg_y2 - man_hinh_y
    if bg_y2 >= man_hinh_y:
        bg_y2 = bg_y1 - man_hinh_y

    tau_rect = tau.get_rect(topleft=(tau_x, tau_y))
    dong_xu = dongxus[currentcoinframe]
    dong_xu_rect = dong_xu.get_rect(topleft=(dong_xu_x, dong_xu_y))
    enemy_rect = enemy_img.get_rect(topleft=(enemy_x, enemy_y))

    if tau_rect.colliderect(dong_xu_rect):
        score += 1
        coin_sound.play()
        reset_dong_xu()

    if tau_rect.colliderect(enemy_rect):
        lives -= 1
        explosion_sound.play()
        reset_enemy()
        if lives <= 0:
            if score > high_score:
                high_score = score
                with open(highscore_file, "w") as f:
                    f.write(str(high_score))
            game_over = True

    for dan in dan_list[:]:
        dan.y -= tocdo_dan * dt
        if dan.bottom < 0:
            dan_list.remove(dan)
        elif dan.colliderect(enemy_rect):
            explosion_sound.play()
            score += 3
            dan_list.remove(dan)
            reset_enemy()

    man_hinh.blit(anh_nen, (0, bg_y1))
    man_hinh.blit(anh_nen, (0, bg_y2))
    man_hinh.blit(tau, (tau_x, tau_y))
    man_hinh.blit(dong_xu, (dong_xu_x, dong_xu_y))
    man_hinh.blit(enemy_img, (enemy_x, enemy_y))

    for dan in dan_list:
        man_hinh.blit(bullet_img, dan)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    lives_text = font.render(f'Lives: {lives}', True, (255, 100, 100))
    high_text = font.render(f'High: {high_score}', True, (255, 255, 0))
    man_hinh.blit(score_text, (10, 10))
    man_hinh.blit(lives_text, (10, 50))
    man_hinh.blit(high_text, (10, 90))

    pygame.display.update()

pygame.quit()
