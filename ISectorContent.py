import abc


class ISectorContent:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def asChar(self):
        """return the single character display letter for the object type"""
        return ''
