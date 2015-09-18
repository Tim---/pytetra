#!/usr/bin/env python
# -*- coding: utf-8 -*-

def toBin(x, n):
    return map(int, bin(x)[2:].zfill(n))

def chunk(l, n):
    for i in range(len(l)/n):
        yield l[n*i:n*(i+1)]

def binDiff(a, b):
    return sum([1 for i,j in zip(a, b) if i != j and i is not None and j is not None])

class ConvolutionalEncoder:
    def __init__(self, N, K, next_output, next_state):
        self.N = N
        self.K = K
        self.next_output = next_output
        self.next_state = next_state
        self.nstates = 2 ** (K - 1)
        self.state = 0
    
    def encodeBit(self, b):
        out = self.next_output[self.state][b]
        self.state = self.next_state[self.state][b]
        return out
    
    def encode(self, bits):
        for b in bits:
            for i in toBin(self.encodeBit(b), self.N):
                yield i

    # Alors en gros...
    # Le but c'est de remplir un gros tableau (bit d'entrée, état)
    # On lit chaque symbole, et on regarde toutes les combinaisons
    
    # Au début, on sait qu'on est dans l'état 0
    # Du coup on a deux outputs possibles : 0 et 15
    # On sait que c'est le symbole qui s'en rapproche le plus qui "gagne"
    def decode(self, bits):
        ae = [0x100000]*self.nstates
        ae[0] = 0
        state_history = [[0]*self.nstates for i in range(len(bits)/self.N)]
        for i, sym in enumerate(chunk(bits, self.N)):
            ae_next = [0x100000]*self.nstates
            # For each possible state and input combo
            for s in range(self.nstates):
                for b in (0, 1):
                    out = toBin(self.next_output[s][b], self.N)
                    state = self.next_state[s][b]
                    # On regarde la différence entre le out et le out simulé
                    nae = ae[s] + binDiff(sym, out)
                    if nae < ae_next[state]:
                        ae_next[state] = nae
                        state_history[i][state] = s
            ae = ae_next

        # get output
        cur_state = min(range(len(ae)), key=lambda i: ae[i])
        res = []
        for i in reversed(range(len(bits)/self.N)):
            min_state = cur_state
            cur_state = state_history[i][cur_state]
            
            #print next_state[cur_state][0], next_state[cur_state][1], min_state
            if self.next_state[cur_state][0] == min_state:
                res.append(0)
            elif self.next_state[cur_state][1] == min_state:
                res.append(1)
            else:
                print '?'
        res.reverse()
        return res

class TETRAConvolutionalEncoder(ConvolutionalEncoder):
    def __init__(self):
        N = 4
        K = 5
        next_output = [
            (  0, 15 ), ( 11,  4 ), (  6,  9 ), ( 13,  2 ),
            (  5, 10 ), ( 14,  1 ), (  3, 12 ), (  8,  7 ),
            ( 15,  0 ), (  4, 11 ), (  9,  6 ), (  2, 13 ),
            ( 10,  5 ), (  1, 14 ), ( 12,  3 ), (  7,  8 ),
        ]

        next_state = [
            (  0,  1 ), (  2,  3 ), (  4,  5 ), (  6,  7 ),
            (  8,  9 ), ( 10, 11 ), ( 12, 13 ), ( 14, 15 ),
            (  0,  1 ), (  2,  3 ), (  4,  5 ), (  6,  7 ),
            (  8,  9 ), ( 10, 11 ), ( 12, 13 ), ( 14, 15 ),
        ]
        ConvolutionalEncoder.__init__(self, N, K, next_output, next_state)

        
if __name__ == "__main__":

    c = TETRAConvolutionalEncoder()
    #b2 = [1, 0, 0, 0, 1, 0, 1]
    b2 = [1, 0, 1, 1, 0, 1, 0]
    v = list(c.encode(b2))
    print v
    #v[2] = 0
    print c.decode(v)
