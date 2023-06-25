# Import the pygame library and initialise the game engine
import pygame
from BaseSprite import BaseSprite
import Constants
# Define a class to create sprites for the paddle


class LaserBullet(BaseSprite):
    def __init__(self, width, height, positionX=0, positionY=0, speed=0, colour=Constants.Yellow):
        super().__init__(width, height, positionX, positionY,
                         image=None, spriteType="rectangle", colour=colour)
        self._speed = speed

    def updatePosition(self):
        self.positionY -= self._speed
