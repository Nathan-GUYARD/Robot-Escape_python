"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame

class Player(pygame.sprite.Sprite):
    """
    Role : Crée le joueur
    """
    def __init__(self, pos : list | tuple, group : pygame.sprite.GroupSingle) -> None:
        """
        Role : Initialise le joueur
        Entre : le position (list ou tuple), le groupe (pygame.sprite.GroupSingle)
        Sortie : Rien
        """

        super().__init__(group)
        self.image = pygame.Surface((24,24))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = pos)
        
    def move(self, vector : list | tuple) -> None:
        """
        Role : Bouge le joueur
        Entre : le vecteur (list ou tuple)
        Sortie : Rien
        """

        self.rect.x += vector[0]
        self.rect.y += vector[1]