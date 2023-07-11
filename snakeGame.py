# Snake game!

# Written on 25/8/2017
# Based on udemy training videos

# TO DO:
# 1. Menus
# 2. Sounds
# 3. Settings - sounds on/off, FPS setting, etc
# 4. Make blocks images
# 5. Convert script to executable - pyinstaller
#

import pygame   # graphics, vectors, sounds, interrupts - usually used for 2D games
import sys      # System
import random   # need random positions for food
import time     # need to sleep

# can also put these on one line, e.g.
# import pygame, sys, random, time

check_errors = pygame.init()  # Should return (6,0)    (tasks, errors)
if check_errors[1] > 0:
    print ("Error initialising : {0} errors".format(check_errors[1]))
    sys.exit(-1)
else:
    print("PyGame successfully initialised")

# Game vars
width = 720
height = 460
gameTitle = "Snake game!"
snakePos = [100,50]
snakeBody = [[100,50], [90,50], [80,50]]
score = 0
foodScore = 10
snakeSize = 10
foodSizeX = 10
foodSizeY = 10

snakeMovement = 10

# Colours!
red = pygame.Color(255, 0, 0)             # game over
green = pygame.Color(0, 255, 0)           # Snake
blue = pygame.Color(0, 0, 255)
black = pygame.Color(0, 0, 0)             # Score
white = pygame.Color(255, 255, 255)       # BG
brown = pygame.Color(165, 42, 42)         # Food

snakeColour = green
foodColour = brown
scoreColour = black

# Play surface
playSurface = pygame.display.set_mode((width, height))  # double brackets creates tuple
pygame.display.set_caption(gameTitle)

# Frames per second controller
fpsController = pygame.time.Clock()

foodPos = [200, 200]  #[random.randrange(1, 72) * 10,random.randrange(1, 46) * 2]
foodSpawn = True
dirLeft = 0
dirRight = 1
dirUp = 2
dirDown = 3

direction = dirRight
changeTo = direction

def exitGame():
    pygame.quit()       # Exit pygame
    sys.exit(0)         # Exit console

# Game Over function
def gameOver():
    myFont = pygame.font.SysFont('monaco',72)
    gameOverSurface = myFont.render('Game Over!', True, red)
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.midtop = (width / 2, 10)
    playSurface.blit(gameOverSurface, gameOverRect)
    showScore(0)
    pygame.display.flip()
    time.sleep(4)
    exitGame()


def showScore(choice = 1):
    scoreFont = pygame.font.SysFont('monaco',24)
    scoreSurface = scoreFont.render('Score : {0}'.format(score), True, scoreColour)
    scoreRect = scoreSurface.get_rect()

    if choice == 1:
        scoreRect.midtop = (80, 10)
    else:
        scoreRect.midtop = (width / 2, 120)

    playSurface.blit(scoreSurface, scoreRect)


def showDebug():
    debugFont = pygame.font.SysFont('monaco',24)
    debugSurface = debugFont.render('Direction:{0}, ChangeTo:{1}, snakePos[0]:{2}, snakePos[1]:{3}, foodPos[0]:{4}, foodPos[1]:{5}'.format(direction, changeTo, snakePos[0], snakePos[1], foodPos[0], foodPos[1]), True, scoreColour)
    debugRect = debugSurface.get_rect()
    debugRect.midtop = (300, 10)
    playSurface.blit(debugSurface, debugRect)

##############
# Main loop
##############

while True:

    # Check keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeTo = dirRight
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeTo = dirLeft
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeTo = dirUp
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeTo = dirDown
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))


    # Check direction change
    if changeTo == dirRight and not direction == dirLeft:
        direction = dirRight
    if changeTo == dirLeft and not direction == dirRight:
        direction = dirLeft
    if changeTo == dirUp and not direction == dirDown:
        direction = dirUp
    if changeTo == dirDown and not direction == dirUp:
        direction = dirDown

    # Move snake
    if direction == dirRight:
        snakePos[0] += snakeMovement
    if direction == dirLeft:
        snakePos[0] -= snakeMovement
    if direction == dirUp:
        snakePos[1] -= snakeMovement
    if direction == dirDown:
        snakePos[1] += snakeMovement

    # Snake Body
    snakeBody.insert(0, list(snakePos))

    # Have we eaten the food?
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        foodSpawn = False
        score += foodScore
        foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    else:
        snakeBody.pop()

    playSurface.fill(white)

    # Draw snake
    for pos in snakeBody:
        pygame.draw.rect(playSurface, snakeColour, pygame.Rect(pos[0], pos[1], snakeSize, snakeSize))

    # Draw food
    pygame.draw.rect(playSurface, foodColour, pygame.Rect(foodPos[0], foodPos[1], foodSizeX, foodSizeY))

    # Check boundary
    if snakePos[0] > width - snakeSize or snakePos[0] < 0:
        gameOver()

    if snakePos[1] > height - snakeSize or snakePos[1] < 0:
        gameOver()

    # Has the head hit the body?
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()

    # Draw
    showScore(2)
    #showDebug()
    pygame.display.flip()
    fpsController.tick(25)

