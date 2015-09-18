#!/usr/bin/env python

# 9.4.4.3.1 Frequency correction bits
f = [1]*8 + [0]*64 + [1]*8
# 9.4.4.3.2 Normal training sequence
n = [1,1, 0,1, 0,0, 0,0, 1,1, 1,0, 1,0, 0,1, 1,1, 0,1, 0,0]
p = [0,1, 1,1, 1,0, 1,0, 0,1, 0,0, 0,0, 1,1, 0,1, 1,1, 1,0]
q = [1,0, 1,1, 0,1, 1,1, 0,0, 0,0, 0,1, 1,0, 1,0, 1,1, 0,1]
# 9.4.4.3.4 Synchronization training sequence
y = [1,1, 0,0, 0,0, 0,1, 1,0, 0,1, 1,1, 0,0, 1,1, 1,0, 1,0, 0,1, 1,1, 0,0, 0,0, 0,1, 1,0, 0,1, 1,1]

class TrainingSequenceError(Exception):
    pass

class Burst:
    def __init__(self, bits):
        self.fields = {}
        i = 0
        for name, size in self.fields_desc:
            self.fields[name] = bits[i:i+size]
            i += size
        if not(self.check()):
            raise TrainingSequenceError

    def __getattr__(self, attr):
        if attr in self.fields:
            return self.fields[attr]
        else:
            raise AttributeError

# 9.4.4.2.5 Normal continuous downlink self
class NormalContinuousDownlinkBurst(Burst):
    fields_desc = [
        ('q1', 12),
        ('ha', 2),
        ('bkn1', 216),
        ('bb1', 14),
        ('n_p', 22),
        ('bb2', 16),
        ('bkn2', 216),
        ('hb', 2),
        ('q2', 10),
    ]

    def __init__(self, bits):
        Burst.__init__(self, bits)
        self.BKN1 = self.bkn1
        self.BB = self.bb1 + self.bb2
        self.BKN2 = self.bkn2
    
    def check(self):
        return self.q2 + self.q1 == q and self.n_p in (n, p)

# 9.4.4.2.6 Synchronization continuous downlink self
class SynchronizationContinuousDownlinkBurst(Burst):
    fields_desc = [
        ('q1', 12),
        ('hc', 2),
        ('f', 80),
        ('sb', 120),
        ('y', 38),
        ('bb', 30),
        ('bkn2', 216),
        ('hd', 2),
        ('q2', 10),
    ]
    
    def __init__(self, bits):
        Burst.__init__(self, bits)
        self.SB = self.sb
        self.BB = self.bb
        self.BKN2 = self.bkn2
    
    def check(self):
        return self.q2 + self.q1 == q and self.f == f and self.y == y

# 9.4.4.2.7 Normal discontinuous downlink self
class NormalDisontinuousDownlinkBurst(Burst):
    fields_desc = [
        ('q1', 2),
        ('hg', 2),
        ('bkn1', 216),
        ('bb1', 14),
        ('n_p', 22),
        ('bb2', 16),
        ('bkn2', 216),
        ('hh', 2),
        ('q2', 2),
    ]

    def __init__(self, bits):
        Burst.__init__(self, bits)
        self.BKN1 = self.bkn1
        self.BB = self.bb1 + self.bb2
        self.BKN2 = self.bkn2

    def check(self):
        return self.q1 == q[-2:] and self.q2 == q[:2] and self.n_p in (n, p)

# 9.4.4.2.8 Synchronization discontinuous downlink self
class SynchronizationDisontinuousDownlinkBurst(Burst):
    fields_desc = [
        ('q1', 2),
        ('hi', 2),
        ('f', 80),
        ('sb', 120),
        ('y', 38),
        ('bb', 30),
        ('bkn2', 216),
        ('hj', 2),
        ('q2', 2),
    ]

    def __init__(self, bits):
        Burst.__init__(self, bits)
        self.SB = self.sb
        self.BB = self.bb
        self.BKN2 = self.bkn2

    def check(self):
        return self.q1 == q[-2:] and self.q2 == q[:2] and self.f == f and self.y == y
