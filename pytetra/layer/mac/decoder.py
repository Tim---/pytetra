from pytetra.layer.mac.scrambling import Unscrambler
from pytetra.layer.mac.interleaving import BSCHDeinterleaver, SCHFDeinterleaver, HalfDeinterleaver, TCHSDeinterleaver
from pytetra.layer.mac.convolutional import ConvolutionalDecoder2_3, NormalTchsConvolutionalDecoder, StealingTchsConvolutionalDecoder
from pytetra.layer.mac.crc import CrcChecker, NormalTchsCrcChecker, StealingTchsCrcChecker
from pytetra.layer.mac.rmcode import RMDecoder
from pytetra.layer.mac.reordering import TchsReorderer


class Decoder(object):
    def decode(self, b5):
        b4 = self.unscramble(b5)
        b3 = self.deinterleave(b4)
        b2 = self.convolutional_decode(b3)
        b1, crc_pass = self.block_decode(b2)
        return b1, crc_pass


class SCHFDecoder(Decoder):
    def __init__(self, extended_colour_code):
        self.unscramble = Unscrambler(extended_colour_code)
        self.deinterleave = SCHFDeinterleaver()
        self.convolutional_decode = ConvolutionalDecoder2_3()
        self.block_decode = CrcChecker()


class SCHHDDecoder(Decoder):
    def __init__(self, extended_colour_code):
        self.unscramble = Unscrambler(extended_colour_code)
        self.deinterleave = HalfDeinterleaver()
        self.convolutional_decode = ConvolutionalDecoder2_3()
        self.block_decode = CrcChecker()


class BSCHDecoder(Decoder):
    def __init__(self):
        self.unscramble = Unscrambler([0] * 30)
        self.deinterleave = BSCHDeinterleaver()
        self.convolutional_decode = ConvolutionalDecoder2_3()
        self.block_decode = CrcChecker()


class AACHDecoder(Decoder):
    def __init__(self, extended_colour_code):
        self.unscramble = Unscrambler(extended_colour_code)
        self.deinterleave = lambda x: x
        self.convolutional_decode = lambda x: x
        self.block_decode = RMDecoder()


class NormalTchsDecoder(Decoder):
    def __init__(self, extended_colour_code):
        self.unscramble = Unscrambler(extended_colour_code)
        self.deinterleave = TCHSDeinterleaver()
        self.convolutional_decode = NormalTchsConvolutionalDecoder()
        self.block_decode = NormalTchsCrcChecker()
        self.reorder = TchsReorderer()

    def decode(self, b5):
        b1, crc_pass = super(NormalTchsDecoder, self).decode(b5)
        b0 = self.reorder(b1[::2]), self.reorder(b1[1::2])
        return b0, crc_pass


class StealingTchsDecoder(Decoder):
    def __init__(self, extended_colour_code):
        self.unscramble = Unscrambler(extended_colour_code)
        self.deinterleave = HalfDeinterleaver()
        self.convolutional_decode = StealingTchsConvolutionalDecoder()
        self.block_decode = StealingTchsCrcChecker()
        self.reorder = TchsReorderer()

    def decode(self, b5):
        b1, crc_pass = super(StealingTchsDecoder, self).decode(b5)
        b0 = self.reorder(b1)
        return b0, crc_pass


BNCHDecoder = STCHDecoder = SCHHDDecoder


class Decoders(dict):
    def __init__(self):
        self['BSCH'] = BSCHDecoder()

    def decode(self, channel, b5):
        return self[channel].decode(b5)

    def set_extended_colour_code(self, extended_colour_code):
        self['SCH/F'] = SCHFDecoder(extended_colour_code)
        self['SCH/HD'] = SCHHDDecoder(extended_colour_code)
        self['STCH'] = STCHDecoder(extended_colour_code)
        self['AACH'] = AACHDecoder(extended_colour_code)
        self['TCH/S normal'] = NormalTchsDecoder(extended_colour_code)
        self['TCH/S stealing'] = StealingTchsDecoder(extended_colour_code)
