
class CC:
    def __init__(self):
        self.wnd = 1
        self.ssthresh = 1
        self.increase = 2
        self.IW = 1 # initial window that is sent during three way handshake
        self.LW = 2 # Loss window is the size of the congestion window after timeout
        self.RW = 1 # Restart window
        self.FW = 1 # FLIGHT window is the amout of bytes sent but not yet aknowledged

    def recvMessage(self, mes):
        if mes == "ACK":
            self.recvACK()
        elif mes == "NACK":
            self.recvNACK()
        elif mes == "LOST":
            self.packetLost()

    def congestionAvoidance(self): # wnd > ssthresh
        pass

    def slowStart(self): # wnd <= ssthresh
        pass

    def recvACK(self):
        pass

    def recvNACK(self):
        pass

    def packetLost(self):
        pass

