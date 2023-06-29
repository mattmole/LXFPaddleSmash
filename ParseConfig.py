import configparser
import os

# Create a class to store information about each brick, when read from config


class BrickConfig:
    # Initialise the instance
    def __init__(self, numCollisions=1, powerValue=0):
        self._numCollisions = numCollisions
        self._powerValue = powerValue

    # Return a textual representation
    def __repr__(self):
        return f"NumCollisions: {self.numCollisions}, PowerValue: {self.powerValue}"

    # Return number of collisions as a value, rather than needing to call a function
    @property
    def numCollisions(self):
        return self._numCollisions

    # Return power value as a value, rather than needing to call a function
    @property
    def powerValue(self):
        return self._powerValue

# Create a class to store config information


class ParseConfig:
    # Initialise the class
    def __init__(self, filePath):
        self._filePath = filePath
        self._config = None
        self.readConfig()

    # Read the config file and add to a instance variable, called _config
    def readConfig(self):
        if os.path.exists(self._filePath):
            config = configparser.ConfigParser()
            config.read(self._filePath)
            self._config = config

    # Return the _config variable information as a value called config. The @property
    # allows the function to operate in the same way as a value
    @property
    def config(self):
        return self._config

    # Return the filepath as a value
    @property
    def filePath(self):
        return self._filePath

# Create a class to ParseLevelConfig files, which inherits from the base ParseConfig class.
# This is useful as the same base class could be used if parsing overall game config etc.


class ParseLevelConfig(ParseConfig):
    # Initialise the instance
    def __init__(self, filePath):
        # Initialise the class being inherited from
        super().__init__(filePath)
        self._levelConfig = {}
        self.validateSections()
        self.readLevelOptions()
        self.readLevelBricks()

    # Validate config file sections by insuring that the relevant sections exist
    def validateSections(self):
        # Check if the relevant Sections exist
        if 'LEVEL' in self.config and 'BRICKS' in self.config:
            return True

    # Take the overall level options from the file and add to an options dictionary
    # Validate the options and then add to the _levelConfig dictionary
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

    # Read the level bricks from the file and add to a list for each row
    # Each row contains a list of brick objects, which contain the numCollisions
    # and powerValue information
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

    # Return the level config information, referencing as a value, rather than calling a functions
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

    # Return a textual representation of the level configuration
    def __repr__(self):
        return f"{self.filePath}: {self.levelConfig['options']['name']}"


# Testing - only run this code when file is being invoked directly
if __name__ == "__main__":
    a = ParseLevelConfig("levels//level1.conf")
    print(a.levelConfig)
