"""
Module door.

Contient la classe Door, utilisée pour représenter une porte entre deux salles,
pouvant être verrouillée et nécessiter une clé spécifique.
"""


class Door: # pylint: disable=too-few-public-methods
    """
    Représente une porte reliant deux salles du jeu.

    Une porte peut être verrouillée et nécessiter un objet spécifique
    (clé, artefact, etc.) pour être déverrouillée.
    """

    def __init__(self, destination, locked=True, key=None):
        """
        Initialise une porte.

        Args:
            destination: Salle de destination vers laquelle mène la porte.
            locked (bool): Indique si la porte est verrouillée.
            key: Objet nécessaire pour déverrouiller la porte.
        """
        self.destination = destination
        self.locked = locked
        self.key = key
