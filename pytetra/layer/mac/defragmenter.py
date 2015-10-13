from pytetra.layer.mac.pdu import MacResourcePdu, MacFrag, MacEnd
from pytetra.pdu.pdu import Bits


class MacDefragmenter(object):
    def __init__(self):
        self.fragments = []

    def process_pdu(self, pdu):
        if isinstance(pdu, MacResourcePdu):
            if pdu.length_indication == 63:
                self.fragments = [pdu]
            else:
                return pdu
        elif isinstance(pdu, MacFrag):
            self.fragments.append(pdu)
        elif isinstance(pdu, MacEnd):
            self.fragments.append(pdu)
            sdu = Bits(''.join(f.sdu.bits for f in self.fragments))
            pdu = self.fragments[0]
            pdu.sdu = sdu
            return pdu
