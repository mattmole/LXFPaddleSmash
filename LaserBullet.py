
# Import the pygame library and initialise the game engine
import pygame
from BaseSprite import BaseSprite
import Constants

# Define a class to create sprites for the laser bullets


class LaserBullet(BaseSprite):
    # Intialise the instance
    def __init__(self, width, height, positionX=0, positionY=0, speed=0, colour=Constants.Yellow):
        # Initialise the base class being inherited from
        super().__init__(width, height, positionX, positionY,
                         image=None, spriteType="rectangle", colour=colour)
        self._speed = speed

    # Function to update the position of the bullet
    def updatePosition(self):
        self.positionY -= self._speed
