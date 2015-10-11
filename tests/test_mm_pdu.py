import unittest
from pytetra.pdu.pdu import Bits
from pytetra.layer.mm.pdu import MmPdu, DLocationUpdateAccept
from pytetra.layer.mm.elements import *


class MmTestCase(unittest.TestCase):
    def test_dlocationupdateaccept(self):
        bits = '0101011100000101010000011101000110111000001001100000010111000010000000000000000000000100'
        pdu = DLocationUpdateAccept(
            PduType(5),
            LocationUpdateAcceptType('ITSI attach'),
            GroupIdendtityLocationAccept(
                GroupIdentityAcceptReject('accept'),
                Reserved(0),
                [
                    GroupIdentityDownlink(
                        GroupIdentityAttachDetachTypeIdentifier('attach'),
                        GroupIdentityAttachment(
                            GroupIdentityAttachmentLifetime(3),
                            ClassOfUsage(4)
                        ),
                        GroupIdentityAddressType('GSSI'),
                        Gssi(8388609)
                    )
                ]
            )
        )
        assert MmPdu.parse(Bits(bits)) == pdu

if __name__ == '__main__':
    unittest.main()
