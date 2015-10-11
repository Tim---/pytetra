import unittest
from pytetra.pdu.pdu import Bits
from pytetra.layer.cmce.pdu import CmcePdu, DConnect, DSetup, DRelease, DTxCeased, DCallProceeding
from pytetra.layer.cmce.elements import *


class CmceTestCase(unittest.TestCase):
    def test_dconnect(self):
        bits = Bits('000100000000000011001110000000')
        pdu = DConnect(
            PduType('D-CONNECT'),
            CallIdentifier(6),
            CallTimeout(7),
            HookMethodSelection('disabled'),
            SimplexDuplexSelection('simplex'),
            TransmissionGrant('granted'),
            TransmissionRequestPermission('allowed'),
            CallOwnership(0)
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

    def test_dsetup(self):
        bits = Bits('00111000000000001100111000000010011000001001010000000000000000011001010')
        pdu = DSetup(
            PduType('D-SETUP'),
            CallIdentifier(6),
            CallTimeout(7),
            HookMethodSelection('disabled'),
            SimplexDuplexSelection('simplex'),
            BasicServiceInformation(
                CircuitModeType('TCH/S'),
                EncryptionFlag('clear'),
                CommunicationType('point-to-multipoint'),
                SlotsPerFrame(0),
                SpeechService('Proprietary encoded speech')
            ),
            TransmissionGrant('granted'),
            TransmissionRequestPermission('allowed'),
            CallPriority(2)
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

    def test_drelease(self):
        bits = Bits('0011000000000000110011100100')
        pdu = DRelease(
            PduType('D-RELEASE'),
            CallIdentifier(6),
            DisconnectCause(14)
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

    def test_dtxceased(self):
        bits = Bits('010010000000000011000')
        pdu = DTxCeased(
            PduType('D-TX CEASED'),
            CallIdentifier(6),
            TransmissionRequestPermission('allowed')
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

    def test_dcallproceeding(self):
        bits = Bits('0000100000000000110110000100')
        pdu = DCallProceeding(
            PduType('D-CALL-PROCEEDING'),
            CallIdentifier(6),
            CallTimeoutSetUpPhase(6),
            HookMethodSelection('disabled')
        )
        self.assertEqual(CmcePdu.parse(bits), pdu)

if __name__ == '__main__':
    unittest.main()
