# Import the pygame library and initialise the game engine
import random
import math
from BaseSprite import BaseSprite

# Define a class to create sprites for the ball, which inherits from the BaseSprite class


class Ball(BaseSprite):
    # Initialise the instance of the class
    def __init__(self, width, height, positionX, positionY, speed, image='images//ball.svg', type="primary", countdown=None, clock=None, powerValue=None):
        # Initialise the class being inherited from
        super().__init__(width, height, positionX, positionY,
                         image, countdown=countdown, clock=clock, powerValue=powerValue)
        # Set a random X direction whenever a ball is created
        self._directionX = random.choice([-1, 1])
        # Set the Y direction to start as travelling up the screen - needed as the ball starts from the paddle
        self._directionY = -1
        # Set a speed and original speed for the ball - original is used when a ball's speed has changed from a power value
        self._originalSpeed = speed
        self._speed = speed
        # Select a random angle that the ball can move in
        self._angle = math.radians(random.randint(30, 60))
        # Select if the ball is primary or secondary
        self._type = type

    # Create a "getter" to return the value of ball type (primary or secondary).
    # The @property decorator allows usage as a property, rather than a function call
    @property
    def type(self):
        return self._type

    # Return the angle as a property
    @property
    def angle(self):
        return self._angle

    # Set the angle as a property, rather than a function call
    @angle.setter
    def angle(self, value):
        self._angle = value

    # Get the directionX value
    @property
    def directionX(self):
        return self._directionX

    # Get the directionY value
    @property
    def directionY(self):
        return self._directionY

    # Set the directionX value
    @directionX.setter
    def directionX(self, value):
        self._directionX = value

    # Set the directionY value
    @directionY.setter
    def directionY(self, value):
        self._directionY = value

    # Get the speed value
    @property
    def speed(self):
        return self._speed

    # Set the speed value
    @speed.setter
    def speed(self, value):
        self._speed = value

    # Update the position of the ball, taking account for when the ball collides with the top and sides of the screen
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
