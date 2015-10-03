from pytetra.logger import Logger


class Layer(object):
    def __init__(self, stack):
        self.stack = stack

    def warning(self, message):
        Logger.log('%s: %s' % (self.__class__.__name__, message))

    def info(self, message):
        Logger.log('%s: %s' % (self.__class__.__name__, message))
