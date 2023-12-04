from .face import UserInterface

class ContactDisplay(UserInterface):
    def disp(self, contacts):
        for contact in contacts:
            print(f"Contact: {contact}")