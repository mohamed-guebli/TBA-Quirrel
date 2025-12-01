# Define the Player class.
class Player():
    '''
    This class represents a player in the game. A player has a name and a current room.

    Attributes:
        name(str) : The name.
        current_room(Room) : The current room.

    Methods:
        __init__(self,name) : The constructor.
        move(self,direction) : Move the player in the given direction.

    Examples:
    >>> player = Player("Hero")
    >>> player.name
    'Hero'
    >>> player.current_room is None
    True
    >>> from room import Room
    >>> room1 = Room("Salle de départ", "dans la salle de départ", {})
    >>> room2 = Room("Salle de nord", "dans la salle au nord", {})
    >>> room1.exits['N'] = room2
    >>> player.current_room = room1
    >>> player.move('N')
    '\nVous êtes dans la salle au nord\n\nSorties: \n'
    >>> player.current_room == room2
    True    
        
    '''
    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        self.history.append(next_room)
        print(self.current_room.get_long_description())
        self.get_history()
        return True

    def get_history(self):
        if not self.history:
            return
        
        print("\nVous avez déja visité les pièces suivantes:")
        for room in self.history:
            print(f"    - {room.name}")


    