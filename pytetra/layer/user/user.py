from pytetra.layer import Layer


class UserLayer(Layer):
    def pdu_indication(self, layer, pdu):
        pass

    def speech_indication(self, block, bfi, marker):
        pass
