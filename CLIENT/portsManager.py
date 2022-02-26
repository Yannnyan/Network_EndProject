import json

r = 15
startPort = 55000
filename = "ports.json"

def extractPort():
    file = open(filename, 'r')
    d: dict = json.load(file)
    d["ports"].pop(0)
    file.close()
    f = open(filename, 'w')
    json.dump(d, f)
    f.close()
    print(d["ports"])


def getPort() -> int:
    ports: list = checkAvailablePorts()
    if ports is None:
        return -1
    if len(ports) == 0:
        return -1
    port = ports[0][0]
    print(port)
    extractPort()
    return port


def checkAvailablePorts() -> []:
    f = open(filename, 'r')
    d = json.load(f)
    f.close()
    return list(d.values())


def resetFile():
    f = open(filename, 'w')
    l = []
    for i in range(r):
        l.append(startPort + i)
    d = {"ports": l}
    json.dump(d, f)
    f.close()


def disconnectPort(port):
    f = open(filename, 'r')
    d = json.load(f)
    l = list(d["ports"])
    l.append(port)
    d["ports"] = l
    f.close()
    f = open(filename, 'w')
    json.dump(d, f)
    f.close()
