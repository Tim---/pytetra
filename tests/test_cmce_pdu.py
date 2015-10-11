import unittest
from pytetra.pdu.pdu import Bits
from pytetra.layer.cmce.pdu import CmcePdu, DConnect, DSetup, DRelease, DTxCeased, DCallProceeding
from pytetra.layer.cmce.elements import *


class CmceTestCase(unittest.TestCase):
    def test_dconnect(self):
        bits = '000100000000000011001110000000'
        #       *****                           PDU Type = 2 (D-CONNECT)
        #            **************             Call identifier = 6
        #                          ****         Call time-out = 7 (5 minutes)
        #                              *        Hook method selection = 0 (No hook signalling (direct through-connect))
        #                               *       Simplex/duplex selection = 0 (Simplex requested)
        #                                **     Transmission grant = 0 (Transmission granted)
        #                                  *    Transmission request permission = 0 (Allowed to request for transmission)
        #                                   *   Call ownership = 0 (Not a call owner (Group call))
        #                                    O  O-Bit = 0

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
        self.assertEqual(CmcePdu.parse(Bits(bits)), pdu)

    def test_dsetup(self):
        bits = '00111000000000001100111000000010011000001001010000000000000000011001010'
        #       *****                                                                    PDU Type = 7 (D-SETUP)
        #            **************                                                      Call identifier = 6
        #                          ****                                                  Call time-out = 7 (5 minutes)
        #                              *                                                 Hook method selection = 0 (No hook signalling (direct through-connect))
        #                               *                                                Simplex/duplex selection = 0 (Simplex requested)
        #                                ********                                        Basic service information
        #                                ...                                               Circuit mode type  = 0 (Speech: TCH/S)
        #                                   .                                              Encryption flag = 0 (Clear Mode)
        #                                    ..                                            Communication type = 1 (Point-to-multipoint)
        #                                      ..                                          Speech service = 0 (TETRA encoded speech)
        #                                        **                                      Transmission grant = 3 (Transmission granted to another user)
        #                                          *                                     Transmission request permission = 0 (Allowed to request for transmission)
        #                                           ****                                 Call priority = 0 (Priority not defined)
        #                                               O                                O-Bit = 1
        #                                                P                               P-Bit = 0
        #                                                 P                              P-Bit = 0
        #                                                  P                             P-Bit = 1
        #                                                   **                           Calling party type identifier = 1 (Short Subscriber Identity (SSI))
        #                                                     ************************   Calling party address SSI = 101
        #                                                                             M  M-Bit = 0

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
                SlotsPerFrame(0)
            ),
            TransmissionGrant('granted to another user'),
            TransmissionRequestPermission('allowed'),
            CallPriority(0),
            CallingPartyTypeIdentifier('SSI'),
            CallingPartySsi(101)
        )
        self.assertEqual(CmcePdu.parse(Bits(bits)), pdu)

    def test_drelease(self):
        bits = '0011000000000000110011100'
        #       *****                      PDU Type = 6 (D-RELEASE)
        #            **************        Call identifier = 6
        #                          *****   Disconnect cause = 14 (SwMI requested disconnection)
        #                               O  O-bit = 0

        pdu = DRelease(
            PduType('D-RELEASE'),
            CallIdentifier(6),
            DisconnectCause(14)
        )
        self.assertEqual(CmcePdu.parse(Bits(bits)), pdu)

    def test_dtxceased(self):
        bits = '010010000000000011000'
        #       *****                  PDU Type = 9 (D-TX CEASED)
        #            **************    Call identifier = 6
        #                          *   Transmission request permission = 0 (Allowed to request for transmission)
        #                           O  O-bit = 0

        pdu = DTxCeased(
            PduType('D-TX CEASED'),
            CallIdentifier(6),
            TransmissionRequestPermission('allowed')
        )
        self.assertEqual(CmcePdu.parse(Bits(bits)), pdu)

    def test_dcallproceeding(self):
        bits = '0000100000000000110110000'
        #       *****                      PDU Type = 1 (D-CALL PROCEEDING)
        #            **************        Call identifier = 6
        #                          ***     Call time-out, set-up phase = 6 (30 seconds)
        #                             *    Hook method selection = 0 (No hook signalling (direct through-connect))
        #                              *   Simplex/duplex selection = 0 (Simplex requested)
        #                               O  O-bit = 0

        pdu = DCallProceeding(
            PduType('D-CALL-PROCEEDING'),
            CallIdentifier(6),
            CallTimeoutSetUpPhase(6),
            HookMethodSelection('disabled')
        )
        self.assertEqual(CmcePdu.parse(Bits(bits)), pdu)

if __name__ == '__main__':
    unittest.main()
