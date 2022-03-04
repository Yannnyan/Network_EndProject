checker = bin(65535)


# splits the string into 16 bits chunks
def divBy16Bits(buffer: str) -> []:
    listbuf = []
    if len(buffer) % 2 == 0:
        for i in range(0, len(buffer) - 1, 2):
            listbuf.append(binaryStringByte(buffer[i]) + binaryStringByte(buffer[i + 1]))
    else:
        for i in range(0, len(buffer) - 2, 2):
            listbuf.append(binaryStringByte(buffer[i]) + binaryStringByte(buffer[i + 1]))
        listbuf.append(binaryStringByte('\0') + binaryStringByte(buffer[len(buffer) - 1]))
    return listbuf


# receives a char and convers it to 8 bits of based on ascii value of the char
def binaryStringByte(cHar):
    l = ord(cHar)
    if l == 0:
        return "00000000"
    ret = ''
    while l != 0:
        if l % 2 == 1:
            ret = '1' + ret
        else:
            ret = '0' + ret
        l = int(l / 2)
    while len(ret) < 8:
        ret = '0' + ret
    return ret

def conv16bits(num):
    if num == 0:
        return binaryStringByte('\0') + binaryStringByte('\0')
    else:
        l = num
        res = ""
        while l != 0:
            if l % 2 == 1:
                res = '1' + res
            else:
                res = '0' + res
            l = int(l / 2)
        while len(res) < 16:
            res = '0' + res
        return res


def oneComplement(buf):
    res = list(buf)
    for i in range(2, len(buf)):
        if buf[i] == '0':
            res[i] = '1'
        else:
            res[i] = '0'
    return "".join(res)


def checksum(buffer: str):
    # split the buffer into 16 bits chunks
    listbytesbuffer = divBy16Bits(buffer)
    sum = 0
    # add them together
    for i in range(len(listbytesbuffer)):
        sum += int(listbytesbuffer[i], 2)
    bsum = bin(sum)
    carry = 0
    # if a carry is generated then add it
    if len(bsum) > 18:  # 0b1111... for some reason
        carry = len(bsum) - 18
        sum = sum + int(bin(carry),2)
        bsum = bin(sum)
        s = "0b" + bsum[-16:]
        return oneComplement(s)
    # no carry is less than 18, 18 because the python formula for binary num is 0b and then 16 bits
    # if less than 18 then pad the remaining left side with zeros and add 0b to the start as binary form
    if len(bsum) < 18:
        bSum = "0b" + conv16bits(sum)
        return oneComplement(bSum)
    if len(bsum) == 18:
        return oneComplement(bsum)

# just like the test, checks if the sum of the 16 bit groups with the carry and the checksum is 16 ones
# if it is then everything is alright, if not then the packet is corrupt
# return false if not corrupted, true if it is corrupted
def checkCurroption(buffer: str, csum: str) -> bool:
    l = divBy16Bits(buffer)
    sum = 0
    for i in range(len(l)):
        sum += int(l[i], 2)
    bsum = bin(sum)
    if len(bsum) > 18:
        carry = len(bsum) - 18
        sum = sum + carry
        bsum = bin(int(bin(sum)[-16:], 2))
        if bin(int(bsum, 2) + int(csum, 2)) == checker:
            return False
        else:
            return True
    elif len(bsum) == 18:
        if bin(int(bsum, 2) + int(csum, 2)) == checker:
            return False
        else:
            return True
    else:
        s = conv16bits(int(bsum, 2))
        if bin(int(s, 2) + int(csum, 2)) == checker:
            return False
        else:
            return True


