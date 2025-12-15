#character.py

class Character:
    """"""
    """"""

    def __init__(self):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
    
    def __str__(self):
        return f"{self.name} : {self.description} -> {self.msgs}"