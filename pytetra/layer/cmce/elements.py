from pytetra.pdu.sublayer32pdu import IntElement, EnumElement, CompoundElement, Type1, Type2, Type3, BitsElement


# 14.8.28 PDU type
class PduType(EnumElement):
    name = "PDU Type"
    length = 5
    enum = [
        "D-ALERT",
        "D-CALL-PROCEEDING",
        "D-CONNECT",
        "D-CONNECT ACKNOWLEDGE",
        "D-DISCONNECT",
        "D-INFO",
        "D-RELEASE",
        "D-SETUP",
        "D-STATUS",
        "D-TX CEASED",
        "D-TX CONTINUE",
        "D-TX GRANTED",
        "D-TX WAIT",
        "D-TX INTERRUPT",
        "D-CALL-RESTORE",
        "D-SDS-DATA",
        "D-FACILITY"] + [
        "Reserved"] * 14 + [
        "CMCE FUNCTION NOT SUPPORTED"
    ]


class Reserved(IntElement):
    name = "Encryption control"
    length = 1


# 14.8.3 Call identifier
class CallIdentifier(IntElement):
    name = "Call identifier"
    length = 14


# 14.8.16 Call time-out
class CallTimeout(IntElement):
    name = "Call timeout"
    length = 4


# 14.8.23 Hook method selection
class HookMethodSelection(EnumElement):
    name = "Hook method selection"
    length = 1
    enum = [
        "disabled",
        "enabled",
    ]


# 14.8.39 Simplex/duplex selection
class SimplexDuplexSelection(EnumElement):
    name = "Simplex/duplex selection"
    length = 1
    enum = [
        "simplex",
        "duplex",
    ]


# 14.8.42 Transmission grant
class TransmissionGrant(EnumElement):
    name = "Transmission grant"
    length = 2
    enum = [
        "granted",
        "not granted",
        "queued",
        "granted to another user"
    ]


# 14.8.43 Transmission request permission
class TransmissionRequestPermission(EnumElement):
    name = "Transmission request permission"
    length = 1
    enum = ["allowed", "disallowed"]


# 14.8.4 Call ownership
class CallOwnership(IntElement):
    name = "Call ownership"
    length = 1


# 14.8.12 Call priority
class CallPriority(IntElement):
    name = "Call priority"
    length = 4


# 14.8.17a Circuit mode type
class CircuitModeType(EnumElement):
    name = "Circuit mode type"
    length = 3
    enum = [
        "TCH/S",
        "TCH/7.2",
        "TCH/4.8, N=1",
        "TCH/4.8, N=4",
        "TCH/4.8, N=8",
        "TCH/2.4, N=1",
        "TCH/2.4, N=4",
        "TCH/2.4, N=8",
    ]


# 14.8.21 Encryption control
class EncryptionControl(EnumElement):
    name = "Encryption control"
    length = 1
    enum = [
        "clear",
        "encrypted",
    ]


# 14.8.21a Encryption flag
class EncryptionFlag(EnumElement):
    name = "Encryption flag"
    length = 1
    enum = [
        "clear",
        "encrypted",
    ]


# 14.8.17c Communication type
class CommunicationType(EnumElement):
    name = "Communication type"
    length = 2
    enum = [
        "point-to-point",
        "point-to-multipoint",
        "point-to-multipoint acknowledged",
        "broadcast",
    ]


# 14.8.39a Slots per frame
class SlotsPerFrame(IntElement):
    name = "Slots per frame"
    length = 2


# 14.8.40 Speech service
class SpeechService(EnumElement):
    name = "Speech service"
    length = 2
    enum = [
        "TETRA encoded speech",
        "Reserved",
        "Reserved",
        "Proprietary encoded speech",
    ]


# 14.8.2 Basic service information
class BasicServiceInformation(CompoundElement):
    name = "Basic service information"
    type1 = [
        Type1(CircuitModeType),
        Type1(EncryptionFlag),
        Type1(CommunicationType),
        Type1(SlotsPerFrame, cond=lambda elem: elem[CircuitModeType] != 0),
        Type1(SpeechService, cond=lambda elem: elem[CircuitModeType] == 0),
    ]
    type2 = []
    type34 = []


# 14.8.41 Temporary address
class TemporaryAddress(IntElement):
    name = "Temporary address"
    length = 24


# 14.8.27 Notification indicator
class NotificationIndicator(IntElement):
    name = "Notification indicator"
    length = 6


# 14.8.22 Facility
class Facility(IntElement):
    name = "Facility"
    length = None


# 14.8.35 Proprietary
class Proprietary(IntElement):
    name = "Proprietary"
    length = None


# 14.8.9 Calling party type identifier
class CallingPartyTypeIdentifier(EnumElement):
    name = "Calling party type identifier"
    length = 2
    enum = [
        "Reserved",
        "SSI",
        "TSI",
        "Reserved",
    ]


# 14.8.11 Calling party SSI
class CallingPartySsi(IntElement):
    name = "Calling party SSI"
    length = 24


# 14.8.10 Calling party extension
class CallingPartyExtension(IntElement):
    name = "Calling party extension"
    length = 24


# 14.8.44 Transmitting party type identifier
class TransmittingPartyTypeIdentifier(EnumElement):
    name = "Transmitting party type identifier"
    length = 2
    enum = [
        "Reserved",
        "SSI",
        "TSI",
        "Reserved",
    ]


# 14.8.46 Transmitting party SSI
class TransmittingPartySsi(IntElement):
    name = "Transmitting party SSI"
    length = 24


# 14.8.45 Transmitting party extension
class TransmittingPartyExtension(IntElement):
    name = "Transmitting party extension"
    length = 24


# 14.8.20 External subscriber number
class ExternalSubscriberNumber(IntElement):
    name = "External subscriber number"
    length = None


# 14.8.18a DM-MS address
class DmMsAddress(IntElement):
    name = "DM-MS address"
    length = None


# 14.8.18 Disconnect cause
class DisconnectCause(IntElement):
    name = "Disconnect cause"
    length = 5


# 14.8.17 Call time-out, set-up phase
class CallTimeoutSetUpPhase(IntElement):
    name = "Call time-out, set-up phase"
    length = 3


# 14.8.13 Call status
class CallStatus(IntElement):
    name = "Call status"
    length = 3


# 14.8.34 Pre-coded status
class PrecodedStatus(IntElement):
    name = "Pre-coded status"
    length = 16


# 14.8.38 Short data type identifier
class ShortDataTypeIdentifier(IntElement):
    name = "Short data type identifier"
    length = 2


# 14.8.49 User defined data-1
class UserDefinedData1(BitsElement):
    name = "User Defined Data 1"
    length = 16


# 14.8.50 User defined data-2
class UserDefinedData2(BitsElement):
    name = "User Defined Data 2"
    length = 32


# 14.8.51 User defined data-3
class UserDefinedData3(BitsElement):
    name = "User Defined Data 3"
    length = 64


# 14.8.24 Length indicator
class LengthIndicator(IntElement):
    name = "Length indicator"
    length = 11


# 14.8.52 User defined data-4
class UserDefinedData4(BitsElement):
    name = "User Defined Data 3"
    length = None


# 14.8.14 Call queued
class CallQueued(IntElement):
    name = "Call queued"
    length = 1
