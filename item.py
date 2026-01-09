#item.py

class Item:
    """
    
    """

    def __init__(self, name: str, descripton: str, value=None):
        self.name = name
        self.description = descripton
        self.value = value

    def __str__(self):
        return f"{self.name} : {self.description} (value: {self.value})"  