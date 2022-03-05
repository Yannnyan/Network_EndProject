import json

r = 15
startPort = 55000
serverStartPort = 55015
filename = "../Algorithms/ports.json"

def extractPortServer():
    file = open(filename, 'r')
    d: dict = json.load(file)
    d["portsServer"].pop(0)
    file.close()
    f = open(filename, 'w')
    json.dump(d, f)
    f.close()
    print(d["ports"])

def extractPort():
    file = open(filename, 'r')
    d: dict = json.load(file)
    d["ports"].pop(0)
    file.close()
    f = open(filename, 'w')
    json.dump(d, f)
    f.close()
    print(d["ports"])

def getPortServer() -> int:
    ports: list = checkAvailablePortsServer()
    if ports is None:
        return -1
    if len(ports) == 0:
        return -1
    port = ports[0]
    print(port)
    extractPortServer()
    return port

def getPort() -> int:
    ports: list = checkAvailablePorts()
    if ports is None:
        return -1
    if len(ports) == 0:
        return -1
    port = ports[0]
    print(port)
    extractPort()
    return port


def checkAvailablePorts() -> []:
    f = open(filename, 'r')
    d = json.load(f)
    f.close()
    # {ports: [1], portserver: [2]}
    return list(d.values())[0]


def checkAvailablePortsServer() -> []:
    f = open(filename, 'r')
    d = json.load(f)
    f.close()
    return list(d.values())[1]


def resetFile():
    f = open(filename, 'w')
    l = []
    s = []
    for i in range(r):
        l.append(startPort + i)
    for i in range(r):
        s.append(serverStartPort + i)
    d = {"ports": l, "portsServer": s}
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

def disconnectPortServer(port):
    f = open(filename, 'r')
    d = json.load(f)
    l = list(d["portsServer"])
    l.append(port)
    d["portsServer"] = l
    f.close()
    f = open(filename, 'w')
    json.dump(d, f)
    f.close()

#resetFile()