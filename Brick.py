# Import the pygame library and initialise the game engine
import pygame
from BaseSprite import BaseSprite
import time

# Define a class to create sprites for the bricks


class Brick(BaseSprite):
    def __init__(self, width, height, positionX, positionY, colour, powerValue=None, numCollisions=1):
        super().__init__(width, height, positionX, positionY,
                         image=None, spriteType="rectangle", colour=colour, powerValue=powerValue)
        self._powerInstigated = False
        self._numCollisions = numCollisions
        self._collisionsRemaining = numCollisions
        self._alpha = 255

    @property
    def powerInstigated(self):
        return self._powerInstigated

    @powerInstigated.setter
    def powerInstigated(self, value):
        self._powerInstigated = value

    @property
    def numCollisions(self):
        return self._numCollisions

    @numCollisions.setter
    def numCollisions(self, value):
        self._numCollisions = value

    @property
    def collisionsRemaining(self):
        return self._collisionsRemaining

    @collisionsRemaining.setter
    def collisionsRemaining(self, value):
        self._collisionsRemaining = value

    def registerCollision(self, collisionPower=1):

        if self.collisionsRemaining != -1:
            if collisionPower == -1:
                collisionPower = self.numCollisions

            if self.collisionsRemaining > 0:
                self.collisionsRemaining -= collisionPower
                print(self.colour, ': ', self.collisionsRemaining,
                      '/', self._numCollisions)
            if self.collisionsRemaining > 0:
                self.alpha -= self.alpha / self._numCollisions
                self.setAlpha()
            if self.collisionsRemaining == 0:
                self.kill()

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = int(value)

    def setAlpha(self):
        self.image.set_alpha(self.alpha)
