"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame,sys,time

from Button_UI import *
from Map import *
from Player import *
from MapLoader import *
from EndLevel import *

class Level:
    """
    Role : Crée le niveau
    """
    def __init__(self, level : str) -> None:
        """
        Role : crée le level
        Entré : le level (str)
        Sortie : Rien
        """

        # stock les informations de la map
        self.level = level
        self.speed = 2
        self.endGame = False
        self.button_put = False
        self.restart = False
        self.inMenu = False

        # charge la map
        self.map = self.mapLoader()

        self.player = pygame.sprite.GroupSingle()
        # place le joueur au debut du niveau
        self.spawn()

        self.time_start = time.perf_counter()

        self.endLevelMenu = None

        self.info = [pygame.image.load(f"asset/image/{key}.png") for key in ['z',"q","s","d","up","left","down","right","entr","f"]]
        
    def mapLoader(self) -> None:
        """
        Role : charge la map
        Entré : Rien
        Sortie : la map (Map)
        """

        mapLoad = MapLoader(self.level)
        return Map(mapLoad.get_floor(),mapLoad.get_wall(),mapLoad.get_start(),mapLoad.get_end(),mapLoad.get_door(),mapLoad.get_button())
    
    def spawn(self) -> None:
        """
        Role : Place le joueur au debut du niveau
        Entré : Rien
        Sortie : Rien
        """

        mapSurf = self.map.get_mapSurf()

        # place la camera au centre de la map
        goStart = (mapSurf.get_width()//2-self.map.start[0],mapSurf.get_height()//2-self.map.start[1])
        self.map.move(goStart)
        
        # crée le joueur
        Player((mapSurf.get_width()//2,mapSurf.get_height()//2),self.player)
        

    def draw(self, screen : pygame.Surface) -> None:
        """
        Role : affiche le niveau
        Entré : l'ecran (Surface)
        Sortie : Rien
        """

        # affiche la map
        self.map.draw(screen)
        # affiche le joueur
        self.player.draw(screen)

        x = (screen.get_width() + self.map.get_mapSurf().get_width() - 32) // 2
        for i in range(2):
            for j in range(4):
                screen.blit(self.info[j + i*4],(x + j%2*34 * (-1)**(j%3), 8+bool(j)*34 + 80*i))

            screen.blit(self.info[-(i+1)],(x,34 + 40*(i+4)))

        if self.endGame:
            # affiche les menu de fin
            self.endLevelMenu.draw(screen)

    def end(self) -> bool:
        """
        Role : verfie si le joueur est arrivée a la fin du niveau
        Entré : Rien
        Sortie : si le joueur est a la fin (bool)
        """

        # detecte si il y a colision entre le joueur et la fin du niveau
        return self.player.sprite.rect.collidepoint(self.map.end)

    def move(self, vector : list[int] | tuple[int,int]) -> None:
        """
        Role : deplace la map et verifie si le joueur peux bouger
        Entré : le sens du déplacement (list ou tuple)
        Sortie : Rien
        """

        # deplace le joueur
        self.player.sprite.move(vector)

        # stock les colision avec toutes les portes
        collid_doors = []
        for color in self.map.all_doors:
            collid_doors.extend([self.player.sprite.rect.colliderect(door.rect) and not(door.isOpen) for door in self.map.all_doors[color]])
        
        # vérifie qu' il n'y a pas de colision
        if not any([self.player.sprite.rect.colliderect(elem.rect) for elem in self.map.wall] + (collid_doors)):
            # deplace la map
            self.map.move((-vector[0],-vector[1]))

        # remet le joueur au centre
        self.player.sprite.move((-vector[0],-vector[1]))

    def input(self) -> None:
        """
        Role : récupère les input du joueur
        Entré : Rien
        Sortie : Rien
        """

        if not self.endGame:
            
            # récupère tout les input
            keys = pygame.key.get_pressed()
            
            # va a gauche
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                self.move((-self.speed,0))
                
            # va a droite
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.move((self.speed,0))

            # va en haut
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.move((0,-self.speed))
            
            # va en bas
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.move((0,self.speed))

            # active le voutton
            if (keys[pygame.K_f] or keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]) and not self.button_put:
                
                # pour chaque couleur de boutton
                for color in self.map.all_buttons:
                    
                    # vérifi si le joueur est sur un boutton
                    for button in self.map.all_buttons[color]:
                        if button.rect.collidepoint(self.player.sprite.rect.x + self.player.sprite.rect.width//2,self.player.sprite.rect.y + self.player.sprite.rect.height//2):
                            # appui sur le boutton
                            button.activate()
                            self.button_put = True

            # si le bouton n'est plus presser
            elif not(keys[pygame.K_f] or keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]):
                self.button_put = False
        
        else:
            mouse = pygame.mouse.get_pressed(3)
            pos_mouse = pygame.mouse.get_pos()
            if mouse[0]:
                if self.endLevelMenu.btn_restart.isClic(pos_mouse):
                    self.restart = True
                
                elif self.endLevelMenu.btn_menu.isClic(pos_mouse):
                    self.inMenu = True
            
    def update(self) -> None:
        """
        Role : met a jour le niveau et vérifie si c'est la fin
        Entré : Rien
        Sortie : Rien
        """
        
        self.map.update()
        # récupère les input
        self.input()
        # si le jeu est fini
        if not self.endGame:

            # vérifi si c'est fini
            if self.end():

                self.endGame = True

                self.endLevelMenu = EndLevel(time.perf_counter() - self.time_start)


#------------------------------------------------
# TEST
#------------------------------------------------

if __name__ == '__main__':

    pygame.init()

    pygame.display.set_caption('Robot Escape')
    screen = pygame.display.set_mode((15*32,9*32))
    
    pygame.font.init()
    FONT = pygame.font.Font(pygame.font.get_default_font(), 17)

    nb = 2
    level = Level(f"level{nb}")

    clock = pygame.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        level.update()
        screen.fill((155,173,183))

        level.draw(screen)
        if level.restart:
            level = Level(f"level{nb}")
        elif level.inMenu:
            nb += 1
            level = Level(f"level{nb}")
        pygame.display.update()

        clock.tick(60)