from pytetra.logger import Logger

class Layer:
    def __init__(self):
        pass

    def warning(self, message):
        Logger.log('%s: %s' % (self.__class__.__name__, message))

    def info(self, message):
        Logger.log('%s: %s' % (self.__class__.__name__, message))
