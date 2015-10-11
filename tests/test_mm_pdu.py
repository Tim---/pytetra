import unittest
from pytetra.pdu.pdu import Bits
from pytetra.layer.mm.pdu import MmPdu, DLocationUpdateAccept
from pytetra.layer.mm.elements import *


class MmTestCase(unittest.TestCase):
    def test_dlocationupdateaccept(self):
        bits = '0101011100000101010000011101000110111000001001100000010111000010000000000000000000000100'
        #       ****                                                                                      PDU type = 5 (D-LOCATION UPDATE ACCEPT)
        #           ***                                                                                   Location update accept type = 3 (ITSI attach)
        #              O                                                                                  O-Bit = 1
        #               P                                                                                 P-Bit = 0
        #                P                                                                                P-Bit = 0
        #                 P                                                                               P-Bit = 0
        #                  P                                                                              P-Bit = 0
        #                   P                                                                             P-Bit = 0
        #                    M                                                                            M-Bit = 1
        #                     ****                                                                        Type 3/4 element identifier = 5 (Group identity location accept)
        #                         ***********                                                             Length indicator = 58
        #                                    ==========================================================   Group identity location accept
        #                                    .                                                              Group identity accept/reject = 0 (All attachment/detachments accepted)
        #                                     .                                                             Reserved = 0
        #                                      O                                                            O-Bit = 1
        #                                       M                                                           M-Bit = 1
        #                                        ****                                                       Type 3/4 element identifier = 7 (Group identity downlink)
        #                                            ***********                                            Length indicator = 38
        #                                                       ======================================        Group identity downlink
        #                                                       ******                                        Number of repeated elements = 1
        #                                                             ================================        Element 1
        #                                                             *                                         Group identity attach/detach type identifier = 0 (Attachment)
        #                                                              =====                                    Group identity attachment
        #                                                              **                                         Group identity attachment lifetime = 3 (Attachment for next location update required)
        #                                                                ***                                      Class of Usage = 4 (Class of usage 5)
        #                                                                   **                                  Group identity address type = 0 (GSSI)
        #                                                                     ************************          GSSI = 8388609
        #                                                                                             *     M-Bit = 0
        #                                                                                              *  M-Bit = 0
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
