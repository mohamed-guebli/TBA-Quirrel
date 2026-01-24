# Define the Room class.
# pylint: disable=no-member, no-self-argument, line-too-long, missing-function-docstring, unused-argument

class Room:
    """
    This class represents a room in the game. A room is composed of
    a name, a description and exits.

    Attributes:
        name(str): The name.
        description(str): The description.
        exits(dict) : The exits.

    Methods:
        __init__(self,name,description) : The constructor.
        get_exit(self, direction) : Return the room in the given direction.
        get_exit_string(self) : Return a string describing the room's exits.
        get_long_description(self) : Return a long description of this room including exits.

    Examples:

    >>> room = Room("Salle de départ", "dans la salle de départ", {} )
    >>> room.name
    'Salle de départ'
    >>> room.description
    'dans la salle de départ'
    >>> room.exits
    {}

    """

    # Define the constructor.
    def __init__(self, name, description, dark=False):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}
        self.dark = dark

    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None

    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: "
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nQuirrel se trouve {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        if not self.inventory:
            return "\nIl n'y a rien ici.\n"

        inv = "\nLa pièce contient :\n"
        for item in self.inventory.values():
            inv += f"    - {item}\n"
        return inv

    def get_characters(self, characters):

        present = [
            c
            for c in characters
            if c.current_room == self and (not c.defeated or not c.is_boss)
        ]

        if not present:
            return "\nIl n'y a personne ici.\n"

        txt = "\nVous voyez ici :\n"
        for c in present:
            txt += f"    - {c}\n"
        return txt
