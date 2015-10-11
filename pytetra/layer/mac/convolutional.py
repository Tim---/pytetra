#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools


class ConvolutionalDecoder(object):
    MAX = 0x1000

    # Fast hamming distance functions
    diff = [
        lambda l1, l2: 0,
        lambda l1, l2: l1[0] ^ l2[0],
        lambda l1, l2: (l1[0] ^ l2[0]) + (l1[1] ^ l2[1]),
        lambda l1, l2: (l1[0] ^ l2[0]) + (l1[1] ^ l2[1]) + (l1[2] ^ l2[2]),
    ]

    def __init__(self):
        def to_bin(output):
            return tuple((output >> i) & 1 for i in range(self.out_rate - 1, -1, -1))

        # self.prevstate[newstate] = [(oldstate1, output1), (oldstate2, output2)]
        self.prevstate = [[] for j in range(self.num_states)]
        for oldstate in range(self.num_states):
            for input_ in range(2):
                newstate = self.next_state[oldstate][input_]
                output = self.next_output[oldstate][input_]
                self.prevstate[newstate].append((oldstate, to_bin(output)))

    def decode_symbol(self, received, oldcost, n):
        cost = [0] * self.num_states
        h = [0] * self.num_states

        # What is the cheaper way to get to each state ?
        for newstate in xrange(self.num_states):
            # Each state has 2 possible predecessors
            oldstate1, output1 = self.prevstate[newstate][0]
            oldstate2, output2 = self.prevstate[newstate][1]

            # Compute the cost of each state
            c1 = oldcost[oldstate1] + self.diff[n](received, output1)
            c2 = oldcost[oldstate2] + self.diff[n](received, output2)

            # The cheaper old state is written in history, and we keep its cost
            # for the next symbol decoding
            if c1 < c2:
                cost[newstate] = c1
                h[newstate] = oldstate1
            else:
                cost[newstate] = c2
                h[newstate] = oldstate2

        return cost, h

    def __call__(self, b3):
        # We begin in state 0
        oldcost = [self.MAX] * self.num_states
        oldcost[0] = 0
        history = []

        # For each symbol
        for j, n in enumerate(itertools.cycle((2, 1))):
            # We get the significant bits of the symbol (bits not punctured)
            received, b3 = b3[:n], b3[n:]

            # Symbol decoding
            oldcost, h = self.decode_symbol(received, oldcost, n)
            history.append(h)

            if not len(b3):
                break

        # We have 4 tail bits to 0, so we should end in state 0
        state = 0
        b2 = [0] * len(history)

        # Walk the history backward to get the type-2 bits
        for t in xrange(len(history) - 1, - 1, -1):
            oldstate = history[t][state]
            b2[t] = self.next_state[oldstate].index(state)
            state = oldstate

        # Remove tail bits
        return b2[:-4]


# /!\ Inaccurate convolutional decoder /!\
class FastConvolutionalDecoder(object):
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


class ConvolutionalDecoder2_3(ConvolutionalDecoder):
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

    out_rate = 4
    num_states = 16

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
    c1 = FastConvolutionalDecoder(Depuncturer_2_3())
    c2 = ConvolutionalDecoder2_3()

    print c2(b3) == b2

    bench_correction()
