import unittest
from pytetra.pdu.pdu import Bits
from pytetra.layer.cmce.pdu import CmcePdu, DConnect, DSetup, DRelease, DTxCeased, DCallProceeding
from pytetra.layer.cmce.elements import *


class CmceTestCase(unittest.TestCase):
    def test_dconnect(self):
        bits = Bits('000100000000000011001110000000')
        pdu = DConnect(
            PduType(2),
            CallIdentifier(6),
            CallTimeout(7),
            HookMethodSelection(0),
            SimplexDuplexSelection(0),
            TxGrant(0),
            TxReqPerm(0),
            CallOwnership(0)
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

    def test_dsetup(self):
        bits = Bits('00111000000000001100111000000010011000001001010000000000000000011001010')
        pdu = DSetup(
            PduType(7),
            CallIdentifier(6),
            CallTimeout(7),
            HookMethodSelection(0),
            SimplexDuplexSelection(0),
            BasicServiceInformation(
                CircuitModeType(0),
                EncryptionFlag(0),
                CommunicationType(1),
                SlotsPerFrame(0),
                SpeechService(3)
            ),
            TxGrant(0),
            TxReqPerm(0),
            CallPriority(2)
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

    def test_drelease(self):
        bits = Bits('0011000000000000110011100100')
        pdu = DRelease(
            PduType(6),
            CallIdentifier(6),
            DisconnectCause(14)
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

    def test_dtxceased(self):
        bits = Bits('010010000000000011000')
        pdu = DTxCeased(
            PduType(9),
            CallIdentifier(6),
            TxReqPerm(0)
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

    def test_dcallproceeding(self):
        bits = Bits('0000100000000000110110000100')
        pdu = DCallProceeding(
            PduType(1),
            CallIdentifier(6),
            CallTimeoutSetUpPhase(6),
            HookMethodSelection(0)
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

if __name__ == '__main__':
    unittest.main()
