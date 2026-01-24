class Door:
    def __init__(self, destination, locked=True, key=None):
        self.destination = destination  # room destination
        self.locked = locked  # porte verrouillée ou non
        self.key = key  # clé nécessaire pour déverrouiller la porte
