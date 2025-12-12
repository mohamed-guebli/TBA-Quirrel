#item.py

class Item:
    """
    
    """

    def __init__(self, name: str, descripton: str, weight):
        self.name = name
        self.description = descripton
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} (weight: {self.weight})"  