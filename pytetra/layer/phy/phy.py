from pytetra.layer.phy.burst import SynchronizationContinuousDownlinkBurst, NormalContinuousDownlinkBurst, SynchronizationDisontinuousDownlinkBurst, NormalDisontinuousDownlinkBurst, TrainingSequenceError
from pytetra.timebase import g_timebase
from pytetra.layer import Layer


class Phy(Layer):
    def __init__(self, stack):
        self.stack = stack
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
            self.stack.lower_mac.tp_sb_indication(burst.SB, burst.BB, burst.BKN2)
        elif cls == NormalContinuousDownlinkBurst:
            self.stack.lower_mac.tp_ndb_indication(burst.BB, burst.BKN1, burst.BKN2, burst.SF)

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
