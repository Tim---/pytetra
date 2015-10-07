#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ConvolutionalDecoder2_3(object):
    MAX = 0x1000

    next_output = [
        (0, 15), (11, 4), (6, 9), (13, 2),
        (5, 10), (14, 1), (3, 12), (8, 7),
        (15, 0), (4, 11), (9, 6), (2, 13),
        (10, 5), (1, 14), (12, 3), (7, 8),
    ]

    next_state = [
        (0, 1), (2, 3), (4, 5), (6, 7),
        (8, 9), (10, 11), (12, 13), (14, 15),
        (0, 1), (2, 3), (4, 5), (6, 7),
        (8, 9), (10, 11), (12, 13), (14, 15),
    ]

    def __init__(self):
        self.tab1 = [[[] for j in range(16)] for k in range(2)]
        for received in range(2):
            for oldstate in range(16):
                for input_ in range(2):
                    newstate = self.next_state[oldstate][input_]
                    output = self.next_output[oldstate][input_]
                    self.tab1[received][newstate].append((oldstate, (output >> 3) ^ received))

        self.tab2 = [[[] for j in range(16)] for k in range(4)]
        for received in range(4):
            for oldstate in range(16):
                for input_ in range(2):
                    newstate = self.next_state[oldstate][input_]
                    output = self.next_output[oldstate][input_]
                    self.tab2[received][newstate].append((oldstate, ((output >> 3) ^ (received >> 1)) + (((output >> 2) & 1) ^ (received & 1))))

    def __call__(self, b3):
        oldcost = [0] + ([self.MAX] * 15)
        cost = [0] * 16
        history = [[0 for i in xrange(16)] for j in xrange(len(b3) * 2 / 3)]

        for i in xrange(len(b3) / 3):
            received = (b3[3 * i] << 1) | b3[3 * i + 1]
            for newstate in xrange(16):
                oldstate1, c1 = self.tab2[received][newstate][0]
                c1 += oldcost[oldstate1]
                oldstate2, c2 = self.tab2[received][newstate][1]
                c2 += oldcost[oldstate2]
                if c1 < c2:
                    cost[newstate] = c1
                    history[2 * i][newstate] = oldstate1
                else:
                    cost[newstate] = c2
                    history[2 * i][newstate] = oldstate2
            oldcost = cost[:]

            received = b3[3 * i + 2]
            for newstate in xrange(16):
                oldstate1, c1 = self.tab1[received][newstate][0]
                c1 += oldcost[oldstate1]
                oldstate2, c2 = self.tab1[received][newstate][1]
                c2 += oldcost[oldstate2]
                if c1 < c2:
                    cost[newstate] = c1
                    history[2 * i + 1][newstate] = oldstate1
                else:
                    cost[newstate] = c2
                    history[2 * i + 1][newstate] = oldstate2
            oldcost = cost[:]

        # Tail bits to 0 mean we end in state 0 ?
        state = 0
        res = [0] * len(history)
        for t in xrange(len(history) - 1, - 1, -1):
            oldstate = history[t][state]
            res[t] = self.next_state[oldstate].index(state)
            state = oldstate
        return res[:-4]


# /!\ Inaccurate convolutional decoder /!\
class ConvolutionalDecoder(object):
    table = [
        [(0, 0), (1, 1)], [(3, 1), (2, 0)],
        [(4, 0), (5, 1)], [(7, 1), (6, 0)],
        [(8, 0), (9, 1)], [(11, 1), (10, 0)],
        [(12, 0), (13, 1)], [(15, 1), (14, 0)],
        [(1, 1), (0, 0)], [(2, 0), (3, 1)],
        [(5, 1), (4, 0)], [(6, 0), (7, 1)],
        [(9, 1), (8, 0)], [(10, 0), (11, 1)],
        [(13, 1), (12, 0)], [(14, 0), (15, 1)]
    ]

    def __init__(self, puncturer):
        self.puncturer = puncturer

    def __call__(self, b3):
        b3dp = list(self.puncturer.depuncture(b3))
        state = 0
        res = []
        for fb in b3dp[::4]:
            state, out = self.table[state][fb]
            res.append(out)
        return res[:-4]


if __name__ == "__main__":
    def bench_speed():
        import time

        times = 200
        start = time.time()
        for i in range(times):
            c1(b3)
        end = time.time()
        speed1 = 1000. * (end - start) / times
        print "Fast decoder : %s ms" % (speed1, )

        start = time.time()
        for i in range(times):
            c2(b3)
        end = time.time()
        speed2 = 1000. * (end - start) / times
        print "Real decoder : %s ms" % (speed2)

        print "Relative speed : %s%%" % (100 * speed1 / speed2)

    def bench_correction():
        import random
        for numerrors in range(5):
            s = 0
            for i in range(1000):
                b3e = b3[:]
                for x in random.sample(range(len(b3)), numerrors):
                    b3e[x] ^= 1
                if c2(b3e) == b2:
                    s += 1
            print numerrors, s / 1000.

    from pytetra.layer.mac.puncturer import Depuncturer_2_3
    b3 = [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0]
    b2 = [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
    c1 = ConvolutionalDecoder(Depuncturer_2_3())
    c2 = ConvolutionalDecoder2_3()

    print c2(b3) == b2

    bench_correction()
