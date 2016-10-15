import abc
import Drawing


class IGameStage:
    __metaclass__ = abc.ABCMeta

    def run(self):
        """ Run the stage"""
        Drawing.animate(self.drawFrame)

    @abc.abstractmethod
    def drawFrame(self):
        pass
