"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame

class Door(pygame.sprite.Sprite):
    """
    Role : Crée la porte
    """
    def __init__(self, surf : pygame.Surface, pos : list[int] | tuple[int,int], surf_open : list[pygame.Surface] | tuple[pygame.Surface], surf_close : list[pygame.Surface] | tuple[pygame.Surface], group : pygame.sprite.Group) -> None:
        """
        Role : Initialise la porte
        Entre : la surface de départ (pygame.Surface), la position (list ou tuple), surface de la porte ouverte (list ou tuple), surface de la porte fermer (list ou tuple), le groupe (pygame.sprite.Group)
        Sortie : Rien
        """

        super().__init__(group)

        # regarde si la porte est ouverte ou fermer
        self.isOpen = surf in surf_open

        # stock les images quand la porte est ouverte
        self.images_open = []
        for img in surf_open:
            self.images_open.append(pygame.transform.scale2x(img))

        # stock les images quand la porte est fermer
        self.images_close = []
        for img in surf_close:
            self.images_close.append(pygame.transform.scale2x(img))
        
        # augmente la taille de l'image par 2
        self.image = pygame.transform.scale2x(surf)
        pos = (pos[0]*2,pos[1]*2)
        
        # crée un rectangle a partir de l'image
        self.rect = self.image.get_rect(topleft = pos)

        self.id_image = 0

    def move(self, vector : list[int] | tuple[int,int]) -> None:
        """
        Role : Bouge la porte
        Entre : le vecteur du mouvement (list ou tuple)
        Sortie : Rien
        """
        
        # bouge la porte
        self.rect.x += vector[0]
        self.rect.y += vector[1]
    
    def switch(self) -> None:
        """
        Role : Change l'état de la porte
        Entre : Rien
        Sortie : Rien
        """

        self.id_image = 0
        self.isOpen = not(self.isOpen)
    
    def animation(self) -> None:
        """
        Role : Anime la porte
        Entre : Rien
        Sortie : Rien
        """
        
        # affiche la porte ouverte
        if self.isOpen:
            self.image = self.images_open[int(self.id_image)]

        # affiche la porte fermer
        else:
            self.image = self.images_close[int(self.id_image)]
            
            self.id_image += 0.1
            if self.id_image >= 2:
                self.id_image = 0
            
    
    def update(self) -> None:
        """
        Role : Met à jour la porte
        Entre : Rien 
        Sortie : Rien
        """
        
        self.animation()
        