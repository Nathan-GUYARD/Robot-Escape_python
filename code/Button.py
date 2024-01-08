"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame

class Button(pygame.sprite.Sprite):
    """
    Role : Crée le boutton
    """
    def __init__(self, surf : pygame.Surface, pos : list[int] | tuple[int,int], surf_off : pygame.Surface, surf_on : pygame.Surface, group : pygame.sprite.Group, door_group : pygame.sprite.Group) -> None:
        """
        Role : Initialise le boutton
        Entre : la surface de départ (pygame.Surface), la position (list ou tuple), surface du boutton pas appuier (pygame.Surface), surface du boutton appuier (pygame.Surface), le groupe (pygame.sprite.Group), les portes affecter par le boutton (pygame.sprite.Group)
        Sortie : Rien
        """
        
        super().__init__(group)

        # staock les images du boutton
        self.images_off = pygame.transform.scale2x(surf_off)
        self.images_on = pygame.transform.scale2x(surf_on)

        # augmente la taille de l'image par 2
        self.image = pygame.transform.scale2x(surf)
        pos = (pos[0]*2,pos[1]*2)
        
        # crée un rectangle a partir de l'image
        self.rect = self.image.get_rect(topleft = pos)

        self.isActivate = False
        self.door_group = door_group

    def move(self, vector : list[int] | tuple[int,int]) -> None:
        """
        Role : Bouge la porte
        Entre : le vecteur du mouvement (list ou tuple)
        Sortie : Rien
        """
        
        # bouge la porte
        self.rect.x += vector[0]
        self.rect.y += vector[1]

    def activate(self) -> None:
        """
        Role : Appui sur le boutton
        Entre : Rien
        Sortie : Rien
        """
        
        # change l'état du boutton
        self.isActivate = not(self.isActivate)

        # affiche l'image du boutton enfoncer
        if self.isActivate:
            self.image = self.images_on
        
        # affiche l'image du boutton normal
        else:
            self.image = self.images_off
        
        # change l'état des portes
        for door in self.door_group:
            door.switch()
