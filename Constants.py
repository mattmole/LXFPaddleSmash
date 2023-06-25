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

ColourList = [Red, Green, Blue, Black, White,
              Pink, Yellow, Orange, Cream, Brown, Gold, Purple, Grey]
random.shuffle(ColourList)


def ReturnColour(num):
    if num < len(ColourList):
        return ColourList[num]
    else:
        while num > len(ColourList):
            num -= len(ColourList)
        return ColourList[num]


# Define constants for the power ups
NoValue = 0         # Does not need implementing
Fireball = 1        # Implemented
Laser = 2           # Implemented
ExtraBall = 4       # Implemented
GrowPaddle = 8      # Implemented
SecondPaddle = 16   # Implemented
ShrinkPaddle = 32   # Implemented
SpeedUpBall = 64    # Implemented
SlowDownBall = 128  # Implemented

PaddlePowerList = [GrowPaddle, ShrinkPaddle, SecondPaddle]

# Define constants for direction of objects
Left = -1
Right = 1
Up = -1
Down = 1

if __name__ == "__main__":
    pass
