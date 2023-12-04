from .face import UserInterface

class NoteDisplay(UserInterface):
    def disp(self, notes):
        for note in notes:
            print(f"Note: {note}")