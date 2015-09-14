#!/usr/bin/env python

# 9.4.4.3.4 Synchronization training sequence
y = [1,1, 0,0, 0,0, 0,1, 1,0, 0,1, 1,1, 0,0, 1,1, 1,0, 1,0, 0,1, 1,1, 0,0, 0,0, 0,1, 1,0, 0,1, 1,1]

class Burst:
    def __init__(self):
        pass

# 9.4.4.2.6 Synchronization continuous downlink burst
class SynchronizationContinuousDownlinkBurst(Burst):
    def __init__(self, bits):
        self.SB = bits[94:214]
    
    @classmethod
    def recognize(cls, bits):
        return bits[214:252] == y
