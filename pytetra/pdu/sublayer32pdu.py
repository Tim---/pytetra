from collections import OrderedDict


# PDU encoding for sublayers 3.2 (CMCE, MM, SNDCP)


class Element(object):
    name = None
    identifier = None

    def __repr__(self):
        raise NotImplementedError

    @classmethod
    def parse(cls, bits):
        raise NotImplementedError


class LeafElement(Element):
    length = None

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value


class IntElement(LeafElement):
    @classmethod
    def parse(cls, bits):
        return cls(bits.read_int(cls.length))


class BitsElement(LeafElement):
    @classmethod
    def parse(cls, bits):
        return cls(bits.read(cls.length))


class EnumElement(LeafElement):
    @classmethod
    def parse(cls, bits):
        return cls(cls.enum[bits.read_int(cls.length)])


class CompoundElement(Element):
    type1 = None
    type2 = None
    type34 = None
    sdu = False
    has_o_bit = False

    def __init__(self, *args):
        self.fields = OrderedDict()
        for elem in args:
            self.add_field(elem)

    @classmethod
    def parse(cls, bits):
        compound_element = cls()

        for elem in compound_element.type1:
            elem.decode(compound_element, bits)

        if cls.has_o_bit or compound_element.type2 or compound_element.type34:
            o_bit = bits.read_int(1)
            if o_bit:
                for elem in compound_element.type2:
                    elem.decode(compound_element, bits)

                if compound_element.type34:
                    for elem in compound_element.type34:
                        elem.decode(compound_element, bits)
                    m_bit = bits.read_int(1)

        if compound_element.sdu:
            compound_element.add_field(SduElement(bits))

        return compound_element

    def add_field(self, field):
        if isinstance(field, list):
            self.fields[field[0].__class__] = field
        else:
            self.fields[field.__class__] = field

    def __getitem__(self, item):
        return self.fields[item]

    def __repr__(self):
        return self.__class__.__name__ + '(' + ', '.join(map(repr, self.fields.values())) + ')'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.fields == other.fields
        return False


class Pdu(CompoundElement):
    has_o_bit = True


class PduDiscriminator(Pdu):
    element = None
    pdu_types = None

    @classmethod
    def parse(cls, bits):
        t = bits.peek_int(0, cls.element.length)
        return cls.pdu_types[t].parse(bits) if t in cls.pdu_types else bits


class TypeField(object):
    pass


class Type1(TypeField):
    def __init__(self, element, cond=None):
        self.element = element
        self.cond = cond

    def decode(self, parent, bits):
        if self.cond is None or self.cond(parent):
            parent.add_field(self.element.parse(bits))


class Type2(TypeField):
    def __init__(self, element, cond=None):
        self.element = element
        self.cond = cond

    def decode(self, parent, bits):
        if self.cond is None:
            p_bit = bits.read_int(1)
            if p_bit:
                parent.add_field(self.element.parse(bits))
        elif self.cond(parent):
            parent.add_field(self.element.parse(bits))


class Type3(TypeField):
    def __init__(self, element):
        self.element = element

    def decode(self, parent, bits):
        m_bit = bits.peek_int(0, 1)
        if m_bit:
            element_identifier = bits.peek_int(1, 4)
            if element_identifier == self.element.identifier:
                bits.read(5)
                length = bits.read_int(11)
                parent.add_field(self.element.parse(bits))


class Type4(TypeField):
    def __init__(self, element):
        self.element = element

    def decode(self, parent, bits):
        m_bit = bits.peek_int(0, 1)
        if m_bit:
            element_identifier = bits.peek_int(1, 4)
            if element_identifier == self.element.identifier:
                bits.read(5)
                length = bits.read_int(11)
                repeat = bits.read_int(6)
                parent.add_field([self.element.parse(bits) for r in range(repeat)])


class SduElement(BitsElement):
    @classmethod
    def parse(cls, bits):
        return cls(bits)
