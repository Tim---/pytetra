from pytetra.layer.phy.burst import Burst, SynchronizationContinuousDownlinkBurst, NormalContinuousDownlinkBurst, SynchronizationDisontinuousDownlinkBurst, NormalDisontinuousDownlinkBurst, TrainingSequenceError
from pytetra.timebase import g_timebase
from pytetra.layer import Layer


class Phy(Layer):
    def __init__(self, stack):
        super(Phy, self).__init__(stack)
        self.locked = False
        self.stream = []
        self.index = 0

    def sync(self):
        while len(self.stream) > 510 and not self.locked:
            try:
                SynchronizationContinuousDownlinkBurst(self.stream[:510])
                self.locked = True
                self.info("locked")
            except TrainingSequenceError:
                self.delete(1)

    def decode(self):
        burst = Burst.parse(self.stream[:510])

        if not burst:
            self.locked = False
            self.info("unlocked")
            return

        self.delete(510)
        g_timebase.increment()

        if isinstance(burst, SynchronizationContinuousDownlinkBurst):
            self.stack.lower_mac.tp_sb_indication(burst.sb, burst.bb, burst.bkn2)
        elif isinstance(burst, NormalContinuousDownlinkBurst):
            self.stack.lower_mac.tp_ndb_indication(burst.bb, burst.bkn1, burst.bkn2, burst.sf)

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
