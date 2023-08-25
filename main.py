import random

import pygame

backgroundColour = (0, 0, 0)
width = 40
height = 40
rows = 10
columns = 15
FPS = 2

pygame.init()
screen = pygame.display.set_mode((rows * width, columns * height))

pygame.display.set_caption('Tetris')
screen.fill(backgroundColour)
clock = pygame.time.Clock()

rec = [pygame.Rect(x * width, y * height, width, height) for x in range(rows) for y in range(columns)]
[pygame.draw.rect(screen, (40, 40, 40), rectangle, 2) for rectangle in rec]
pygame.display.flip()
clock.tick(200)

def getRandomPosition():
    curr_x_position = random.randint(0, 360)
    curr_x_position = curr_x_position - (curr_x_position % 40)
    return (curr_x_position, 0)


running = True
(curr_x_position, curr_y_position) = getRandomPosition()
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:

            if keys[pygame.K_LEFT] and curr_x_position > 0:
                curr_x_position = curr_x_position - width
            if keys[pygame.K_RIGHT] and curr_x_position < 360:
                curr_x_position = curr_x_position + width
            if keys[pygame.K_UP] and curr_y_position > 0:
                curr_y_position = curr_y_position - height
            if keys[pygame.K_DOWN] and curr_y_position < 560:
                curr_y_position = curr_y_position + height
            screen.fill((0, 0, 0))

    if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]) and (not keys[pygame.K_UP]) and (not keys[pygame.K_DOWN]) and curr_y_position <= 560:
        curr_y_position = curr_y_position + height
        screen.fill((0, 0, 0))
    if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]) and (not keys[pygame.K_UP]) and (not keys[pygame.K_DOWN]) and curr_y_position > 560:
        (curr_x_position, curr_y_position) = getRandomPosition()
        pygame.draw.rect(screen, (255, 0, 0), (curr_x_position, curr_y_position, width, height))

    rec = [pygame.Rect(x * width, y * height, width, height) for x in range(rows) for y in range(columns)]
    [pygame.draw.rect(screen, (40, 40, 40), rectangle, 2) for rectangle in rec]

    pygame.draw.rect(screen, (255, 0, 0), (curr_x_position, curr_y_position, width, height))

    pygame.display.flip()
    clock.tick(FPS)


