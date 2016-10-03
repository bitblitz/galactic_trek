import abc
import Drawing


class IGameStage:
    __metaclass__ = abc.ABCMeta

    def run(self):
        """ Run the stage"""
        self.animate()
        Drawing.frame_ready(self.run)

    @abc.abstractmethod
    def animate(self):
        pass
