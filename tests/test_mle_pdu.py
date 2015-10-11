import unittest
from pytetra.pdu.pdu import Bits
from pytetra.pdu.sublayer32pdu import SduElement
from pytetra.layer.mle.pdu import MlePdu, DMleSyncPdu, DMleSysinfoPdu
from pytetra.layer.mle.elements import *


class MleTestCase(unittest.TestCase):
    def test_mlepdu(self):
        bits = Bits('00101010111000001010100000111010001101110000010011000000101110000100000000000000000000001001000')
        pdu = MlePdu(
            ProtocolDiscriminator(1),
            SduElement(Bits('01010111000001010100000111010001101110000010011000000101110000100000000000000000000001001000'))
        )
        self.assertEqual(MlePdu.parse(bits), pdu)

    def test_dmlesync(self):
        bits = Bits('00000000010000000000000110001')
        pdu = DMleSyncPdu(
            Mcc(1),
            Mnc(1),
            NeighbourCellBroadcast(2),
            CellServiceLevel(0),
            LateEntryInformation(1)
        )
        self.assertEqual(DMleSyncPdu.parse(bits), pdu)

    def test_dmlesysinfo(self):
        bits = Bits('000000000000011111111111111111110100100101')
        pdu = DMleSysinfoPdu(
            La(1),
            SubscriberClass(65535),
            NeighbourCellBroadcast(3),
            BsServiceDetails(293)
        )
        self.assertEqual(DMleSysinfoPdu.parse(bits), pdu)


if __name__ == '__main__':
    unittest.main()
