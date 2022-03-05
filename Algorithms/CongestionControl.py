import math

class CC:
    def __init__(self, MSS):
        self.MSS = MSS
        self.cwnd = 2
        self.ss = True
        self.keepsend = True
        self.ssthresh = math.inf
        self.acks = 0


    def recvMessage(self, mes):
        if mes == "ACK":
            self.acks += 1
            if self.acks >= self.cwnd:
                self.acks = 0
                if self.ss:
                    self.slowStart()
                else:
                    self.congestionAvoidance()
        elif mes == "LOST":
            self.resetcwnd()

    def congestionAvoidance(self):  # wnd > ssthresh
        self.cwnd += 2

    def slowStart(self):  # wnd <= ssthresh
        self.cwnd *= 2
        if self.cwnd >= self.ssthresh:
            self.ss = False

    def resetcwnd(self):
        # Fast recovery parameter, not going back to slow start
        self.ssthresh = math.ceil(self.cwnd / 2)
        self.acks = 0
        self.cwnd = self.ssthresh
        self.ss = False


    # def recvACK(self):
    #     pass
    #
    # def recvNACK(self):
    #     pass
    #
    # def packetLost(self):
    #     pass
