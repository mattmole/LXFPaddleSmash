# Import the pygame library and initialise the game engine
import pygame
from Ball import Ball
from Paddle import Paddle
from LaserBullet import LaserBullet
from Brick import *
import Constants
import math
from ParseConfig import ParseLevelConfig
from rich import print
import os

a = ParseLevelConfig('levels/level1.conf')

pygame.init()

# Define whether to use full screen or not
fullScreen = False

# Variables to define sizes of the window and the paddles
screenRes = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screenWidth = pygame.display.Info().current_w / 2
screenHeight = pygame.display.Info().current_h - 100
if fullScreen == True:
    # Grab the resolution of the display if needed
    screenWidth, screenHeight = pygame.display.Info(
    ).current_w, pygame.display.Info().current_h

# Variable to define frame rate
frameRate = 60

# Open a new window and set to full screen if required
size = (screenWidth, screenHeight)
if fullScreen == True:
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)

gameTitle = "Paddle Smash"

# Set the caption of the Window
window = pygame.display
window.set_caption(gameTitle)

# Calculate some sizes for objects based on percentages of the window size
ballRadius = (screenWidth / screenHeight) * 50
paddleWidth = screenWidth / 4
paddleHeight = paddleWidth / 6
brickRenderWidth = screenWidth - 4 * ballRadius
brickRenderHeight = screenHeight / 2
brickHeight = screenHeight / 30
paddleSpeed = screenHeight / 150
ballSpeed = screenHeight / 150
laserHeight = screenHeight / 40
laserWidth = screenHeight / 120
laserBulletSpeed = screenHeight / 150

# Variable to store the points per collision
collisionPoints = 10

# Add a font to be used to show the score and any other text
font = pygame.font.SysFont(None, int(screenHeight / 20))

# Create an object for the main ball
ball = Ball(ballRadius, ballRadius, screenWidth /
            4, screenHeight / 2, ballSpeed)

paddle = Paddle(paddleWidth, paddleHeight, 0, screenHeight - 100, paddleSpeed)
paddle2 = Paddle(paddleWidth, paddleHeight,
                 screenWidth - 400, screenHeight - 100, paddleSpeed)

# Create groups to store the balls
ballGroup = pygame.sprite.Group()
ballGroup.add(ball)
secondaryBallGroup = pygame.sprite.Group()

# Create a group to store the paddles
paddleGroup = pygame.sprite.Group()
paddleGroup.add(paddle)

# Create a group to store the bricks
brickGroup = pygame.sprite.Group()
secondaryBrickGroup = pygame.sprite.Group()

# Create a group to store the laser "bullets"
laserBulletGroup = pygame.sprite.Group()
createLaserBullets = False
laserTimeCounter = 0

# The while loop will carry on until the user exits the game (e.g. clicks the close button or presses the escape key).
carryOn = True

# Frame counter variable to use to determine when each 10s or 60s period has passed
frameCount = 0

# Variables to store the score
gameScore = 0

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Load the config file
levelConfig = ParseLevelConfig("levels//level1.conf")
bgMusicFile = levelConfig.levelConfig["options"]["audio"]
bgFile = levelConfig.levelConfig["options"]["background"]

# Load the music file
if bgMusicFile != None and os.path.isfile(bgMusicFile):
    bgMusic = pygame.mixer.music.load(bgMusicFile)
    pygame.mixer.music.play(-1)

# Load the background image
bgImage = None
if bgFile != None and os.path.isfile(bgFile):
    bgImage = pygame.image.load(bgFile)
    rect = bgImage.get_rect()
    bgImage = pygame.transform.scale(bgImage, (screenWidth, screenHeight))

# Grab the number of lives from the config
numLives = levelConfig.levelConfig["options"]["lives"]
print(numLives)

# Grab the number of seconds countdown from the config
countdownTime = levelConfig.levelConfig["options"]["countdown"]

# Grab the number of seconds the power-ups / downs should last for
powerTime = levelConfig.levelConfig["options"]["powertime"]

# Now generate the objects for the bricks, based on the config file
numBrickRows = len(levelConfig.levelConfig["bricks"])

# Calculate if brickHeight is too large to fit in the area given
brickOffsetHeight = 0
for i in range(0, numBrickRows):
    brickOffsetHeight += i

# Total brick height. If it doesn't fit in the area given, alter the brick height
totalBrickAreaHeight = brickOffsetHeight + brickHeight*numBrickRows
if totalBrickAreaHeight > brickRenderHeight:
    brickHeight = brickRenderHeight / numBrickRows

