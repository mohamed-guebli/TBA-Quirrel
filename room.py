# Define the Room class.

class Room:
    '''
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

    '''

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}
    
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
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        if not self.inventory:
            return "\nIl n'y a rien ici.\n"

        inv = "\nLa pièce contient :\n"
        for item in self.inventory.values():
            inv += f"    - {item}\n"
        return inv

