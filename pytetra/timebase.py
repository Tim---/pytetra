
# 7.3 Timebase counters
class Timebase:
    def __init__(self):
        self.tn = 1 # Timeslot Number
        self.fn = 1 # TDMA Frame Number
        self.mn = 1 # TDMA Multiframe Number

    def increment(self):
        self.tn += 1
        if self.tn > 4:
            self.tn = 1
            self.fn += 1
            if self.fn > 18:
                self.fn = 1
                self.mn += 1
                if self.mn > 60:
                    self.mn = 1

    def update(self, tn, fn, mn):
        missed = 0
        while not (tn == self.tn and fn == self.fn and mn == self.mn):
            self.increment()
            missed += 1
        if missed:
            print 'Timebase : missed %s timeslots' % (missed, )

g_timebase = Timebase()
