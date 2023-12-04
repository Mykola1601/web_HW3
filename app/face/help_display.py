from .face import UserInterface

class HelpDisplay(UserInterface):
    def disp(self, help_text):
        print(help_text)