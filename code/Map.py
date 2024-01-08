"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame

from Floor import *
from Wall import *

class Map:
    """
    Role : Crée la map
    """
    def __init__(self, floor : pygame.sprite.Group, walls : pygame.sprite.Group, start : list[int] | tuple[int], end : list[int] | tuple[int], doors : dict, buttons : dict) -> None:
        """
        Role : Crée la map
        Entre : le sol (pygame.sprite.Group), les murs (pygame.sprite.Group), le point de départ (list ou tuple), le point d'arrivée (list ou tuple)
        Sortie : Rien
        """

        # stock les information de la map
        self.floor = floor
        self.wall = walls
        self.start = start
        self.end = end

        # stock les porte et les bouttons
        self.all_doors = doors
        self.all_buttons = buttons

        # crée la surface de la map
        self.mapSurface = pygame.Surface((9*32,9*32))
        
    def draw(self, screen : pygame.Surface) -> None:
        """
        Role : Affiche la map
        Entre : la fenètre (pygame.Surface)
        Sortie : Rien
        """

        # affiche le sol
        self.floor.draw(self.mapSurface)
        # affiche les murs
        self.wall.draw(self.mapSurface)

        # pour chaque couleur de porte
        for color in self.all_buttons:
            # affiche les portes et les bouttons
            self.all_buttons[color].draw(self.mapSurface)
            self.all_doors[color].draw(self.mapSurface)
        
        screen.blit(self.mapSurface,(0,0))
        
    def move(self, vector : list[int] | tuple[int]) -> None:
        """
        Role : Bouge la map
        Entre : le vecteur du mouvement (list ou tuple)
        Sortie : Rien 
        """

        # bouge le sol
        for elem in self.floor:
            elem.move(vector)
            # bouge les murs
        for elem in self.wall:
            elem.move(vector)

        # bouge les points
        self.start = [self.start[0]+vector[0], self.start[1]+vector[1]]
        self.end = [self.end[0]+vector[0], self.end[1]+vector[1]]
        
        # pour chaque couleur de porte
        for color in self.all_buttons:
            # bouge les bouttons
            for button in self.all_buttons[color]:
                button.move(vector)
            # bouge les portes
            for door in self.all_doors[color]:
                door.move(vector)
            
    def update(self) -> None:
        """
        Role : met à jour la map
        Entre : Rien
        Sortie : Rien
        """

        # met à jour les portes
        for color in self.all_buttons:
            self.all_doors[color].update()
             

    def get_mapSurf(self) -> pygame.Surface:
        """
        Role : récupérer la map
        Entre : Rien
        Sortie : la map (pygame.Surface)
        """

        return self.mapSurface
        
