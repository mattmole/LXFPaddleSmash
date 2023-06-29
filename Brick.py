# Import the pygame library and initialise the game engine
from BaseSprite import BaseSprite

# Define a class to create sprites for the bricks


class Brick(BaseSprite):
    # Initialise the instance
    def __init__(self, width, height, positionX, positionY, colour, powerValue=None, numCollisions=1):
        # Initialise the base class being inherited from
        super().__init__(width, height, positionX, positionY,
                         image=None, spriteType="rectangle", colour=colour, powerValue=powerValue)
        self._powerInstigated = False
        self._numCollisions = numCollisions
        self._collisionsRemaining = numCollisions
        self._alpha = 255

    # Return the powerInstigated value
    @property
    def powerInstigated(self):
        return self._powerInstigated

    # Allow the powerInstigated function to be used as a value
    @powerInstigated.setter
    def powerInstigated(self, value):
        self._powerInstigated = value

    # Return number of collisions
    @property
    def numCollisions(self):
        return self._numCollisions

    # Allow the number of collisions to be set as a value
    @numCollisions.setter
    def numCollisions(self, value):
        self._numCollisions = value

    # Return the number of collisions remaining, as a value
    @property
    def collisionsRemaining(self):
        return self._collisionsRemaining

    # Allow the number of collisons remaining to be set as a value
    @collisionsRemaining.setter
    def collisionsRemaining(self, value):
        self._collisionsRemaining = value

    # Work out what happens if a ball collides with a brick
    def registerCollision(self, collisionPower=1):
        # If the brick isn't indestructable...
        if self.collisionsRemaining != -1:
            # Use collisionPower to determine if fireball is being used
            if collisionPower == -1:
                # If fireball, set collision power to number of collisions required to remove the brick
                collisionPower = self.numCollisions

            # If collisionsRemaining > 0, reduce the value and change the alpha value
            if self.collisionsRemaining > 0:
                self.collisionsRemaining -= collisionPower
                self.alpha -= self.alpha / self._numCollisions
                self.setAlpha()
            # If no collisions are remaining, destroy the brick
            if self.collisionsRemaining == 0:
                self.kill()

    # Return the alpha value of the brick
    @property
    def alpha(self):
        return self._alpha

    # Allow the alpha value to be set as a value and not a function
    @alpha.setter
    def alpha(self, value):
        self._alpha = int(value)

    # Create a function to set the value of the alpha of a brick
    def setAlpha(self):
        self.image.set_alpha(self.alpha)
