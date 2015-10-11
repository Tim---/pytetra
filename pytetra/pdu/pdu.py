#!/usr/bin/env python

from collections import OrderedDict


class PduDecodingException(Exception):
    pass


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
        if isinstance(other, self.__class__):
            return self.bits == other.bits
        elif isinstance(other, str):
            return self.bits == other
        else:
            return False


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
