# item.py
# pylint: disable=no-member, no-self-argument, line-too-long, missing-function-docstring, unused-argument

class Item:
    """
    Represents an item in the game.
    """

    def __init__(self, name: str, description: str, value=None):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return f"{self.name} : {self.description} (value: {self.value})"
