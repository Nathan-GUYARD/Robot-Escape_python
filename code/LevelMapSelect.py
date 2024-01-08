"""
Auteur : Nacharon
Date : 24/05/2023
"""

class LevelMapSelect:
    """
    Role : Crée le niveau sur le menu
    """
    def __init__(self, name : str, pos : list | tuple, next : list[str]) -> None:
        """
        Role : Initialise le niveau qui est sur le menu
        Entre : le nom (str), la position (list ou tuple), les niveaux qui sont relier
        Sortie : Rien
        """
        
        self.name = name
        self.pos = pos
        self.next = next

    def distance(self, other_level) -> tuple:
        """
        Role : Calcule la distance entre 2 niveau sur le menu de selection
        Entre : 
        Sortie : le vecteur (tuple)
        """

        return (other_level.pos[0]-self.pos[0],other_level.pos[1]-self.pos[1])
        



