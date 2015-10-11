#!/usr/bin/env python

from collections import OrderedDict


class Bits(object):
    def __init__(self, bits):
        self.bits = bits

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.bits)

    def read(self, size):
        res, self.bits = Bits(self.bits[:size]), self.bits[size:]
        return res

    def read_int(self, size):
        res, self.bits = int(self.bits[:size], 2), self.bits[size:]
        return res

    def peek_int(self, start, size):
        return int(self.bits[start:start + size], 2)

    def __len__(self):
        return len(self.bits)

    def __getitem__(self, key):
        return Bits(self.bits[key])

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.bits == other.bits


class Field(object):
    pass


class UIntField(Field):
    def __init__(self, name, sz):
        self.name = name
        self.sz = sz

    def dissect(self, pkt, bits):
        return bits.read_int(self.sz)


class BitsField(Field):
    def __init__(self, name, sz=None):
        self.name = name
        self.sz = sz

    def dissect(self, pkt, bits):
        sz = self.sz or len(bits)
        return bits.read(sz)


class ConditionalField(Field):
    def __init__(self, field, cond):
        self.field = field
        self.name = field.name
        self.cond = cond

    def dissect(self, pkt, bits):
        if self.cond(pkt):
            return self.field.dissect(pkt, bits)
        else:
            return None


class Pdu(object):
    def __init__(self, bits):
        self.fields = OrderedDict()
        for field in self.fields_desc:
            self.fields[field.name] = field.dissect(self, bits)

    def __getattr__(self, attr):
        return self.fields[attr]

    def __repr__(self):
        return '<%s ' % (self.__class__.__name__, ) + \
            ' '.join('%s=%s' % item for item in self.fields.items()) + '>'


def binToInt(x):
    return int(''.join(map(str, x)), 2)


class Type1Field(Pdu):
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def dissect(self, bits):
        return bits.read_int(self.size)


class Type2Field(Pdu):
    def __init__(self, name, size, cond=None):
        self.name = name
        self.size = size
        self.cond = cond

    def dissect(self, bits):
        return bits.read_int(self.size)


class Type3Field(Pdu):
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier

    def dissect(self, bits, length):
        return bits.read_int(length)


class Type4Field(Pdu):
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier

    def dissect(self, bits, length, repetitions):
        res = []
        for i in range(repetitions):
            res.append(bits.read_int(length))
        return res


# E.1 PDU encoding rules for CMCE, MM and SNDCP PDUs
class TypedPdu(Pdu):
    def __init__(self, bits):
        self.bits = bits

        self.fields = OrderedDict()

        # Type 1
        for field in self.type1:
            self.fields[field.name] = field.dissect(self.bits)

        # Type 2
        obit = self.bits.read_int(1)
        if obit:
            for field in self.type2:
                if field.cond:
                    pbit = field.cond(self)
                else:
                    pbit = self.bits.read_int(1)
                if pbit:
                    self.fields[field.name] = field.dissect(self.bits)

            # Type 3/4
            mbit = self.bits.read_int(1)
            while mbit:
                identifier = self.bits.read_int(4)
                length = self.bits.read_int(11)
                for field in self.type3:
                    if field.identifier == identifier:
                        self.fields[field.name] = field.dissect(self.bits, length)
                for field in self.type4:
                    if field.identifier == identifier:
                        repetitions = self.bits.read_int(6)
                        self.fields[field.name] = field.dissect(self.bits, length, repetitions)
                mbit = self.bits.read_int(1)
