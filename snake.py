import pygame as pg
import time
import itertools

pg.init()

# Game settings
w = 12  # Grid width
h = 8   # Grid height
L = 50  # Cell size
pad = 5  # Padding
toppad = 30  # Top padding

# Initialize screen
screen = pg.display.set_mode((w * L, h * L + toppad))

# Font settings
default_font = pg.font.get_default_font()
font = pg.font.SysFont(default_font, 30)

# Snake setup
snake = [(h, 0)]  # Initial snake position
direction = "up"
point_pos = (h // 2, w // 2)  # Initial food position

running = True
paused = False  # Pause flag

def find_farthest_point(snake, grid_w, grid_h):
    """Find the farthest point from the snake's head."""
    head = snake[0]
    max_distance = -1
    best_position = None

    for row, col in itertools.product(range(grid_h), range(grid_w)):
        if (row, col) in snake:
            continue  # Skip positions occupied by the snake
        
        distance = abs(head[0] - row) + abs(head[1] - col)  # Manhattan distance
        if distance > max_distance:
            max_distance = distance
            best_position = (row, col)

    return best_position

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:  
                running = False  
            elif event.key == pg.K_SPACE:  
                paused = not paused  
            elif not paused:  
                if event.key == pg.K_UP and direction != "down":
                    direction = "up"
                elif event.key == pg.K_DOWN and direction != "up":
                    direction = "down"
                elif event.key == pg.K_LEFT and direction != "right":
                    direction = "left"
                elif event.key == pg.K_RIGHT and direction != "left":
                    direction = "right"

    if not paused:
        head_row, head_col = snake[0]

        if direction == "up":
            new_head = (head_row - 1, head_col)
        elif direction == "right":
            new_head = (head_row, head_col + 1)
        elif direction == "down":
            new_head = (head_row + 1, head_col)
        elif direction == "left":
            new_head = (head_row, head_col - 1)

        # Teleport through walls
        new_head = (new_head[0] % h, new_head[1] % w)

        # Check if the snake collides with itself or the walls
        if new_head in snake:
            running = False  # Snake collides with itself, game over
        elif new_head[0] < 0 or new_head[0] >= h or new_head[1] < 0 or new_head[1] >= w:
            running = False  # Snake collides with wall, game over

        snake.insert(0, new_head)
        snake.pop()

        if snake[0] == point_pos:
            snake.append(point_pos)
            point_pos = find_farthest_point(snake, w, h)  # Move apple farthest away

    screen.fill((0, 0, 0))

    for col in range(w):
        for row in range(h):
            pg.draw.rect(screen, (50, 50, 50), pg.Rect(col * L + pad, row * L + pad + toppad, L - pad, L - pad))

    for s in snake:
        row, col = s
        pg.draw.rect(screen, (200, 200, 200), pg.Rect(col * L + pad, row * L + pad + toppad, L - pad, L - pad))

    pg.draw.rect(screen, (200, 20, 20), pg.Rect(point_pos[1] * L + pad, point_pos[0] * L + pad + toppad, L - pad, L - pad))

    text = font.render('Snake' if not paused else 'Paused', True, (220, 220, 220))
    screen.blit(text, (5, 5))

    pg.display.flip()
    time.sleep(0.2)

pg.quit()
