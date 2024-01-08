"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame
from pytmx.util_pygame import load_pygame

from Floor import *
from Wall import *
from Button import *
from Door import *

class MapLoader:
    """
    Role : Charge de la map
    """
    def __init__(self, level : str) -> None:
        """
        Role : charge la map
        Entré : le level (str)
        Sortie : Rien
        """

        # récupère les donnée de la map
        self.mapData = load_pygame("level/map/{}.tmx".format(level))
        
        # récupère les layers
        self.map_layer = self.mapData.layers
        
        self.floor_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.all_doors_group = {}
        self.all_buttons_group = {}
        
        # charge les couches
        self.loadLayer()
        # charge les objets
        self.loadObject()

    def loadLayer(self) -> None:
        """
        Role : Charge les couches
        Entre : Rien
        Sortie : Rien
        """
        
        # pour chaque layer
        for layer in self.map_layer:
            # si c'est le sol
            if layer.name == "floor":
                
                # stock le soL
                for x,y,img in layer.tiles():
                    pos = (x*16,y*16)
                    Floor(img,pos,self.floor_group)

            # si c'est le mur
            elif layer.name == "wall":
                
                # stock les murs
                for x,y,img in layer.tiles():
                    pos = (x*16,y*16)
                    Wall(img,pos,self.wall_group)

            
            for color in ["cyan","red","green","yellow","magenta"]:
                self.load_color_button_and_door(layer,color)
    
    def load_color_button_and_door(self, layer, color : str) -> None:
        """
        Role : Charge les bouttons et les portes d'une couleur
        Entre : La couche visiter (), la couleur (str)
        Sortie : Rien
        """
        
        # vérifie si il existe des porte de cette couleur
        if layer.name == f"{color}_door_init":
            
            # charge les portes
            self.all_doors_group[color] = self.load_color_door(color,layer)
            # charge les bouttons
            self.all_buttons_group[color] = self.load_color_button(color,self.all_doors_group[color])

    def load_color_door(self, color : str, layer) -> pygame.sprite.Group:
        """
        Role : Charge les portes d'une couleur
        Entre : la couleur (str), la couche
        Sortie : toutes les portes de la couleur (pygame.sprite.Group)
        """

        door_group = pygame.sprite.Group()

        # récupère les portes
        for x,y,img in layer.tiles():
            # récupère les images où les porte la porte est désactiver
            img_open = [self.mapData.get_tile_image(
                        x,y,list(self.mapData.layers).index(
                            self.mapData.get_layer_by_name(f"{color}_door_open")))]
            
            # récupère les images où les porte la porte est activer
            img_close = [self.mapData.get_tile_image(
                        x,y,list(self.mapData.layers).index(
                            self.mapData.get_layer_by_name(f"{color}_door_close1"))),
                    self.mapData.get_tile_image(
                        x,y,list(self.mapData.layers).index(
                            self.mapData.get_layer_by_name(f"{color}_door_close2")))]
            
            # crée la porte
            Door(img,(x*16,y*16),img_open,img_close,door_group)
        
        return door_group

    def load_color_button(self, color : str, door_group : pygame.sprite.Group) -> pygame.sprite.Group:
        """
        Role : Charge les bouttons et les portes d'une couleur
        Entre : la couleur (str), les porte de la meme couleur (pygame.sprite.Group)
        Sortie : tout les bouttons de la couleur (pygame.sprite.Group)
        """

        button_group = pygame.sprite.Group()
        
        # récupère les bouttons
        for x,y,img_off in self.mapData.get_layer_by_name(f"{color}_button_off").tiles():
            # récupère l'image où le boutton est activer
            img_on = self.mapData.get_tile_image(
                        x,y,list(self.mapData.layers).index(
                            self.mapData.get_layer_by_name(f"{color}_button_on")))

            # crée le boutton
            Button(img_off,(x*16,y*16),img_off,img_on,button_group,door_group)
            
        return button_group
    
    def loadObject(self) -> None:
        """
        Role : Charge les objets
        Entre : Rien
        Sortie : Rien
        """

        # pour toutes les objets
        for object in self.mapData.objects:

            # si c'est un point
            if object.type == "point":
                
                # si c'est le point de départ
                if object.name == "start":
                    self.start = [object.x*2,object.y*2]
                # si c'est le point d'arrivée
                elif object.name == "end":
                    self.end = [object.x*2,object.y*2]

            # si c'est des collision
            elif object.type == "collision":
                # crée une surface invisible
                noneSurafce = pygame.Surface((16,16),pygame.SRCALPHA)
                noneSurafce.fill((0,0,0,0))

                # crée un mur invisible
                Wall(noneSurafce,(object.x,object.y),self.wall_group)
    
    def get_floor(self) -> pygame.sprite.Group:
        """
        Role : récupère le sol
        Entre : Rien
        Sortie : le sol (pygame.sprite.Group)
        """

        return self.floor_group

    def get_wall(self) -> pygame.sprite.Group:
        """
        Role : récupère les murs
        Entre : Rien
        Sortie : les murs (pygame.sprite.Group)
        """

        return self.wall_group

    def get_start(self) -> list | tuple:
        """
        Role : récupère le début du niveau
        Entre : Rien
        Sortie : le début (list ou tuple)
        """

        return self.start

    def get_end(self) -> list | tuple:
        """
        Role : récupère la fin du niveau
        Entre : Rien
        Sortie : la fin (list ou tuple)
        """

        return self.end

    def get_button(self) -> dict:
        """
        Role : récupère les bouttons
        Entre : Rien
        Sortie : les bouttons (dict)
        """

        return self.all_buttons_group
    
    def get_door(self) -> dict:
        """
        Role : récupère les portes
        Entre : Rien
        Sortie : les portes (dict)
        """

        return self.all_doors_group

