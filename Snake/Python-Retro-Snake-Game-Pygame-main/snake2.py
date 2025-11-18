import pygame, sys, random

pygame.init()

# Fonts
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

# Colors
GREEN = (168, 242, 145)
DARK_GREEN = (43, 51, 24)
HEAD_COLOR = (97, 157, 242)
BODY_COLOR = (52, 68, 247)
BLUE = (90, 142, 224)

# Settings
cell_size = 30
number_of_cells = 25
OFFSET = 75

# Load resources
food_surface = pygame.image.load("Graphics/food.png")
food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size))
eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")
wall_hit_sound = pygame.mixer.Sound("Sounds/wall.mp3")

# Window
screen = pygame.display.set_mode(
    (2 * OFFSET + cell_size * number_of_cells,
     2 * OFFSET + cell_size * number_of_cells)
)
pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

# -----------------------------
# SNAKE STATE (tuple)
# -----------------------------
snake_body = [(6, 9), (5, 9), (4, 9)]
snake_direction = (1, 0)   # dx, dy
add_segment = False

# -----------------------------
# FOOD POSITION
# -----------------------------
def generate_food_position():
    while True:
        pos = (random.randint(0, number_of_cells-1),
               random.randint(0, number_of_cells-1))
        if pos not in snake_body:
            return pos

food_position = generate_food_position()

game_state = "RUNNING"
score = 0

# -----------------------------
# GAME LOGIC
# -----------------------------
def update_snake():
    global snake_body, add_segment
    head_x, head_y = snake_body[0]
    dir_x, dir_y = snake_direction

    new_head = (head_x + dir_x, head_y + dir_y)
    snake_body.insert(0, new_head)

    if add_segment:
        add_segment = False
    else:
        snake_body.pop()


def check_food_collision():
    global food_position, add_segment, score
    if snake_body[0] == food_position:
        food_position = generate_food_position()
        add_segment = True
        score += 1
        eat_sound.play()


def check_edge_collision():
    head_x, head_y = snake_body[0]

    if head_x < 0 or head_x >= number_of_cells:
        game_over()
    if head_y < 0 or head_y >= number_of_cells:
        game_over()


def check_tail_collision():
    if snake_body[0] in snake_body[1:]:
        game_over()


def game_over():
    global snake_body, snake_direction, food_position, game_state, score
    snake_body[:] = [(6, 9), (5, 9), (4, 9)]
    snake_direction = (1, 0)
    food_position = generate_food_position()
    game_state = "STOPPED"
    score = 0
    wall_hit_sound.play()

# -----------------------------
# DRAWING
# -----------------------------
def draw_food():
    x, y = food_position
    rect = pygame.Rect(
        OFFSET + x * cell_size,
        OFFSET + y * cell_size,
        cell_size, cell_size
    )
    screen.blit(food_surface, rect)


def draw_snake():
    head = snake_body[0]
    for x, y in snake_body:
        seg_rect = pygame.Rect(
            OFFSET + x * cell_size,
            OFFSET + y * cell_size,
            cell_size, cell_size
        )   
        if (x, y) == head:
            pygame.draw.rect(screen, HEAD_COLOR, seg_rect, border_radius=7)
        else:
            pygame.draw.rect(screen, BODY_COLOR, seg_rect, border_radius=7)


# -----------------------------
# TIMER EVENT
# -----------------------------
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)


# -----------------------------
# MAIN GAME LOOP
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SNAKE_UPDATE and game_state == "RUNNING":
            update_snake()
            check_food_collision()
            check_edge_collision()
            check_tail_collision()

        if event.type == pygame.KEYDOWN:
            if game_state == "STOPPED":
                game_state = "RUNNING"

            dx, dy = snake_direction

            if event.key == pygame.K_UP and (dx, dy) != (0, 1):
                snake_direction = (0, -1)
            if event.key == pygame.K_DOWN and (dx, dy) != (0, -1):
                snake_direction = (0, 1)
            if event.key == pygame.K_LEFT and (dx, dy) != (1, 0):
                snake_direction = (-1, 0)
            if event.key == pygame.K_RIGHT and (dx, dy) != (-1, 0):
                snake_direction = (1, 0)

    # ---------------------------------------------------
    # DRAW FRAME
    # ---------------------------------------------------
    screen.fill(GREEN)

    pygame.draw.rect(
        screen, DARK_GREEN,
        (OFFSET - 5, OFFSET - 5,
         cell_size * number_of_cells + 10,
         cell_size * number_of_cells + 10),
        5
    )

    draw_food()
    draw_snake()

    title_surface = title_font.render("Snake", True, DARK_GREEN)
    screen.blit(title_surface, (OFFSET - 5, 20))

    score_surface = score_font.render(str(score), True, DARK_GREEN)
    screen.blit(score_surface,
                (OFFSET - 5, OFFSET + cell_size * number_of_cells + 10))

    pygame.display.update()
    clock.tick(60)
