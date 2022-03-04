import unittest
from SERVER import RDTServer
from Algorithms import checksum
checker = bin(65535)
print(checker)
print("len checker" + str(len(checker)))


class checkssum(unittest.TestCase):
    def test_checkSum(self):
        a = "2222222222222222"
        print(len(a))
        b = "1111111"
        c = "1"
        d = "ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"
        #csum = checksum.checksum(a)
        #csum = checksum.checksum(b)
        #csum = checksum.checksum(c)
        #csum = checksum.checksum("")
        csum = checksum.checksum(d)
        #l = checksum.divBy16Bits(b)
        #l = checksum.divBy16Bits(a)
        #l = checksum.divBy16Bits(c)
        #l = checksum.divBy16Bits("")
        l = checksum.divBy16Bits(d)
        sum = 0
        for i in range(len(l)):
            sum += int(l[i],2)
        bsum = bin(sum)
        if len(bsum) > 18:
            carry = len(bsum) - 18
            sum = sum + carry
            bsum = bin(int(bin(sum)[-16: ],2))
            self.assertEqual(bin(int(bsum,2)+ int(csum,2)),checker)
        elif len(bsum) == 18:
            self.assertEqual(bin(int(bsum, 2) + int(csum,2)), checker)
        else:
            s = checksum.conv16bits(int(bsum,2))
            self.assertEqual(bin(int(s,2) + int(csum,2)),checker)


if __name__ == "__main__":
    unittest.main()