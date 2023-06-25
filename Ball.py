# Import the pygame library and initialise the game engine
import pygame
import random
import math
from BaseSprite import BaseSprite
import Constants

# Define a class to create sprites for the ball


class Ball(BaseSprite):
    def __init__(self, width, height, positionX, positionY, speed, image='images//ball.svg', type="primary", countdown=None, clock=None, powerValue=None):
        super().__init__(width, height, positionX, positionY,
                         image, countdown=countdown, clock=clock, powerValue=powerValue)
        self._directionX = random.choice([-1, 1])
        self._directionY = random.choice([-1, 1])
        self._originalSpeed = speed
        self._speed = speed
        self._angle = math.radians(random.randint(30, 60))
        self._type = type

    @property
    def type(self):
        return self._type

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    @property
    def directionX(self):
        return self._directionX

    @property
    def directionY(self):
        return self._directionY

    @directionX.setter
    def directionX(self, value):
        self._directionX = value

    @directionY.setter
    def directionY(self, value):
        self._directionY = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    def updatePosition(self, screenWidth):

        ballPositionX = self.positionX + self.directionX * \
            self.speed * math.cos(self.angle)
        ballPositionY = self.positionY + self.directionY*self.speed * \
            math.sin(self.angle)

        if (self.directionX == -1 and ballPositionX <= 0) or (self.directionX == 1 and ballPositionX >= screenWidth - self.width):
            self.directionX *= -1

        if (self.directionY == -1 and ballPositionY <= 0):
            self.directionY *= -1

        self.positionX = ballPositionX
        self.positionY = ballPositionY
