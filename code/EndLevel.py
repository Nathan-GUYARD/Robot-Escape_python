"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame
from Button_UI import *


pygame.font.init()
FONT = pygame.font.Font(pygame.font.get_default_font(), 17)

class EndLevel:
    """
    Role : Crée le menu de fin de niveau
    """
    def __init__(self, time) -> None:
        # récupère le temps que le joueur a pris pour finir le niveau 
        self.time_end = time
        self.minutes = self.time_end//60
        self.seconds = round(self.time_end%60,2)
        self.hours = int(self.minutes//60)
        self.minutes = int(self.minutes%60)

        # défini l'état initial du menu de fin
        self.menu_end = None
        self.btn_restart = None
        self.btn_menu = None

        # crée le menu de fin
        self.createEndMenu()
   
    def createEndMenu(self) -> None:
        """
        Role : Crée le menu de fin de niveau
        Entre : l'écran (pygame.Surface)
        Sortie : Rien
        """

        # le temps du joueur
        name_time_finish = FONT.render("Vous avez fini en",True,'black')
        time_finish = FONT.render(f"{self.hours}h {self.minutes}min {self.seconds:.2f}sec",True,'black')
        
        # crée la surface en arriere plan
        self.menu_end = pygame.Surface((max([name_time_finish.get_width(),time_finish.get_width()]) + 50,name_time_finish.get_height()+time_finish.get_height()+90))
        self.menu_end.fill('grey')

        # affiche le texte du joueur sur le fond 
        self.menu_end.blit(name_time_finish,((self.menu_end.get_width()-name_time_finish.get_width())//2,5))
        self.menu_end.blit(time_finish,((self.menu_end.get_width()-time_finish.get_width())//2, 10 + name_time_finish.get_height()))

        # crée les boutton
        self.btn_restart = self.createButtonEnd("Rejouer", True)
        self.btn_menu = self.createButtonEnd("Menu", False)

    def createButtonEnd(self, text : str, inLeft : bool) -> Button_UI:
        """
        Role : Crée un boutton
        Entre : le texte (str), si il est à gauche (bool)
        Sortie : le bouton (Boutton_UI) 
        """

        # crée l'arrière plan
        surf_btn = pygame.Surface((self.menu_end.get_width()//2-10,60))
        surf_btn.fill((140,140,140))

        # crée le texte
        txt_render = FONT.render(text,True,'black')
        # affiche le texte sur le fond
        surf_btn.blit(txt_render,((surf_btn.get_width()-txt_render.get_width())//2,
            (surf_btn.get_height()-txt_render.get_height())//2))

        # crée la deuxieme surface quand la souris va être sur le boutton 
        surf_btn_overlap = pygame.Surface((self.menu_end.get_width()//2-10,60))
        surf_btn_overlap.fill((150,150,150))
        surf_btn_overlap.blit(txt_render,((surf_btn.get_width()-txt_render.get_width())//2,
            (surf_btn.get_height()-txt_render.get_height())//2))
        
        # défini la position du boutton
        pos_btn = ((pygame.display.get_surface().get_width()-self.menu_end.get_width())//2 + 5 if inLeft else (pygame.display.get_surface().get_width()+self.menu_end.get_width())//2-surf_btn.get_width()-5,
            (pygame.display.get_surface().get_height()+self.menu_end.get_height())//2 - surf_btn.get_height() - 10)

        return Button_UI(surf_btn,surf_btn_overlap,pos_btn)
    
    def draw(self, screen : pygame.Surface) -> None:
        """
        Role : affiche le menu de fin de niveau
        Entre : l'écran (pygame.Surface)
        Sortie : Rien
        """

        screen.blit(self.menu_end,((screen.get_width()-self.menu_end.get_width())//2,(screen.get_height()-self.menu_end.get_height())//2))
        # affiche les bouttons
        self.btn_restart.draw(screen)
        self.btn_menu.draw(screen)

