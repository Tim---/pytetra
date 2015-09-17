from pytetra.layer import Layer
from pytetra.sap.tpsap import TpUnidataIndication
from pytetra.layer.phy.burst import SynchronizationContinuousDownlinkBurst, NormalContinuousDownlinkBurst, SynchronizationDisontinuousDownlinkBurst, NormalDisontinuousDownlinkBurst, TrainingSequenceError

class Phy(Layer):
    def __init__(self, tpsap):
        Layer.__init__(self)
        self.tpsap = tpsap
        tpsap.register(self)
        self.locked = False
        self.stream = []
    
    def sync(self):
        while len(self.stream) > 510 and not self.locked:
            try:
                SynchronizationContinuousDownlinkBurst(self.stream[:510])
                self.locked = True
            except TrainingSequenceError:
                del self.stream[0]

    def decode(self):
        for cls in [SynchronizationContinuousDownlinkBurst, NormalContinuousDownlinkBurst, SynchronizationDisontinuousDownlinkBurst, NormalDisontinuousDownlinkBurst]:
            try:
                burst = cls(self.stream[:510])
                print cls
                del self.stream[:510]
                break
            except TrainingSequenceError:
                pass
        else:
            print "lost sync"
            self.locked = False
            return
        if cls == SynchronizationContinuousDownlinkBurst:
            #burst = SynchronizationContinuousDownlinkBurst(self.stream[:510])
            ind = TpUnidataIndication(burst.SB, "BSCH")
            self.tpsap.send(ind)
            self.locked = True
    
    def feed(self, data):
        self.stream.extend(data)
        while len(self.stream) > 510:
            if not self.locked:
                self.sync()
            else:
                self.decode()
            
    
    def recv(self, prim):
        pass