rowCounter = 0
for rowKey in levelConfig.levelConfig["bricks"]:
    numBricksInRow = len(levelConfig.levelConfig["bricks"][rowKey])
    # Calculate the brick width
    brickOffsetWidth = 0
    for i in range(0, numBricksInRow):
        brickOffsetWidth += i

    brickWidth = (brickRenderWidth / numBricksInRow)
    print(brickWidth)

    print(rowKey)
    brickCounter = 0
    for brickConfig in levelConfig.levelConfig["bricks"][rowKey]:
        brickObject = Brick(brickWidth-1, brickHeight, brickCounter *
                            brickWidth + (screenWidth - brickRenderWidth) / 2, screenHeight / 4 - brickRenderHeight/4 + rowCounter*brickHeight + rowCounter, Constants.ReturnColour(brickConfig.numCollisions), numCollisions=brickConfig.numCollisions, powerValue=brickConfig.powerValue)
        brickGroup.add(brickObject)
        if brickObject.numCollisions != -1:
            secondaryBrickGroup.add(brickObject)
        brickCounter += 1
    rowCounter += 1

# exit()
# -------- Main Program Loop -----------
while carryOn:
    # Fill the screen with a black colour
    screen.fill((0, 0, 0))
    # Draw the background image
    if bgFile != None:
        screen.blit(bgImage, (0, 0))

    # Use the events framework to determine when the quit button is clicked and if the escape key is pressed
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we can exit the while loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                carryOn = False
            if event.key == pygame.K_q:
                carryOn = False

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT]:
        if len(paddleGroup) == 1:
            paddle.updatePosition(Constants.Left, screenWidth)
        else:
            for paddleCounter in range(0, len(paddleGroup)):
                print(paddleCounter)
                paddleObject = paddleGroup.sprites()[paddleCounter]
                if paddleCounter == 0:
                    direction = Constants.Right
                else:
                    direction = Constants.Left
                paddleObject.updatePosition(direction, screenWidth)

    if keys_pressed[pygame.K_RIGHT]:
        if len(paddleGroup) == 1:
            paddle.updatePosition(Constants.Right, screenWidth)
        else:
            for paddleCounter in range(0, len(paddleGroup)):
                print(paddleCounter)
                paddleObject = paddleGroup.sprites()[paddleCounter]
                if paddleCounter == 0:
                    direction = Constants.Left
                else:
                    direction = Constants.Right
                paddleObject.updatePosition(direction, screenWidth)

    # Iterate over the balls in the group and change properties based on it's current angle and speed
    # as well as countdown, if a countdown is set
    for ballObject in ballGroup.sprites():
        ballObject.updatePosition(screenWidth)

        if (ballObject.directionY == 1 and ballObject.positionY >= paddle.positionY):
            if ballObject.type == "secondary":
                ballObject.kill()
            elif ballObject.type == "primary":
                ballObject.positionX = 100
                ballObject.positionY = 100
                numLives -= 1
                print("Lives:", numLives)

        if type(ballObject.countdown) == type(int()):
            ballObject.clock.tick()
            ballObject.testClock()

        screen.blit(ballObject.image,
                    (ballObject.positionX, ballObject.positionY))

    # Detect if the balls collide:
    # ballCollidedWith = ball.detectCollision(secondaryBallGroup)
    # if ballCollidedWith != None:

    #    if ball.directionY == -1 and ballCollidedWith.directionY == -1:
    #        ball.directionX *= -1
    #        ballCollidedWith.directionX *= -1

    #    if ball.directionY == 1 and ballCollidedWith.directionY == 1:
    #        ball.directionX *= -1
    #        ballCollidedWith.directionX *= -1

    #    if ball.directionY == 1 and ballCollidedWith.directionY == -1:
    #        ball.directionY *= -1
    #        ballCollidedWith.directionY *= -1

    #    if ball.directionY == -1 and ballCollidedWith.directionY == 1:
    #        ball.directionY *= -1
    #        ballCollidedWith.directionY *= -1

    # Detect if any balls collide with the paddles
    for paddleObject in paddleGroup:
        ballCollisionObject = paddleObject.detectCollision(ballGroup)

        if ballCollisionObject != None:
            ballCollisionObject.directionY *= -1

        # Update the clock for the second paddle
        if paddleObject.powerValue != None and paddleObject.countdown != None:
            paddleObject.clock.tick()
            paddleObject.testClock()

        screen.blit(paddleObject.image,
                    (paddleObject.positionX, paddleObject.positionY))

    # Detect if any balls collide with the bricks
    for ballObject in ballGroup:
        brickCollidedWith = ballObject.detectCollision(brickGroup)
        if brickCollidedWith != None:
            # if True:  # brickCollidedWith.numCollisions == -1 and :
            # if brickCollidedWith.numCollisions != -1:
            if ballObject.powerValue != Constants.Fireball:
                ballObject.directionY *= -1
            brickCollidedWith.registerCollision()

            # Add to the score whenever a collisions occurs
            gameScore += collisionPoints

            # Deal with the power ups / power downs
            if brickCollidedWith.powerValue != 0 and brickCollidedWith.powerInstigated == False:
                # Extra ball
                if brickCollidedWith.powerValue == Constants.ExtraBall:
                    print("Spawning second ball")
                    extraBall = Ball(ballRadius, ballRadius,
                                     screenWidth * 3/4, screenHeight/2, ballSpeed, type="secondary", countdown=powerTime, powerValue=brickCollidedWith.powerValue)
                    ballGroup.add(extraBall)
                    secondaryBallGroup.add(extraBall)
                if brickCollidedWith.powerValue == Constants.SpeedUpBall or brickCollidedWith.powerValue == Constants.SlowDownBall:
                    speedValue = 0
                    if brickCollidedWith.powerValue == Constants.SpeedUpBall:
                        speedValue = 1
                    elif brickCollidedWith.powerValue == Constants.SlowDownBall:
                        speedValue = -1
                    for ballObject in ballGroup:
                        ballObject.speed += 0.5 * ballObject.speed * speedValue
                        ballObject.countdown = powerTime
                        ballObject.powerValue = brickCollidedWith.powerValue
                if brickCollidedWith.powerValue == Constants.Laser:
                    createLaserBullets = True
                if brickCollidedWith.powerValue == Constants.Fireball:
                    for ballObject in ballGroup:
                        ballObject.powerValue = Constants.Fireball
                        ballObject.countdown = powerTime
                # Paddle related power values
                if brickCollidedWith.powerValue in Constants.PaddlePowerList:
                    # Second paddle
                    if brickCollidedWith.powerValue == Constants.SecondPaddle:
                        if len(paddleGroup) == 1:
                            extraPaddle = Paddle(paddleWidth, paddleHeight, screenWidth -
                                                 400, screenHeight - 100, paddleSpeed, type="secondary", countdown=powerTime, powerValue=brickCollidedWith.powerValue)
                            paddleGroup.add(extraPaddle)
                    if brickCollidedWith.powerValue == Constants.GrowPaddle or brickCollidedWith.powerValue == Constants.ShrinkPaddle:
                        sizeChange = 0
                        if brickCollidedWith.powerValue == Constants.GrowPaddle:
                            sizeChange = 1
                        elif brickCollidedWith.powerValue == Constants.ShrinkPaddle:
                            sizeChange = -1
                        for paddleObject in paddleGroup:
                            paddleObject.width += paddleObject.width * 0.5 * sizeChange
                            paddleObject.powerValue = brickCollidedWith.powerValue
                            paddleObject.countdown = powerTime
            brickCollidedWith.powerInstigated = True

    for brickObject in brickGroup:
        screen.blit(brickObject.image,
                    (brickObject.positionX, brickObject.positionY))

    # Construct a string to display the score and countdown timer
    textString = f'Score: {gameScore} - Countdown: {countdownTime}s - Lives: {numLives}'

    # Generate the text object to display the score and draw on the screen
    text = font.render(textString, True, Constants.Red)
    screen.blit(text, ((screenWidth - text.get_rect().width)/2, 10))

    # Update the laser bullet countdown timer if required
    if createLaserBullets:
        laserTimeCounter += clock.get_time()

    # Update the position of the laser bullets every 0.5s
    if frameCount % (frameRate * 0.5) == 0:
        if createLaserBullets:
            if laserTimeCounter < powerTime*1000:
                for paddleObject in paddleGroup:
                    newLaserBullet = LaserBullet(
                        laserWidth, laserHeight, paddleObject.positionX + paddleObject.width / 2, paddleObject.positionY, laserBulletSpeed)
                    laserBulletGroup.add(newLaserBullet)
            else:
                laserTimeCounter = 0
                createLaserBullets = False

    # Deal with what happens if the laser beam hits a brick, move the bullet if needed and remove when the timer runs out
    for laserBullet in laserBulletGroup:
        if laserTimeCounter < powerTime*1000:
            brickCollidedWith = laserBullet.detectCollision(brickGroup)
            if brickCollidedWith == None:
                laserBullet.updatePosition()
            else:
                brickCollidedWith.registerCollision()
                laserBullet.kill()
        else:
            laserBullet.kill()
    # Perform some screen updates every second
    if frameCount % frameRate == 0:
        # Update the title bar to show the FPS
        window.set_caption(f"{gameTitle} - {int(clock.get_fps())}fps")

        countdownTime -= 1

    for laserBulletObject in laserBulletGroup:
        screen.blit(laserBulletObject.image,
                    (laserBulletObject.positionX, laserBulletObject.positionY))

    # Update the entire display
    pygame.display.update()

    # Increase the frame counter, which is used for determining each 10s and 60s period
    frameCount += 1

    # Set the frame rate
    clock.tick(frameRate)

    if countdownTime == 0:
        carryOn = False

    if numLives == 0:
        carryOn = False

    if len(secondaryBrickGroup) == 0:
        carryOn = False

pygame.quit()
