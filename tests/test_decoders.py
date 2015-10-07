import unittest
from pytetra.layer.mac.decoder import SCHFDecoder, BSCHDecoder, AACHDecoder, BNCHDecoder

f = lambda l: map(int, l)


class DecoderTestCase(object):
    def test_unscrambling(self):
        b4_ = self.decoder.unscramble(self.b5)
        self.assertEqual(b4_, self.b4)

    def test_deinterleaving(self):
        b3_ = self.decoder.deinterleave(self.b4)
        self.assertEqual(b3_, self.b3)

    def test_convolutional_decoding(self):
        b2_ = self.decoder.convolutional_decode(self.b3)
        self.assertEqual(b2_, self.b2)

    def test_block_decoding(self):
        b1_, crc_pass_ = self.decoder.block_decode(self.b2)
        self.assertEqual(b1_, self.b1)
        self.assertEqual(crc_pass_, self.crc_pass)


class BSCHTestCase(DecoderTestCase, unittest.TestCase):
    def setUp(self):
        self.b5 = f('011111110101111010111101000100101100000001000001101011001000110100011110110001101101011101101010001111110111011000101010')
        self.b4 = f('110000001010101001001100100010000000000000000110000011100010001110111101011001000010011101000101100000000011110010010011')
        self.b3 = f('000001100011001010100001010100010100011000000000000000000000111010110000000000000110110100011111110100110101111001001011')
        self.b2 = f('0001000001110100010001000000000000000000100000000000001100011011111001101101')
        self.b1 = f('000100000111010001000100000000000000000010000000000000110001')
        self.crc_pass = True
        self.decoder = BSCHDecoder()


class BNCHTestCase(DecoderTestCase, unittest.TestCase):
    def setUp(self):
        self.b5 = f('010000111000011001010001000010000001101011101010000111100100111101101001101001010010110010101101110111011000111110100000110101000000111001011111000101110001001001010011011000111110100011010001101000100101011110010110')
        self.b4 = f('011101010101101101101010001010110100000110110001111101101011001101000011111100011110000101100111001001101101111011011110101100010001011100001100011000100001010010100100010110011100011000100001011010001011111100100110')
        self.b3 = f('111010110110111111101101001100101110101000001100010011111111110101110010001111100110000011001100001011000111010110000000000000000000000000000001010011101101101101101101101010001100011011111100101100111100011111010110')
        self.b2 = f('10000011011100000100110000000100011011100110101101110110010111010000001000000000000000000000000111111111111111111101001001010010100001000010')
        self.b1 = f('1000001101110000010011000000010001101110011010110111011001011101000000100000000000000000000000011111111111111111110100100101')
        self.crc_pass = True
        self.decoder = BNCHDecoder(f('000000000100000000000001000001'))


class SCHFTestCase(DecoderTestCase, unittest.TestCase):
    def setUp(self):
        self.b5 = f('001110111011100111011010111101111000001101111011111010000111111000010110110011001100010011001111111001110110101100101110011000010011010111100110011001110000010111101011000110100010111001110011110100011111000010000001111100111010011100000000011100111001100100011110011111001101101001111110100010110100010001011000011001011101110101011010110001100010100111000111100111011000111100011010011010011011110000001000011000110000010110100001')
        self.b4 = f('000011010110010011100001110101001101100000100000000000001000001000111100100110000000100100000101000111000011101001010000000001000010110010110101000100100000001100011100001000000000000010000011000110110001100000110001101100010000111000011011001100101000000000110010001100100101000100000001001001000000011000110010011010110100000000001000001101000101000011101000000001000101010010110110010000110001010101100100011001011101000000001000')
        self.b3 = f('000000000000000110110100100011000000000000000000001011000011111011001011001001010110111011101000010011000000000000000000001011000011110111011000000000000111010001101011010111111110111101011100110110001000100000111111101101001100101110101000111100111111111100011000000000000000000000000000111011010011000000000000000001100011111010110000000000000000000000000000000000000000000000000000000000000000000000001010100111100000111011000000')
        self.b2 = f('00000000001100010000000000000000011001010000011000100000100110010000000000000000011001010100000000000010001010101110000010101000001110100011011100000100110000001011100001000000000000000000000010010000000000000001000010000000000000000000000000000000000000000000000000000111011101010000')
        self.b1 = f('0000000000110001000000000000000001100101000001100010000010011001000000000000000001100101010000000000001000101010111000001010100000111010001101110000010011000000101110000100000000000000000000001001000000000000000100001000000000000000000000000000000000000000000000000000')
        self.crc_pass = True
        self.decoder = SCHFDecoder(f('000000000100000000000001000001'))


class AACHTestCase(DecoderTestCase, unittest.TestCase):
    def setUp(self):
        self.b5 = f('111101101101111111100001001000')
        self.b4 = f('110000000000001011011010000000')
        self.b3 = f('110000000000001011011010000000')
        self.b2 = f('110000000000001011011010000000')
        self.b1 = f('11000000000000')
        self.crc_pass = True
        self.decoder = AACHDecoder(f('000000000100000000000001000001'))


if __name__ == '__main__':
    unittest.main()