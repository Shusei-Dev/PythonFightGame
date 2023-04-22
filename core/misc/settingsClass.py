import json, os, sys

class Settings:

    def __init__(self, gameObj):
        self.gameObj = gameObj

        with open(os.path.dirname(sys.argv[0]) + os.path.sep + "settings.json") as f:
            self.data = json.load(f)
