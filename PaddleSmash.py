# Import the pygame library and initialise the game engine
import pygame
import Constants
import os
import pygame_menu
from Ball import Ball
from Paddle import Paddle
from LaserBullet import LaserBullet
from Brick import *
from ParseConfig import ParseLevelConfig
from rich import print

# Initialise pygame
pygame.init()

# Define whether to use full screen or not
fullScreen = False

# Variables to define sizes of the window and the paddles
screenRes = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screenWidth = int(pygame.display.Info().current_w / 2)
screenHeight = int(pygame.display.Info().current_h - 100)
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
ballRadius = (screenWidth * screenHeight) / 30000
paddleWidth = screenWidth * screenHeight / 5000
paddleHeight = paddleWidth / 6
brickRenderWidth = screenWidth - 4 * ballRadius
brickRenderHeight = screenHeight / 2
brickHeight = screenHeight / 30
paddleSpeed = screenHeight / 150
ballSpeed = screenHeight / 150
laserHeight = screenHeight / 40
laserWidth = screenHeight / 120
laserBulletSpeed = screenHeight / 150

# Variables to hold directory locations
levelConfigDir = "levels//"

# Variable to store the points per collision
collisionPoints = 10

# Add a font to be used to show the score and any other text
font = pygame.font.SysFont(None, int(screenHeight / 20))

# Create an object to be used for the two paddles
paddle = Paddle(paddleWidth, paddleHeight, 0, screenHeight - 100, paddleSpeed)
paddle2 = Paddle(paddleWidth, paddleHeight,
                 screenWidth - 400, screenHeight - 100, paddleSpeed)

# Create an object for the main ball
ball = Ball(ballRadius, ballRadius, paddle.positionX + ballRadius / 2,
            paddle.positionY - ballRadius, ballSpeed)

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

# Frame counter variable to use to determine when certain time periods have passed
frameCount = 0

# Variables to store the score
gameScore = 0

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Load all of the config files from the levels directory and store in structures, to be used later on
levelConfigFileDict = {}
levelConfigCounter = 0
levelConfigMenuList = []
for levelConfigFile in os.listdir(levelConfigDir):
    filePath = os.path.join(levelConfigDir, levelConfigFile)
    if os.path.isfile(filePath) and "level" in levelConfigFile and ".conf" in levelConfigFile:
        parsedConfig = ParseLevelConfig(filePath)
        levelConfigFileDict[filePath] = parsedConfig
        levelConfigMenuList.append(
            (parsedConfig.levelConfig["options"]["name"], levelConfigCounter, parsedConfig.filePath, parsedConfig.levelConfig["options"]["number"]))
        levelConfigCounter += 1
levelConfigMenuList.sort(key=lambda x: x[3])

# Load the config file
# Set a default file to load, which corresponds with the first value from the levelConfigMenuList - this is used for the situation where the user does not select a level, so the setLevel function is not called
levelConfig = ParseLevelConfig(levelConfigMenuList[0][2])
# Define some variable, which will be used in a later function
bgMusicFile = None
bgFile = None
bgImage = None
bgMusic = None
numLives = None
countdownTime = None
powerTime = None
numBrickRows = None

# All of the logic used to play the level is in this function. It's a biggy!


