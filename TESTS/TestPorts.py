import json

FILE = "../Algorithms/ports.json"
from Algorithms import portsManager


def testGetPort():
    xport = portsManager.getPort()
    print(xport)
    portsManager.disconnectPort(xport)
    readPorts()


def readPorts():
    with open(FILE) as file:
        d: dict = json.load(file)
        print(d)

def testResetFile():
    portsManager.resetFile()


if __name__ == "__main__":
    portsManager.resetFile()
    testGetPort()
