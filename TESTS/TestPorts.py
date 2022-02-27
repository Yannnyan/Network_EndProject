import unittest
import json

from CLIENT import portsManager

def testGetPort(self, manager):
    pass

def testResetFile(self):
    portsManager.resetFile()


if __name__ == "__main__":
    portsManager.resetFile()
    with open("CLIENT.ports.json") as file:
        d: dict = json.load(file)
        print(d)
    # TestPorts().testGetPort()

