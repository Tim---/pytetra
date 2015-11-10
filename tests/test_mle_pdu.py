import unittest
from pytetra.pdu.pdu import Bits
from pytetra.pdu.sublayer32pdu import SduElement
from pytetra.layer.mle.pdu import MleServicePdu, DMleSync, DMleSysinfo
from pytetra.layer.mle.elements import *


class MleTestCase(unittest.TestCase):
    def test_mlepdu(self):
        bits = '00101010111000001010100000111010001101110000010011000000101110000100000000000000000000001001000'
        #       ***                                                                                              Protocol discriminator = 1 (MM protocol)
        #          ********************************************************************************************  SDU

        pdu = MleServicePdu(
            ProtocolDiscriminator('MM'),
            SduElement(Bits('01010111000001010100000111010001101110000010011000000101110000100000000000000000000001001000'))
        )
        self.assertEqual(MleServicePdu.parse(Bits(bits)), pdu)

    def test_dmlesync(self):
        bits = '00000000010000000000000110001'
        #       **********                     MCC = 1
        #                 **************       MNC = 1
        #                               ==     Neighbour cell broadcast
        #                               *      D-NWRK-BROADCAST broadcast supported = 1 (Supported)
        #                                *     D-NWRK-BROADCAST enquiry supported = 0 (Not supported)
        #                                 **   Cell service level = 0 (Cell load unknown)
        #                                   *  Late entry information = 1 (Late entry available)

        pdu = DMleSync(
            Mcc(1),
            Mnc(1),
            NeighbourCellBroadcast(2),
            CellServiceLevel('unknown'),
            LateEntrySupported('available')
        )
        self.assertEqual(DMleSync.parse(Bits(bits)), pdu)

    def test_dmlesysinfo(self):
        bits = '000000000000011111111111111111110100100101'
        #       **************                             LA = 1
        #                     ****************             Subscriber class = Member of all classes
        #                                     ============ BS service details
        #                                     *            Registration = 1 (Registration mandatory on this cell)
        #                                      *           De-registration = 1 (De-registration mandatory on this cell)
        #                                       *          Priority cell = 0 (Cell is not a priority cell)
        #                                        *         Minimum mode service = 1 (Cell never uses minimum mode)
        #                                         *        Migration = 0 (Migration is not supported by this cell)
        #                                          *       System wide services = 0 (System wide services temporarily not supported)
        #                                           *      TETRA voice service = 1 (TETRA voice service is supported on this cell)
        #                                            *     Circuit mode data service = 0 (Circuit mode data service is not supported on this cell)
        #                                             *    Reserved = 0 (Service is not available on this cel)
        #                                              *   SNDCPService = 1 (SNDCP service is available on this cell)
        #                                               *  Air interface encryption service = 0 (Air interface encryption is not available on this cell)
        #                                                * Advanced link supported = 1 (Advanced link is supported on this cell)

        pdu = DMleSysinfo(
            La(1),
            SubscriberClass(65535),
            BsServiceDetails(
                BsServiceRegistration(1),
                BsServiceDeregistration(1),
                BsServicePriorityCell(0),
                BsServiceMinimumMode(1),
                BsServiceMigration(0),
                BsServiceSystemWide(0),
                BsServiceTetraVoice(1),
                BsServiceCircuitModeData(0),
                BsServiceReserved(0),
                BsServiceSndcp(1),
                BsServiceEncryption(0),
                BsServiceAdvancedLink(1)
            )
        )
        self.assertEqual(DMleSysinfo.parse(Bits(bits)), pdu)


if __name__ == '__main__':
    unittest.main()
