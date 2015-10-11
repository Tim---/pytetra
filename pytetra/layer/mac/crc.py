
class CRC(object):
    def __init__(self, poly):
        self.poly = poly

    def compute(self, bits):
        crc = [1] * len(self.poly)
        for i in range(len(bits)):
            b = bits[i]

            msb = crc[0] ^ b
            crc = crc[1:] + [0]
            if(msb):
                crc = [c ^ p for c, p in zip(crc, self.poly)]

        return [c ^ p for p, c in zip([1] * len(self.poly), crc)]


class TETRACRC(CRC):
    def __init__(self):
        super(TETRACRC, self).__init__([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])


class FastCrc(object):
    def __call__(self, b2):
        crc = [1] * 16
        for b in b2:
            c = crc.pop(0) ^ b
            crc.append(0)

            if(c):
                crc[3] = 1 - crc[3]
                crc[10] = 1 - crc[10]
                crc[15] = 1 - crc[15]
        return b2[:-16], (crc == [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1])

CrcChecker = FastCrc


class NormalTchsCrcChecker:
    def __init__(self):
        self.poly = map(int, '10001001')

    def __call__(self, b2):
        unprotected, protected, check = b2[:214], b2[214:-8], b2[-8:]
        s = list(reversed(protected))
        s = s + [0] * (len(self.poly) - 1)
        for i in range(len(s) - len(self.poly) + 1):
            if s[0]:
                for j in range(len(self.poly)):
                    s[j] ^= self.poly[j]
            s = s[1:]
        b8 = sum(protected + s) % 2
        return unprotected + protected, list(reversed(s)) + [b8] == check


class StealingTchsCrcChecker:
    def __init__(self):
        self.poly = map(int, '10011')

    def __call__(self, b2):
        unprotected, protected, check = b2[:107], b2[107:-4], b2[-4:]
        s = list(reversed(protected))
        s = s + [0] * (len(self.poly) - 1)
        for i in range(len(s) - len(self.poly) + 1):
            if s[0]:
                for j in range(len(self.poly)):
                    s[j] ^= self.poly[j]
            s = s[1:]
        return unprotected + protected, list(reversed(s)) == check


if __name__ == "__main__":
    bits = [0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]

    c = TETRACRC()
    print c.compute(bits)
