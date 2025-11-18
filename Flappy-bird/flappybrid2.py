import pygame
from sys import exit
import random

pygame.init()


GAME_WIDTH = 1920
GAME_HEIGHT = 1080
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Windifybird")
clock = pygame.time.Clock()

pipe_width = 100
pipe_height = 800
bird_width = 80
bird_height = 80

gravity = 0.4
velocity_x = -5
velocity_y = 0
score = 0
game_over = False

sfx_point = pygame.mixer.Sound("sfx_point.wav")
sfx_hit = pygame.mixer.Sound("sfx_hit.wav")
sfx_die = pygame.mixer.Sound("sfx_die.wav")
sfx_wing = pygame.mixer.Sound("sfx_wing.wav")


background_image = pygame.image.load("futureacademybackground.jpg")
background_image = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))


bird_frames = [
    pygame.image.load("Robot.png"),
    pygame.image.load("Robot3.png"),
    pygame.image.load("Robot2.png")
]
bird_frames = [pygame.transform.scale(frame, (bird_width, bird_height)) for frame in bird_frames]
bird_frame_index = 0

top_pipe_image = pygame.image.load("cottren.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bottom_pipe_image = pygame.image.load("cotduoi.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width, pipe_height))

game_font = pygame.font.Font("04B_19.TTF", 36)


bird = {"x": GAME_WIDTH / 4, "y": GAME_HEIGHT / 2, "w": bird_width, "h": bird_height, "img": bird_frames[0]}
pipes = []

def reset_game():
    global pipes, bird, velocity_y, score, game_over, bird_frame_index
    pipes.clear()
    bird["x"] = GAME_WIDTH / 4
    bird["y"] = GAME_HEIGHT / 2
    velocity_y = 0
    score = 0
    game_over = False
    bird_frame_index = 0
    bird["img"] = bird_frames[0]


def create_pipes():
    random_pipe_y = -pipe_height / 4 - random.random() * (pipe_height / 2)
    opening_space = GAME_HEIGHT / 4

    top_pipe = {"x": GAME_WIDTH, "y": random_pipe_y, "w": pipe_width, "h": pipe_height, "img": top_pipe_image, "passed": False}
    bottom_pipe = {"x": GAME_WIDTH, "y": top_pipe["y"] + pipe_height + opening_space, "w": pipe_width, "h": pipe_height, "img": bottom_pipe_image, "passed": False}

    pipes.append(top_pipe)
    pipes.append(bottom_pipe)

def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    bird["y"] += velocity_y
    bird["y"] = max(bird["y"], 0)

    if bird["y"] > GAME_HEIGHT:
        sfx_die.play()
        game_over = True
        return

    cut_top = 25
    hitbox_height = bird["h"] - cut_top
    bird_hitbox = pygame.Rect(bird["x"], bird["y"] + cut_top, bird["w"], hitbox_height)

    for pipe in pipes:
        pipe["x"] += velocity_x
        pipe_rect = pygame.Rect(pipe["x"], pipe["y"], pipe["w"], pipe["h"])
        if bird_hitbox.colliderect(pipe_rect):
            sfx_hit.play()
            game_over = True
            return

        if not pipe["passed"] and bird["x"] > pipe["x"] + pipe["w"]:
            score += 0.5
            sfx_point.play()
            pipe["passed"] = True

    while len(pipes) > 0 and pipes[0]["x"] < -pipe_width:
        pipes.pop(0)

def draw():
    window.blit(background_image, (0, 0))
    for pipe in pipes:
        window.blit(pipe["img"], (pipe["x"], pipe["y"])) 

    rotated_bird = pygame.transform.rotate(bird["img"], -velocity_y * 0.5)
    window.blit(rotated_bird, (bird["x"], bird["y"]))

    if game_over:
        text_str = f"GAME OVER  |  SCORE: {int(score)}  |  Press SPACE to Restart"
    else:
        text_str = f"SCORE: {int(score)}"
    text_render = game_font.render(text_str, True, (255, 255, 255))
    score_rect = text_render.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT / 8))
    window.blit(text_render, score_rect)

CREATE_PIPE_EVENT = pygame.USEREVENT + 0
BIRD_ANIM_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_PIPE_EVENT, 1500)
pygame.time.set_timer(BIRD_ANIM_EVENT, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == CREATE_PIPE_EVENT and not game_over:
            create_pipes()

        if event.type == BIRD_ANIM_EVENT and not game_over:
            bird_frame_index = (bird_frame_index + 1) % len(bird_frames)
            bird["img"] = bird_frames[bird_frame_index]

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                if not game_over:
                    sfx_wing.play()
                    velocity_y = -8
                else:
                    reset_game()

    if not game_over:
        move()

    draw()
    pygame.display.update()
    clock.tick(60)
