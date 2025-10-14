import pygame
from copy import deepcopy
from random import choice, randrange

W, H = 10, 20
TILE = int(48 * 0.8)
GAME_RES = W * TILE, H * TILE
pygame.init()
infoObject = pygame.display.Info()
RES = infoObject.current_w - 10, infoObject.current_h - 55  
FPS = 60

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000
fast_drop_speed = 1

bg = pygame.image.load('./img/bg.jpg').convert()
game_bg = pygame.image.load('./img/bg2.jpg').convert()
gameover_img = pygame.image.load('./img/gameover.jpg').convert()
gameover_img = pygame.transform.scale(gameover_img, GAME_RES)

main_font = pygame.font.Font('./font/font.ttf', int(65 * 0.8))
font = pygame.font.Font('./font/font.ttf', int(55 * 0.8))

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))
title_level = font.render('level:', True, pygame.Color('cyan'))

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

def generate_piece():
    return deepcopy(choice(figures)), get_color()

figure, color = generate_piece()
next_queue = [generate_piece() for _ in range(4)]

score, lines, level = 0, 0, 1
scores = {0: 0, 1: 10, 2: 30, 3: 70, 4: 100}
level_threshold = 100

# Game over animation variables
game_over = False
gameover_y = -GAME_RES[1]  
gameover_speed = 20  
waiting_for_enter = False

# Screen shake effect variables
shake_intensity = 0
shake_duration = 0
shake_offset_x = 0
shake_offset_y = 0  


def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    record = get_record()
    dx, rotate = 0, False
    # Screen shake effect
    if shake_duration > 0:
        shake_offset_x = randrange(-shake_intensity, shake_intensity + 1)
        shake_offset_y = randrange(-shake_intensity, shake_intensity + 1)
        shake_duration -= 1
        if shake_duration <= 0:
            shake_intensity = 0
            shake_offset_x = 0
            shake_offset_y = 0
    else:
        shake_offset_x = 0
        shake_offset_y = 0

    bg_full = pygame.transform.scale(bg, RES)
    sc.blit(bg_full, (0, 0))
    sc.blit(game_sc, (int(700 * 0.8) + shake_offset_x, int(20 * 0.8) + shake_offset_y))
    game_sc.blit(game_bg, (0, 0))
    # delay for full lines
    for i in range(lines):
        pygame.time.wait(10)
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                for _ in range(2):
                    figure_old = deepcopy(figure)
                    for i in range(4):
                        figure[i].y += 1
                        if not check_borders():
                            for i in range(4):
                                field[figure_old[i].y][figure_old[i].x] = color
                            figure, color = next_queue.pop(0)
                            next_queue.append(generate_piece())
                            anim_limit = 2000
                            break
                    else:
                        continue
                    break
            elif event.key == pygame.K_SPACE:
                shake_intensity = 2
                shake_duration = 30
                
                while True:
                    figure_old = deepcopy(figure)
                    for i in range(4):
                        figure[i].y += 1
                        if not check_borders():
                            for i in range(4):
                                field[figure_old[i].y][figure_old[i].x] = color
                            figure, color = next_queue.pop(0)
                            next_queue.append(generate_piece())
                            anim_limit = 2000
                            break
                    else:
                        continue
                    break
            elif event.key == pygame.K_UP:
                rotate = True
            elif event.key == pygame.K_RETURN and waiting_for_enter:
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score, lines, level = 0, 0, 1
                figure, color = generate_piece()
                next_queue = [generate_piece() for _ in range(4)]
                game_over = False
                gameover_y = -GAME_RES[1]
                waiting_for_enter = False
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_queue.pop(0)
                next_queue.append(generate_piece())
                anim_limit = 2000  # Reset speed 
                break
    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
    # compute score
    score += scores[lines]
    
    # check level up
    if score >= level * level_threshold:
        level += 1
        anim_speed += 2  # Tăng tốc độ khi lên level
        anim_limit = max(50, anim_limit - 100)  
    # draw grid
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    # draw next figures (3-piece queue)
    preview_base_x = int(1280 * 0.8)
    preview_base_y = int(185 * 0.8)
    preview_spacing = int(200 * 0.8)
    for idx, (nfig, ncol) in enumerate(next_queue):
        offset_y = preview_base_y + idx * preview_spacing
        for i in range(4):
            figure_rect.x = nfig[i].x * TILE + preview_base_x
            figure_rect.y = nfig[i].y * TILE + offset_y
            pygame.draw.rect(sc, ncol, figure_rect)
    # draw titles
    sc.blit(title_tetris, (int(1400 * 0.8), int(0 * 0.8)))
    sc.blit(title_score, (int(240 * 0.8), int(770 * 0.8)))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (int(300 * 0.8), int(860 * 0.8)))
    sc.blit(title_record, (int(230 * 0.8), int(600 * 0.8)))
    sc.blit(font.render(record, True, pygame.Color('gold')), (int(250 * 0.8), int(690 * 0.8)))
    sc.blit(title_level, (int(240 * 0.8), int(450 * 0.8)))
    sc.blit(font.render(str(level), True, pygame.Color('cyan')), (int(310 * 0.8), int(530 * 0.8)))
    # game over
    for i in range(W):
        if field[0][i] and not game_over:
            set_record(record, score)
            game_over = True
            gameover_y = -GAME_RES[1]  
    if game_over:
        if not waiting_for_enter:
            gameover_y += gameover_speed
            game_sc.blit(gameover_img, (0, gameover_y))
            if gameover_y >= 0:
                waiting_for_enter = True
        else:
            game_sc.blit(gameover_img, (0, gameover_y))
    pygame.display.flip()
    clock.tick(FPS)