from pytetra.layer import Layer
from pytetra.sap.tpsap import TpUnidataIndication
from pytetra.layer.phy.burst import SynchronizationContinuousDownlinkBurst

class Phy(Layer):
    def __init__(self, tpsap):
        Layer.__init__(self)
        self.tpsap = tpsap
        tpsap.register(self)
    
    def sync(self, stream):
        while not SynchronizationContinuousDownlinkBurst.recognize(stream[:510]):
            del stream[0]

    def decode(self, stream):
        if SynchronizationContinuousDownlinkBurst.recognize(stream[:510]):
            burst = SynchronizationContinuousDownlinkBurst(stream[:510])
            ind = TpUnidataIndication(burst.SB, "BSCH")
            self.tpsap.send(ind)
            return burst
    
    def recv(self, prim):
        pass
