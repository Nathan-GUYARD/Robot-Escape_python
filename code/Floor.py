"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame

class Floor(pygame.sprite.Sprite):
    """
    Role : Crée le sol
    """
    def __init__(self, image : pygame.Surface, pos : list[int] | tuple[int,int], group : pygame.sprite.Group) -> None:
        """
        Role : Crée un sol
        Entre : l'image (pygame.Surface), la position (list ou tuple), le group (pygame.sprite.Group)
        Sortie : Rien
        """

        super().__init__(group)

        # augmente la taille de l'image par 2
        self.image = pygame.transform.scale2x(image)
        pos = (pos[0]*2,pos[1]*2)
        
        # crée un rectangle a partir de l'image
        self.rect = self.image.get_rect(topleft = pos)

    def move(self, vector : list[int] | tuple[int,int]) -> None:
        """
        Role : Bouge le sol
        Entre : le vecteur du mouvement (list ou tuple)
        Sortie : Rien
        """

        # bouge le sol
        self.rect.x += vector[0]
        self.rect.y += vector[1]