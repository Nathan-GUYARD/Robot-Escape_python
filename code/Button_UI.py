"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame

class Button_UI:
    """
    Role : Crée le boutton où l'utilisateur peut cliquer
    """
    def __init__(self, surf1 : pygame.Surface, surf2 : pygame.Surface, pos : list[int] | tuple[int,int]) -> None:
        """
        Role : Crée le boutton 
        Entre : la surface par défaut (pygame.Surface), la surface quand la souris sera sur la boutton(pygame.Surface), la position du boutton
        Sortie : Rien
        """

        # stock les information du boutton
        self.pos = pos
        self.surf1 = surf1
        self.surf2 = surf2
    
    def draw(self, surface : pygame.Surface) -> None:
        """
        Role : 
        Entre : la surface sur laquelle le boutton est afficher (pygame.Surface)
        Sortie : Rien
        """

        # si la souris n'est pas sur le boutton
        if not(self.isOverlaping()):
            # afficher la surface normal
            surface.blit(self.surf1,self.pos)

        else:
            # afficher la deuxieme surface
            surface.blit(self.surf2,self.pos)

    def isClic(self, pos : list[int] | tuple[int,int]) -> bool:
        """
        Role : Vérifie si le boutton est cliqué
        Entre : la position de la souris (list ou tuple)
        Sortie : si le boutton est cliqué (bool)
        """

        # si la souris est sur le boutton
        return self.surf1.get_rect(topleft=self.pos).collidepoint(pos)

    def isOverlaping(self):
        """
        Role : Vérifie la souris est sur le boutton
        Entre : Rien
        Sortie : si la souris est sur le boutton (bool)
        """
        
        # si la souris est sur le boutton
        return self.surf1.get_rect(topleft=self.pos).collidepoint(pygame.mouse.get_pos())