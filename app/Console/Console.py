from abc import ABC, abstractmethod

GREEN = "\033[92m"  # for green 
RED = '\033[91m'
BLUE = '\033[94m'

#   abstract class
class BotVeiw(ABC):
    @abstractmethod
    def output(data):
        pass


class Console(BotVeiw):
    def output(data):
        print(data)


class GreenConsole(BotVeiw):
    def output(data):
        data = f'{GREEN} {data} '
        print(data)


class RedConsole(BotVeiw):
    def output(data):
        data = f'{RED} {data} '
        print(data)


class BlueConsole(BotVeiw):
    def output(data):
        data = f'{BLUE} {data} '
        print(data)
