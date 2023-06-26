import random

# Define constants for the colours
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Black = (0, 0, 0)
White = (255, 255, 255)
Pink = (255, 0, 255)
Yellow = (255, 255, 0)
Orange = (255, 128, 0)
Cream = (255, 255, 204)
Brown = (153, 51, 0)
Gold = (204, 153, 0)
Purple = (153, 0, 255)
Grey = (179, 179, 179)

# Add the colours to a list
ColourList = [Red, Green, Blue, Black, White,
              Pink, Yellow, Orange, Cream, Brown, Gold, Purple, Grey]

# Randomise the list of colours
random.shuffle(ColourList)

# Function to return a colour. If the value is greater than the length of the list
# subtract the length of the list until the value is within range and then return a colour


def ReturnColour(num):
    if num < len(ColourList):
        return ColourList[num]
    else:
        while num > len(ColourList):
            num -= len(ColourList)
        return ColourList[num]


# Define constants for the power ups
NoValue = 0
Fireball = 1
Laser = 2
ExtraBall = 4
GrowPaddle = 8
SecondPaddle = 16
ShrinkPaddle = 32
SpeedUpBall = 64
SlowDownBall = 128

# Add any constants to a list that are for Paddle related power values
PaddlePowerList = [GrowPaddle, ShrinkPaddle, SecondPaddle]

# Define constants for direction of objects
Left = -1
Right = 1
Up = -1
Down = 1
