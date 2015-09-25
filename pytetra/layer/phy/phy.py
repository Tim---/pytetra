from pytetra.layer import Layer
from pytetra.sap.tpsap import TpSBIndication, TpNDBIndication
from pytetra.layer.phy.burst import SynchronizationContinuousDownlinkBurst, NormalContinuousDownlinkBurst, SynchronizationDisontinuousDownlinkBurst, NormalDisontinuousDownlinkBurst, TrainingSequenceError
from pytetra.timebase import g_timebase

class Phy(Layer):
    def __init__(self, tpsap):
        Layer.__init__(self)
        self.tpsap = tpsap
        tpsap.register(self)
        self.locked = False
        self.stream = []
        self.index = 0
    
    def sync(self):
        while len(self.stream) > 510 and not self.locked:
            try:
                SynchronizationContinuousDownlinkBurst(self.stream[:510])
                self.locked = True
            except TrainingSequenceError:
                self.delete(1)

    def decode(self):
        for cls in [SynchronizationContinuousDownlinkBurst, NormalContinuousDownlinkBurst, SynchronizationDisontinuousDownlinkBurst, NormalDisontinuousDownlinkBurst]:
            try:
                burst = cls(self.stream[:510])
            except TrainingSequenceError:
                continue
            self.delete(510)
            break
        else:
            self.locked = False
            self.info("lost sync")
            return
        
        g_timebase.increment()

        if cls == SynchronizationContinuousDownlinkBurst:
            ind = TpSBIndication(burst.SB, burst.BB, burst.BKN2)
            self.tpsap.send(ind)
        elif cls == NormalContinuousDownlinkBurst:
            ind = TpNDBIndication(burst.BB, burst.BKN1, burst.BKN2, burst.SF)
            self.tpsap.send(ind)
    
    def feed(self, data):
        self.stream.extend(data)
        while len(self.stream) > 510:
            if not self.locked:
                self.sync()
            else:
                self.decode()
    
    def delete(self, size):
        del self.stream[:size]
        self.index += size
    
    def recv(self, prim):
        pass
