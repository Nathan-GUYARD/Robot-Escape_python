"""
Auteur : Nacharon
Date : 24/05/2023
"""

import pygame,sys

from Button_UI import*
from Player import*
from Graphe import*
from Level import*

class Menu:
    """
    Role : Crée le menu
    """
    def __init__(self, levels : list) -> None:
        """
        Role : Initialise le Menu
        Entre : La liste de tout les niveaux (list)
        Sortie : Rien
        """

        # créer le graphe
        levelMap = []
        for level,pos,next in levels:
            levelMap.append(LevelMapSelect(level,pos,next))
        self.graphe = Graphe(levelMap)
        
        # crée le joueur
        self.player = pygame.sprite.GroupSingle()
        Player(self.graphe.sommets["level1"].pos,self.player)
        

        self.lines = pygame.surface.Surface((pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height()),pygame.SRCALPHA)
        self.lines.fill((0,0,0,0))
        self.buttons = {}
        for level, sommet in self.graphe.sommets.items():
            
            # crée le boutton
            surf1 = pygame.Surface((64,32))
            surf1.fill((155,155,155))
            txt = FONT.render(sommet.name,True,'black')
            surf1.blit(txt,((surf1.get_width()-txt.get_width())//2,
                            (surf1.get_height()-txt.get_height())//2))

            surf2 = pygame.Surface((64,32))
            surf2.fill('darkgrey')
            surf2.blit(txt,((surf2.get_width()-txt.get_width())//2,
                            (surf2.get_height()-txt.get_height())//2))
            
            self.buttons[level] = Button_UI(surf1,surf2,sommet.pos)

            # crée les ligne entre les niveau qui sont relier
            for other_level in sommet.next:
                self.drawLine(level,other_level)

        self.isMoving = False
        self.inLevel = False

        self.vector = (0,0)
        self.i = 60

        # place le joueur au niveau 1
        self.current_level = "level1"
        self.next_level = self.current_level
        self.player.sprite.rect.x = self.buttons[self.current_level].pos[0]+self.buttons[self.current_level].surf1.get_width()//2-self.player.sprite.image.get_width()//2
        self.player.sprite.rect.y = self.buttons[self.current_level].pos[1]+self.buttons[self.current_level].surf1.get_height()//2-self.player.sprite.image.get_height()//2
        self.pos = (self.player.sprite.rect.x,self.player.sprite.rect.y)
        
    def drawLine(self, A : str, B : str) -> None:
        """
        Role : affiche une ligne entre 2 points
        Entre : le point A (str), le point B (str)
        Sortie : Rien
        """

        # récupère la position au millieu du niveau A et B
        posA = (self.graphe.sommets[A].pos[0]+32,self.graphe.sommets[A].pos[1]+16)
        posB = (self.graphe.sommets[B].pos[0]+32,self.graphe.sommets[B].pos[1]+16)
        
        # dessine la line entre les 2 niveaus
        pygame.draw.line(self.lines,'black',posA,posB,2)
        
    def draw(self, screen : pygame.Surface) -> None:
        """
        Role : affiche le menu
        Entre : l'écran (pygame.Surface) 
        Sortie : Rien
        """

        # affiche les lignes
        screen.blit(self.lines,(0,0))
        # affiche les bouttons
        for level in self.buttons:
            self.buttons[level].draw(screen)
        
        # affiche le joueur
        self.player.draw(screen)
    
    def update(self) -> None:
        """
        Role : met à jour le menu
        Entre : Rien
        Sortie : Rien
        """
        
        # récupère les input du joueur
        self.input()
        
        # bouge le joueur
        if self.isMoving:
            self.goToPath()

    def input(self) -> None:
        """
        Role : récupère les input du joueur
        Entre : Rien
        Sortie : Rien
        """

        # récupère les input de la souris
        mouse = pygame.mouse.get_pressed(3)
        
        if mouse[0] and not self.isMoving:
            pos_mouse = pygame.mouse.get_pos()
            for level, button in self.buttons.items():
                # si le bouton est cliquer
                if button.isClic(pos_mouse):
                    # si c'est un boutton ou le joeur n'est pas
                    if level == self.current_level:
                        self.inLevel = True
                    
                    # si le niveau cliquer est un autre nivaue que celui ou le joueur est
                    else:
                        self.isMoving = True
                        self.path = self.get_path(level)


    def get_path(self, level : str) -> list:
        """
        Role : récupère le chemin le plus cours
        Entre : le niveau de destination (str)
        Sortie : le chemin le plus cours (list)
        """

        # récupère le chemin le plus court
        path = self.graphe.shortestPath(self.current_level,level)
        path.pop(0)
        return path

    def get_vector(self) -> tuple:
        """
        Role : récupère le vecteur entre le nivaeu actuel et le suivant
        Entre : Rien
        Sortie : le vecteur (tuple)
        """

        return self.graphe.sommets[self.current_level].distance(self.graphe.sommets[self.next_level])
    
    def next(self) -> str:
        """
        Role : récupère le nivaeu suivant
        Entre : Rien
        Sortie : le niveau suivant (str)
        """

        # enlève le premier élement du chemin 
        return self.path.pop(0)
    
    def goTo(self) -> None:
        """
        Role : va au niveau suivant
        Entre : Rien
        Sortie : Rien
        """

        self.move(self.vector)
        self.i += 1

    def move(self, vector : list | tuple) -> None:
        """
        Role : bouge le joueur
        Entre : le vecteur de déplacement (list ou tuple)
        Sortie : Rien 
        """
        
        # stock la positon en float
        self.pos = (self.pos[0]+vector[0]/60,self.pos[1]+vector[1]/60)
        
        # change les position du joueur
        self.player.sprite.rect.x = self.pos[0]
        self.player.sprite.rect.y = self.pos[1]
    
    def goToPath(self) -> None:
        """
        Role : va au niveau sélectionner par le joueur en prenant le chemin le plus court
        Entre : Rien
        Sortie : Rien
        """

        if self.i == 60:
            self.current_level = self.next_level
            
            # si il est arriver à la destination final
            if not self.path:
                self.isMoving = False
            
            # si il reste des niveau à traversé
            else:
                self.next_level = self.next()
                self.vector = self.get_vector()
                self.i = 0

        else:
            self.goTo()
        

#------------------------------------------------
# TEST
#------------------------------------------------

if __name__ == '__main__':

    pygame.init()

    pygame.display.set_caption('Robot Escape')
    screen = pygame.display.set_mode((13*32,9*32))
    
    pygame.font.init()
    FONT = pygame.font.Font(pygame.font.get_default_font(), 17)

    points = [("level1",(16,screen.get_height()//4-32//2),["level2","level4"]),
            ("level2",(screen.get_width()//3-64//2,16),["level3","level1"]),
            ("level3",(2*screen.get_width()//3-64//2,16),["level5","level2"]),
            ("level4",((screen.get_width()-64)//2,screen.get_height()//2-48),["level1","level5"]),
            ("level5",(screen.get_width()-80,(screen.get_height()-32)//2),["level3","level4","level6","level8"]),
            ("level6",(2*(screen.get_width()-64)//3,screen.get_height()-48),["level5","level7"]),
            ("level7",((screen.get_width()-64)//3,screen.get_height()-48),["level6","level9"]),
            ("level8",((screen.get_width()-64)//2,screen.get_height()//2+16),["level5","level9"]),
            ("level9",(16,3*screen.get_height()//4-32//2),["level7","level8"])]

    test = Menu(points)
    inLevel = False 
    clock = pygame.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
        screen.fill((155,173,183))

        if not inLevel:
            test.update()
            test.draw(screen)
            
        else:
            level.update()
            level.draw(screen)
            
            if level.restart:
                level = Level(test.current_level)
            
            elif level.inMenu:
                inLevel = False
                test.inLevel = False
        
        if test.inLevel and not inLevel:
            level = Level(test.current_level)
            inLevel = True
        
        pygame.display.update()

        clock.tick(60)


