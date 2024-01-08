"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame

from Menu import*
from Level import*

def main():
    """
    Role : lance le jeu
    Entre : Rien
    Sortie : Rien
    """

    # crée la fenetre
    pygame.init()
    pygame.display.set_caption('Robot Escape')
    screen = pygame.display.set_mode((13*32,9*32))
    
    # crée la font
    pygame.font.init()
    FONT = pygame.font.Font(pygame.font.get_default_font(), 17)

    # crée l'emplacement sur le menu des niveaux
    points = [("level1",(16,screen.get_height()//4-32//2),["level2","level4"]),
            ("level2",(screen.get_width()//3-64//2,16),["level3","level1"]),
            ("level3",(2*screen.get_width()//3-64//2,16),["level5","level2"]),
            ("level4",((screen.get_width()-64)//2,screen.get_height()//2-48),["level1","level5"]),
            ("level5",(screen.get_width()-80,(screen.get_height()-32)//2),["level3","level4","level6","level8"]),
            ("level6",(2*(screen.get_width()-64)//3,screen.get_height()-48),["level5","level7"]),
            ("level7",((screen.get_width()-64)//3,screen.get_height()-48),["level6","level9"]),
            ("level8",((screen.get_width()-64)//2,screen.get_height()//2+16),["level5","level9"]),
            ("level9",(16,3*screen.get_height()//4-32//2),["level7","level8"])]
    menu = Menu(points)
    
    inLevel = False 
    clock = pygame.Clock()

    # boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # affiche le fond
        screen.fill((155,173,183))
        
        if not inLevel:
            menu.update()
            menu.draw(screen)

        # si un niveau est lancé
        else:
            level.update()
            level.draw(screen)
            
            # si le niveau doit etre relancer
            if level.restart:
                level = Level(menu.current_level)
            
            # si le joueur a cliquer sur menu
            elif level.inMenu:
                # retourne au menu
                inLevel = False
                menu.inLevel = False
        
        # si le joueur à cliquer sur un niveau 
        if menu.inLevel and not inLevel:
            level = Level(menu.current_level)
            inLevel = True
        
        pygame.display.update()

        clock.tick(60)

main()