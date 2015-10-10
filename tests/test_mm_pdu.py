import unittest
from pytetra.pdu.pdu import Bits
from pytetra.layer.mm.pdu import MmPdu, DLocationUpdateAccept
from pytetra.layer.mm.elements import *


class MmTestCase(unittest.TestCase):
    def test_dlocationupdateaccept(self):
        bits = Bits('01010111000001010100000111010001101110000010011000000101110000100000000000000000000001001000')
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
        assert MmPdu.parse(bits) == pdu

if __name__ == '__main__':
    unittest.main()
