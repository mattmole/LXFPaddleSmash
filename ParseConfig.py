import configparser
import os


class BrickConfig:
    def __init__(self, numCollisions=1, powerValue=0):
        self._numCollisions = numCollisions
        self._powerValue = powerValue

    def __repr__(self):
        return f"NumCollisions: {self.numCollisions}, PowerValue: {self.powerValue}"

    @property
    def numCollisions(self):
        return self._numCollisions

    @property
    def powerValue(self):
        return self._powerValue


class ParseConfig:
    def __init__(self, filePath):
        self._filePath = filePath
        self._config = None
        self.readConfig()

    def readConfig(self):
        if os.path.exists(self._filePath):
            config = configparser.ConfigParser()
            config.read(self._filePath)
            self._config = config

    @property
    def config(self):
        return self._config

    @property
    def filePath(self):
        return self._filePath


class ParseLevelConfig(ParseConfig):
    def __init__(self, filePath):
        super().__init__(filePath)
        self._levelConfig = {}
        self.validateSections()
        self.validateBricks()
        self.readLevelOptions()
        self.readLevelBricks()
        # print(self._levelConfig)

    def validateSections(self):
        # Check if the relevant Sections exist
        if 'LEVEL' in self.config and 'BRICKS' in self.config:
            return True

    def validateBricks(self):
        # Use a set to determine if all rows have the same number of bricks defined
        rowBrickNums = set()
        for rowName, bricks in self.config.items('BRICKS'):
            if rowName.startswith('row'):
                rowBrickNums.add(len(bricks.split(',')))
        if len(rowBrickNums) == 1:
            return True
        else:
            return False

    def readLevelOptions(self):
        options = {}
        for key, value in self.config.items('LEVEL'):
            options[key] = value
        self._levelConfig['options'] = options
        self._levelConfig['options']['lives'] = int(
            self._levelConfig['options']['lives'])
        self._levelConfig['options']['countdown'] = int(
            self._levelConfig['options']['countdown'])
        self._levelConfig['options']['powertime'] = int(
            self._levelConfig['options']['powertime'])
        self._levelConfig['options']['number'] = int(
            self._levelConfig['options']['number'])

    def readLevelBricks(self):
        rows = {}
        for key, value in self.config.items('BRICKS'):
            rows[key] = []
            for brick in value.split(","):
                numCollisions = None
                powerValue = 0
                if ":" not in brick:
                    numCollisions = brick
                elif ":" in brick:
                    numCollisions, powerValue = brick.split(":")
                else:
                    print("Error in file")
                    return
                rows[key].append(BrickConfig(
                    int(numCollisions), int(powerValue)))

        self._levelConfig['bricks'] = rows

    @property
    def levelConfig(self):
        # Add values of None if options missing in the config
        if "audio" not in self._levelConfig["options"]:
            self._levelConfig["options"]["audio"] = None
        if "background" not in self._levelConfig["options"]:
            self._levelConfig["options"]["background"] = None
        if "number" not in self._levelConfig["options"]:
            self._levelConfig["options"]["number"] = None
        if "name" not in self._levelConfig["options"]:
            self._levelConfig["options"]["name"] = None
        if "difficulty" not in self._levelConfig["options"]:
            self._levelConfig["options"]["difficulty"] = None
        if "countdown" not in self._levelConfig["options"]:
            self._levelConfig["options"]["countdown"] = None
        if "powertime" not in self._levelConfig["options"]:
            self._levelConfig["options"]["powertime"] = None
        if "lives" not in self._levelConfig["options"]:
            self._levelConfig["options"]["lives"] = None
        return self._levelConfig

    def __repr__(self):
        return f"{self.filePath}: {self.levelConfig['options']['name']}"


if __name__ == "__main__":
    a = ParseLevelConfig("levels//level1.conf")
    print(a.levelConfig)
