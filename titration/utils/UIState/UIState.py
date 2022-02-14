from abc import ABC, abstractmethod
 
# display prompts (based on array of subset)
# get menu working with tests
class UIState(ABC):
    def __init__(self, tc):
        self.tc = tc
 
    @abstractmethod
    def handleKey(self, key):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def loop(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def _setNextState(self, state):
        self.tc.setNextState(state)