def startLevel():
    # The following variables are defined outside of the function and need to be updated as such
    global createLaserBullets, frameCount, brickHeight, gameScore, laserTimeCounter

    # Empty the groups, so that we can start afresh
    brickGroup.empty()
    secondaryBrickGroup.empty()

    # Grab file paths from the config data
    print(levelConfig.filePath)
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

    # For each row, work out the width of each brick, using the number of bricks in the config file
    rowCounter = 0
    for rowKey in levelConfig.levelConfig["bricks"]:
        numBricksInRow = len(levelConfig.levelConfig["bricks"][rowKey])
        # Calculate the brick width allowing for a pixel between each one
        brickOffsetWidth = 0
        for i in range(0, numBricksInRow):
            brickOffsetWidth += i
        brickWidth = (brickRenderWidth / numBricksInRow)

        # Build a group of sprites to hold all of the bricks that will be rendered on the screen
        brickCounter = 0
        for brickConfig in levelConfig.levelConfig["bricks"][rowKey]:
            # Create a new Brick object, using variables we have previously calculated
            brickObject = Brick(brickWidth-1, brickHeight, brickCounter *
                                brickWidth + (screenWidth - brickRenderWidth) / 2, screenHeight / 4 - brickRenderHeight/4 + rowCounter*brickHeight + rowCounter, Constants.ReturnColour(brickConfig.numCollisions), numCollisions=brickConfig.numCollisions, powerValue=brickConfig.powerValue)
            # Add the bricks to our brick group
            brickGroup.add(brickObject)
            # We need a secondary group to store those bricks that can disintegrate. Indestructible bricks will never disappear and when this group drops to zero members, we know the level is complete
            if brickObject.numCollisions != -1:
                secondaryBrickGroup.add(brickObject)
            brickCounter += 1
        rowCounter += 1

    # The while loop will carry on until the user exits the level (e.g. clicks the close button, presses the escape key, removes the bricks...)
    carryOn = True
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

        # Keys pressed can work for keys that are held down, which is better for moving the paddle
        keys_pressed = pygame.key.get_pressed()
        # When the left arrow is pressed, move a single paddle left and if there are two, move them in opposite directions
        if keys_pressed[pygame.K_LEFT]:
            if len(paddleGroup) == 1:
                paddle.updatePosition(Constants.Left, screenWidth)
            else:
                for paddleCounter in range(0, len(paddleGroup)):
                    paddleObject = paddleGroup.sprites()[paddleCounter]
                    if paddleCounter == 0:
                        direction = Constants.Right
                    else:
                        direction = Constants.Left
                    paddleObject.updatePosition(direction, screenWidth)
        # When the right arrow is pressed, move a single paddle right and if there are two, move them in opposite directions
        if keys_pressed[pygame.K_RIGHT]:
            if len(paddleGroup) == 1:
                paddle.updatePosition(Constants.Right, screenWidth)
            else:
                for paddleCounter in range(0, len(paddleGroup)):
                    paddleObject = paddleGroup.sprites()[paddleCounter]
                    if paddleCounter == 0:
                        direction = Constants.Left
                    else:
                        direction = Constants.Right
                    paddleObject.updatePosition(direction, screenWidth)

        # Iterate over the balls in the group and change properties based on it's current angle and speed
        # as well as countdown, if a countdown is set
        for ballObject in ballGroup.sprites():
            # Call the object's updatePosition function
            ballObject.updatePosition(screenWidth)

            # If the ball is moving towards the bottom of the screen and is lower than the top of the paddles
            # do one of two things: Secondary ball - remove it, Primary ball - respawn and remove a life
            if (ballObject.directionY == 1 and ballObject.positionY >= paddle.positionY):
                if ballObject.type == "secondary":
                    ballObject.kill()
                elif ballObject.type == "primary":
                    ballObject.positionX = paddle.positionX + ballRadius / 2
                    ballObject.positionY = paddle.positionY - ballRadius
                    numLives -= 1
                    print("Lives:", numLives)
            # Secondary balls will be removed after a countdown time. If the ball has a countdown associated with
            # it, tick the clock and call the testClock function to determine if it needs to be destroyed yet
            if type(ballObject.countdown) == type(int()):
                ballObject.clock.tick()
                ballObject.testClock()

            # Detect if any balls collide with the bricks
            brickCollidedWith = ballObject.detectCollision(brickGroup)
            if brickCollidedWith != None:
                if ballObject.powerValue != Constants.Fireball or (ballObject.powerValue == Constants.Fireball and brickObject.numCollisions == -1):
                    ballObject.directionY *= -1
                # If a brick has been collided with, call the relevant function to determine whether
                # it should be destroyed or not
                brickCollidedWith.registerCollision()

                # Add to the score whenever a collisions occurs
                gameScore += collisionPoints

                # Deal with the power ups / power downs. Depending what the power value is, do different things
                if brickCollidedWith.powerValue != 0 and brickCollidedWith.powerInstigated == False:
                    # Extra ball
                    if brickCollidedWith.powerValue == Constants.ExtraBall:
                        extraBall = Ball(ballRadius, ballRadius,
                                         paddle.positionX + ballRadius/2, paddle.positionY - ballRadius, ballSpeed, type="secondary", countdown=powerTime, powerValue=brickCollidedWith.powerValue)
                        ballGroup.add(extraBall)
                        secondaryBallGroup.add(extraBall)
                    # Speed up or slow down the ball
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
                    # Add lasers to the paddle(s)
                    if brickCollidedWith.powerValue == Constants.Laser:
                        createLaserBullets = True
                    # Make the ball(s) have fireball power, so they pass through the bricks and destroy them instantly
                    if brickCollidedWith.powerValue == Constants.Fireball:
                        for ballObject in ballGroup:
                            ballObject.powerValue = Constants.Fireball
                            ballObject.countdown = powerTime
                    # Paddle related power values
                    if brickCollidedWith.powerValue in Constants.PaddlePowerList:
                        # Add a second paddle
                        if brickCollidedWith.powerValue == Constants.SecondPaddle:
                            if len(paddleGroup) == 1:
                                extraPaddle = Paddle(paddleWidth, paddleHeight, screenWidth -
                                                     400, screenHeight - 100, paddleSpeed, type="secondary", countdown=powerTime, powerValue=brickCollidedWith.powerValue)
                                paddleGroup.add(extraPaddle)
                        # Grow or shrink the paddle(s)
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
                # Mark the brick so that the power value cannot be used multiple times (relevant for multi-collision bricks)
                brickCollidedWith.powerInstigated = True

            # Draw the ball object(s) on the screen each time the loop iterates
            screen.blit(ballObject.image,
                        (ballObject.positionX, ballObject.positionY))

        # Detect if any balls collide with the paddles
        for paddleObject in paddleGroup:
            ballCollisionObject = paddleObject.detectCollision(ballGroup)

            # Reverse the Y direction of the ball, if it collides with a paddle
            if ballCollisionObject != None:
                ballCollisionObject.directionY *= -1

            # Update the clock for the second paddle, so that it will disappear at the end of the countdown period
            if paddleObject.powerValue != None and paddleObject.countdown != None:
                paddleObject.clock.tick()
                paddleObject.testClock()

            # Draw the paddle on the screen, each time the loop runs
            screen.blit(paddleObject.image,
                        (paddleObject.positionX, paddleObject.positionY))

        # Draw the bricks on the screen, each time the loop runs
        for brickObject in brickGroup:
            screen.blit(brickObject.image,
                        (brickObject.positionX, brickObject.positionY))

        # Construct a string to display the score and countdown timer
        textString = f'Score: {gameScore} - Countdown: {countdownTime}s - Lives: {numLives}'

        # Generate the text object to display the score and draw on the screen
        text = font.render(textString, True, Constants.Red)
        screen.blit(text, ((screenWidth - text.get_rect().width)/2, 10))

        # Update the laser bullet countdown timer if required.
        # Like all power values, they stop after a configured time.
        if createLaserBullets:
            laserTimeCounter += clock.get_time()

        # Update the position of the laser bullets every 0.5s
        if frameCount % (frameRate * 0.5) == 0:
            # If laser bullet are being created, create news ones every 0.5 seconds and add to the group
            if createLaserBullets:
                if laserTimeCounter < powerTime*1000:
                    for paddleObject in paddleGroup:
                        newLaserBullet = LaserBullet(
                            laserWidth, laserHeight, paddleObject.positionX + paddleObject.width / 2, paddleObject.positionY, laserBulletSpeed)
                        laserBulletGroup.add(newLaserBullet)
                else:
                    # When the countdown period has elapsed, mark the counter as zero and the creation flag to False
                    laserTimeCounter = 0
                    createLaserBullets = False

        # Deal with what happens if the laser beam hits a brick, move the bullet if needed and remove when the timer runs out
        for laserBullet in laserBulletGroup:
            # During the countdown timer period, act on any bricks that the laser beam collides with
            if laserTimeCounter < powerTime*1000:
                brickCollidedWith = laserBullet.detectCollision(brickGroup)
                # If it doesn't collide, update the position
                if brickCollidedWith == None:
                    laserBullet.updatePosition()
                else:
                    # If it does collide, register the collision and remove the laser bullet
                    brickCollidedWith.registerCollision()
                    laserBullet.kill()
            # When the countdown timer elapses, remove all laser bullets from the screen
            else:
                laserBullet.kill()

        # Update the window title each second to show the frame rate
        if frameCount % frameRate == 0:
            # Update the title bar to show the FPS
            window.set_caption(f"{gameTitle} - {int(clock.get_fps())}fps")
            # Reduce the level countdown timer by 1s
            countdownTime -= 1

        # Draw the laser bullets on the screen each time the loop passes
        for laserBulletObject in laserBulletGroup:
            screen.blit(laserBulletObject.image,
                        (laserBulletObject.positionX, laserBulletObject.positionY))

        # Update the entire display
        pygame.display.update()

        # Increase the frame counter, which is used for determining each 10s and 60s period
        frameCount += 1

        # Set the frame rate
        clock.tick(frameRate)

        # If the level countdown reaches zero, break out from the loop
        if countdownTime == 0:
            carryOn = False

        # If the number of lives reaches zero, break out from the loop
        if numLives == 0:
            carryOn = False

        # If all bricks that can be disintegrate are removed from the secondaryBrickGroup break out from the loop
        if len(secondaryBrickGroup) == 0:
            carryOn = False


# This function loads the relevant config file, when the option is selected on the menu system
def setLevel(name, positionInList, filePath, numbers):
    # Use the dictionary contain all config files and assign the relevant values to the variables
    global levelConfig
    levelConfig = levelConfigFileDict[filePath]
    print(filePath)


# Let's draw the menu
menu = pygame_menu.Menu('Welcome', screenWidth - 100, screenHeight - 100,
                        theme=pygame_menu.themes.THEME_BLUE)

# Add a text field, so that the player can enter their name
menu.add.text_input('Name: ', default='John Doe')
# Add a menu selector to pick which level to play. This takes the information from the previous step, which loads the config files in
# The setLevel function is called when this option changes
menu.add.selector(
    'Difficulty: ', levelConfigMenuList, onchange=setLevel)
# Add a button, to start playing the game. The startLevel function is called
menu.add.button('Play', startLevel)
# Add a button, to quit the game. When pressed the EXIT event is put onto the event bus
menu.add.button('Quit', pygame_menu.events.EXIT)

# Display the menu on the screen
menu.mainloop(screen)

# Quit the game when the mainloop ends
pygame.quit()
