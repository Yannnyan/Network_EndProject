import unittest
from Algorithms import CongestionControl


class test_cc(unittest.TestCase):

    def setUp(self) -> None:
        self.cc = CongestionControl.CC(1024)

    def test_slowStart(self):
        sum = 0
        for i in range(1, 4):
            sum += i*2
        for i in range(sum):
            self.cc.recvMessage("ACK")
        self.cc.recvMessage("LOST")
        self.assertEqual(self.cc.cwnd, 4)
        for i in range(4):
            self.cc.recvMessage("ACK")
        self.assertEqual(self.cc.cwnd, 6)
        self.cc.recvMessage("LOST")
        self.cc.recvMessage("LOST")
        self.assertEqual(self.cc.cwnd, 2)
        for i in range(6):
            self.cc.recvMessage("ACK")
        self.assertEqual(self.cc.cwnd, 6)

    def test_CongestionAvoidance(self):
        pass
