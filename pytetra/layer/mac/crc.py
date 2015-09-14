
class CRC:
    def __init__(self, poly):
        self.poly = poly
    
    def compute(self, bits):
        crc = [1]*len(self.poly)
        for i in range(len(bits)):
            b = bits[i]
            
            c = crc[0] ^ b
            crc = crc[1:] + [0]
            if(c):
                crc = [c ^ p for c, p in zip(crc, self.poly)];

        return [c ^ p for p, c in zip([1]*len(self.poly), crc)]

class TETRACRC(CRC):
    def __init__(self):
        CRC.__init__(self, [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
