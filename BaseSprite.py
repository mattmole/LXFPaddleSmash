# Import the pygame library and initialise the game engine
import pygame
import Constants

# Define a class to create sprites for the ball


class BaseSprite(pygame.sprite.Sprite):
    # Initialise the instance with any necessary variables
    def __init__(self, width, height, positionX, positionY, image, spriteType="image", colour=None, countdown=None, clock=None, powerValue=None):
        super().__init__()
        # Store the width twice, so that we can revert to the original value after a power value is used
        self._originalWidth = width
        self._width = width
        # Store the height twice, for the same reason
        self._originalHeight = height
        self._height = height
        # Position of the object
        self._positionX = positionX
        self._positionY = positionY
        # Colour of the object
        self._colour = colour
        # Allow a countdown value to be assigned to the objects
        self._countdown = countdown
        # Create an image by loading in the file and scaling it
        if spriteType == "image":
            self._image = pygame.image.load(image).convert_alpha()
            self._image = pygame.transform.scale(self._image, (width, height))
        # Create an image by drawing a rectangle with the surface method
        # Fill it with a colour
        elif spriteType == "rectangle":
            self._image = pygame.Surface((self._width, self._height))
            self._image.fill(self._colour)
        # Set the rectangle object for the sprite, by isong the get_rect() function
        self._rect = self._image.get_rect()
        # Call the updateRect() method as this updates the rectange to account for the original position the object will be drawn at
        self.updateRect()
        # Assign a clock to the object that can be used if a countdown value is set
        self._clock = pygame.time.Clock()
        # Variable to count how long the power value is assigned for
        self._timeElapsed = 0
        # Power value is whether the object has powerValues associated with it, or was created / altered by a powerValue
        self._powerValue = powerValue

    # Return the powerValue as a value, using the @property decorator
    @property
    def powerValue(self):
        return self._powerValue

    # Allow the powerValue to be set, by using a decorator
    @powerValue.setter
    def powerValue(self, value):
        self._powerValue = value

    # Return the clock as a value
    @property
    def clock(self):
        return self._clock

    # Return the countdown value as a value
    @property
    def countdown(self):
        if self._countdown == None:
            return self._countdown
        else:
            return int(self._countdown)

    # Allow the countdown value to be set, as a value, rather than as a function
    @countdown.setter
    def countdown(self, value):
        if value == None:
            self._countdown = value
        else:
            self._countdown = int(value)

    # Allow the rectangle to be returned as a value
    @property
    def rect(self):
        return self._rect

    # Update the rectangle object by referencing sub-elements
    def updateRect(self):
        self._rect.topleft = (self._positionX, self._positionY)
        self._rect.bottomleft = (
            self._positionX, self._positionY+self._height)
        self._rect.topright = (
            self.positionX + self._width, self._positionY)
        self._rect.bottomright = (
            self.positionX + self._width, self._positionY+self._height)
        self.rect.height = self.height
        self.rect.width = self.width

    # Return the positionX value
    @property
    def positionX(self):
        return self._positionX

    # Return the positionY value
    @property
    def positionY(self):
        return self._positionY

    # Allow positionX to be set, by using a value
    @positionX.setter
    def positionX(self, value):
        self._positionX = value
        self.updateRect()

    # Allow positionY to be set, by using a value
    @positionY.setter
    def positionY(self, value):
        self._positionY = value
        self.updateRect()

    # Return the width value
    @property
    def width(self):
        return self._width

    # Allow width to be set and if it is changed, call the tranformSize method before updating the rectangle
    @width.setter
    def width(self, value):
        oldWidth = self._width
        self._width = value
        if oldWidth != self._width:
            self.transformSize()
        self.updateRect()

    # Return the object's height
    @property
    def height(self):
        return self._height

    # Allow height to be set and if it is changed, call the tranformSize method before updating the rectangle
    @height.setter
    def height(self, value):
        oldHeight = self._height
        self._height = value
        if oldHeight != self._height:
            self.transformSize()
        self.updateRect()

    # Return the image as a value
    @property
    def image(self):
        return self._image

    # Return the colour as a value
    @property
    def colour(self):
        return self._colour

    # Allow the colour to be set, as a value
    @colour.setter
    def colour(self, value):
        self._colour = value

    # Use the spritecollideany function to determine whether the object collides with any objects
    # in the group that is passed into the function. Return the object being collided with
    def detectCollision(self, objectGroup):
        collidedObject = pygame.sprite.spritecollideany(self, objectGroup)
        return collidedObject

    # Transform the size of the object
    def transformSize(self):
        self._image = pygame.transform.scale(
            self._image, (self._width, self._height))

    # Function used to determine if any power values have timed out yet
    # If they have, undo the effect
    def testClock(self):
        # Work out how long it has been since the last clock tick
        timeSinceLastCall = self._clock.get_time()
        # Add this value to timeElapsed
        self._timeElapsed += timeSinceLastCall
        # If the elapsed time is above or equal to the countdown value, under the effects
        if self._timeElapsed >= self._countdown * 1000:
            # Destroy the extra ball
            if self._powerValue == Constants.ExtraBall:
                self.kill()
            # Revert the speed back to the original if the ball was slowed down or sped up
            if self._powerValue == Constants.SpeedUpBall or self._powerValue == Constants.SlowDownBall:
                self.speed = self._originalSpeed
            # Revert the size of the paddle if it was shrunk or expanded
            if self._powerValue == Constants.ShrinkPaddle or self._powerValue == Constants.GrowPaddle:
                self.width = self._originalWidth
            # Remove the second paddle if it has been created
            if self.powerValue == Constants.SecondPaddle:
                self.kill()
            # Remove the fireball functionality if it has been switched on
            if self.powerValue == Constants.Fireball:
                self.powerValue = None
            # Remove the countdown once any of the power values have been removed
            self.countdown = None
