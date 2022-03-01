import unittest
from SERVER import CongestionControl

checker = bin(65535)
print(checker)
print("len checker" + str(len(checker)))


class checksum(unittest.TestCase):
    def test_checkSum(self):
        a = "2222222222222222"
        print(len(a))
        b = "1111111"
        c = "1"

        #csum = CongestionControl.checksum(a)
        #csum = CongestionControl.checksum(b)
        csum = CongestionControl.checksum(c)
        #l = CongestionControl.divBy16Bits(b)
        #l = CongestionControl.divBy16Bits(a)
        l = CongestionControl.divBy16Bits(c)
        sum = 0
        for i in range(len(l)):
            sum += int(l[i],2)
        carry = 0
        bsum = bin(sum)
        p = len(bsum)
        if len(bsum) > 18:
            carry = len(bsum) - 18
            sum = sum + carry
            bsum = bin(int(bin(sum)[-16: ],2))
            self.assertEqual(bin(int(bsum,2)+ int(csum,2)),checker)
        elif len(bsum) == 18:
            self.assertEqual(bin(int(bsum, 2) + int(csum,2)), checker)
        else:
            s = CongestionControl.conv16bits(int(bsum,2))
            self.assertEqual(bin(int(s,2) + int(csum,2)),checker)


if __name__ == "__main__":
    unittest.main()