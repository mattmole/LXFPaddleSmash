# Import the pygame library and initialise the game engine
import pygame
from BaseSprite import BaseSprite
import Constants
# Define a class to create sprites for the paddle


class Paddle(BaseSprite):
    def __init__(self, width, height, positionX=0, positionY=0, speed=1, image='images//paddle.svg', type="primary", countdown=None, powerValue=None):
        super().__init__(width, height, positionX, positionY,
                         image, countdown=countdown, powerValue=powerValue)
        self._speed = speed
        self._type = type
        # self._powerValue = powerValue

        print(self.speed)

    @property
    def type(self):
        return self._type

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    def updatePosition(self, direction, screenWidth):
        valueToMove = direction * self.speed
        self.positionX += valueToMove
        if self.positionX <= 0:
            self.positionX = 0
        if self.positionX >= screenWidth - self.width:
            self.positionX = screenWidth - self.width
