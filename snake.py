import pygame as pg
import time

pg.init()

w= 12
h= 8
L = 50
pad =5
toppad = 30

screen = pg.display.set_mode((w * L, h * L + toppad))

default_font = pg.font.get_default_font()
font = pg.font.SysFont(default_font, 30)

snake = [(h, 0)] 
direction = "up"
point_pos = (h // 2, w // 2)  

running = True
paused = False  

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

        snake.insert(0, new_head)
        snake.pop()

        # Check if the snake eats the food
        if snake[0] == point_pos:
            snake.append(point_pos)

    # Draw game board
    screen.fill((0, 0, 0))  
    for col in range(w):
        for row in range(h):
            pg.draw.rect(screen, (50, 50, 50), pg.Rect(col * L + pad, row * L + pad + toppad, L - pad, L - pad))

    # Draw snake
    for s in snake:
        row, col = s
        pg.draw.rect(screen, (200, 200, 200), pg.Rect(col * L + pad, row * L + pad + toppad, L - pad, L - pad))

    # Draw food
    pg.draw.rect(screen, (200, 20, 20), pg.Rect(point_pos[1] * L + pad, point_pos[0] * L + pad + toppad, L - pad, L - pad))

    # Display text
    text = font.render('Snake' if not paused else 'Paused', True, (220, 220, 220))
    screen.blit(text, (5, 5))

    pg.display.flip()
    time.sleep(0.2)  # Game speed

pg.quit()
