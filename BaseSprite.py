# Import the pygame library and initialise the game engine
import pygame
import Constants
# Define a class to create sprites for the ball


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, positionX, positionY, image, spriteType="image", colour=None, countdown=None, clock=None, powerValue=None):
        super().__init__()
        self._originalWidth = width
        self._width = width
        self._originalHeight = height
        self._height = height
        self._positionX = positionX
        self._positionY = positionY
        self._colour = colour
        self._countdown = countdown
        if spriteType == "image":
            self._image = pygame.image.load(image).convert_alpha()
            self._image = pygame.transform.scale(self._image, (width, height))
        elif spriteType == "rectangle":
            self._image = pygame.Surface((self._width, self._height))
            self._image.fill(self._colour)
        self._rect = self._image.get_rect()
        self.updateRect()
        self._clock = pygame.time.Clock()
        self._timeElapsed = 0
        self._powerValue = powerValue

    @property
    def powerValue(self):
        return self._powerValue

    @powerValue.setter
    def powerValue(self, value):
        self._powerValue = value

    @property
    def clock(self):
        return self._clock

    @property
    def countdown(self):
        if self._countdown == None:
            return self._countdown
        else:
            return int(self._countdown)

    @countdown.setter
    def countdown(self, value):
        if value == None:
            self._countdown = value
        else:
            self._countdown = int(value)

    @property
    def rect(self):
        return self._rect

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

    @property
    def positionX(self):
        return self._positionX

    @property
    def positionY(self):
        return self._positionY

    @positionX.setter
    def positionX(self, value):
        self._positionX = value
        self.updateRect()

    @positionY.setter
    def positionY(self, value):
        self._positionY = value
        self.updateRect()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        oldWidth = self._width
        self._width = value
        if oldWidth != self._width:
            self.transformSize()
        self.updateRect()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        oldHeight = self._height
        self._height = value
        if oldHeight != self._height:
            self.transformSize()
        self.updateRect()

    @property
    def image(self):
        return self._image

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, value):
        self._colour = value

    def detectCollision(self, objectGroup):
        collidedObject = pygame.sprite.spritecollideany(self, objectGroup)
        return collidedObject

    def transformSize(self):
        self._image = pygame.transform.scale(
            self._image, (self._width, self._height))

    def testClock(self):
        a = self._clock.get_time()
        self._timeElapsed += a
        print(self._countdown, self._timeElapsed)
        if self._timeElapsed >= self._countdown * 1000:
            if self._powerValue == Constants.ExtraBall:
                self.kill()
            if self._powerValue == Constants.SpeedUpBall or self._powerValue == Constants.SlowDownBall:
                self.speed = self._originalSpeed
                self.countdown = None
            if self._powerValue == Constants.ShrinkPaddle or self._powerValue == Constants.GrowPaddle:
                self.width = self._originalWidth
                self.countdown = None
            if self.powerValue == Constants.SecondPaddle:
                self.kill()
                self.countdown = None
            if self.powerValue == Constants.Fireball:
                self.powerValue = None
                self.countdown = None
