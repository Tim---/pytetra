from collections import OrderedDict


# PDU encoding for sublayers 3.2 (CMCE, MM, SNDCP)


class Element(object):
    name = None
    identifier = None

    def __init__(self, bits):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class LeafElement(Element):
    length = None

    def __init__(self, bits):
        self._value = bits.read_int(self.length)

    def __repr__(self):
        return '"%s" = %s' % (self.name, self.value())

    def value(self):
        return self._value


class CompoundElement(Element):
    type1 = None
    type2 = None
    type34 = None

    def __init__(self, bits):
        self.fields = OrderedDict()

        for elem in self.type1:
            elem.decode(self, bits)

        if self.type2 or self.type34:
            o_bit = bits.read_int(1)
            if o_bit:
                for elem in self.type2:
                    elem.decode(self, bits)

                if self.type34:
                    for elem in self.type34:
                        elem.decode(self, bits)
                    m_bit = bits.read_int(1)

    def add_field(self, field):
        if isinstance(field, list):
            self.fields[field[0].name] = field
        else:
            self.fields[field.name] = field

    def __getitem__(self, item):
        return self.fields[item]

    def __repr__(self):
        return '<' + self.name + ' ' + ', '.join(map(repr, self.fields.values())) + '>'


class Pdu(CompoundElement):
    pass


class PduDiscriminator(Pdu):
    length = None
    pdu_types = None

    def __new__(cls, bits):
        t = bits.peek_int(0, cls.length)
        return cls.pdu_types[t](bits) if t in cls.pdu_types else None


class TypeField(object):
    pass


class Type1(TypeField):
    def __init__(self, element, cond=None):
        self.element = element
        self.cond = cond

    def decode(self, parent, bits):
        if self.cond is None or self.cond(parent):
            parent.add_field(self.element(bits))


class Type2(TypeField):
    def __init__(self, element, cond=None):
        self.element = element
        self.cond = cond

    def decode(self, parent, bits):
        if self.cond is None:
            p_bit = bits.read_int(1)
            if p_bit:
                parent.add_field(self.element(bits))
        elif self.cond(parent):
            parent.add_field(self.element(bits))


class Type3(TypeField):
    def __init__(self, element):
        self.element = element

    def decode(self, parent, bits):
        m_bit = bits.peek_int(0, 1)
        if m_bit:
            element_identifier = bits.peek_int(1, 4)
            if element_identifier == self.element.identifier:
                bits.forward(5)
                length = bits.read_int(11)
                parent.add_field(self.element(bits))


class Type4(TypeField):
    def __init__(self, element):
        self.element = element

    def decode(self, parent, bits):
        m_bit = bits.peek_int(0, 1)
        if m_bit:
            element_identifier = bits.peek_int(1, 4)
            if element_identifier == self.element.identifier:
                bits.forward(5)
                length = bits.read_int(11)
                repeat = bits.read_int(6)
                parent.add_field([self.element(bits) for r in range(repeat)])
