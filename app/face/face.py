from abc import ABC, abstractmethod

class UserInterface(ABC):

    @abstractmethod
    def disp(self, data):
        ...

