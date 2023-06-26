# Import the pygame library and initialise the game engine
import pygame
from BaseSprite import BaseSprite
import Constants

# Define a class to create sprites for the paddle


class Paddle(BaseSprite):
    # Initialise the instance
    def __init__(self, width, height, positionX=0, positionY=0, speed=1, image='images//paddle.svg', type="primary", countdown=None, powerValue=None):
        # Initialise the base class being inherited from
        super().__init__(width, height, positionX, positionY,
                         image, countdown=countdown, powerValue=powerValue)
        self._speed = speed

    # Return the speed as a value
    @property
    def speed(self):
        return self._speed

    # Set the speed as a value
    @speed.setter
    def speed(self, value):
        self._speed = value

    # Function is used to update the position of the paddle
    def updatePosition(self, direction, screenWidth):
        valueToMove = direction * self.speed
        self.positionX += valueToMove
        if self.positionX <= 0:
            self.positionX = 0
        if self.positionX >= screenWidth - self.width:
            self.positionX = screenWidth - self.width
