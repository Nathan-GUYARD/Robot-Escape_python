"""
Auteur : Nacharon
Date : 24/05/2023
"""

from LevelMapSelect import*

class Graphe:
    """
    Role : Crée le graphe
    """
    def __init__(self, sommets : list[LevelMapSelect]) -> None:
        """
        Role : Initialise le graphe
        Entre : Les sommet (LevelMapSelect)
        Sortie : Rien
        """

        self.sommets = {}
        self.dict = {}

        # pour chaque sommets stock les successeurs du sommets
        for elem in sommets:
            self.sommets[elem.name] = elem
            
            for other_sommet in elem.next:
                self.add_path(elem.name,other_sommet)
    
    def add_path(self, A : str, B : str) -> None:    
        """
        Role : Crée le chemin entre 2 sommets
        Entre : le point A (str), le point B (str)
        Sortie : Rien
        """

        # stock qu'un successeur de A est B
        if A in self.dict:
            if not(B,1) in self.dict[A]:
                self.dict[A].append((B,1))
        else:
            self.dict[A] = [(B,1)]

        # stock qu'un successeur de B est A
        if B in self.dict:
            if not(A,1) in self.dict[B]:
                self.dict[B].append((A,1))
        else:
            self.dict[B] = [(A,1)]

    def dijkstra(self, start : str) -> dict:
        """
        Role : effectue l'algorithme de Dijkstra à partir d'un point du graphe
        Entre : le point de départ
        Sortie : le sommet duquel on arrive pour chaque sommet (dict)
        """
        
        assert start in self.dict

        novisit = set(self.dict.keys())
        # stock la seul distance connu
        distance = {start:0}
        predecesseur = {}

        # tant que tout les noeud n'ont pas été visité
        while novisit:

            # récupère le plus petit noeud non visité
            sommet = min(novisit, key = lambda x:distance.get(x,float('inf')))
            #retir le noeud des noeud non visité
            novisit.remove(sommet)

            # traite tout les successeurs du noeud si il n'a pas déjà été visité
            for elem,poid in self.dict[sommet]:
                if elem in novisit:
                    # si la distance entre le noeud et le successur est plus court
                    if distance.get(elem,float('inf')) > distance[sommet] + poid:
                        # change la distance
                        distance[elem] = distance[sommet] + poid
                        # retient le noeud précedant
                        predecesseur[elem] = sommet

        return predecesseur

    def shortestPath(self, start : str, end : str) -> list:
        """
        Role : Récupère le plus court chemin entre 2 sommets
        Entre : le point de départ (str), le point d'arriver (str)
        Sortie : les chemin le plus court (list)
        """

        assert start in self.dict and end in self.dict

        # récupère tout les chemins les plus court du graphe en partant du départ
        all_path = self.dijkstra(start)

        # stack le bon chemin en récupérent les prédécesseurs en partant de l'arrivé jusqu'à la fin
        pile = [end]
        while pile[len(pile)-1] != start:
            pile.append(all_path[pile[len(pile)-1]])

        # inverse la pile
        reverse_pile = []
        while pile:
            reverse_pile.append(pile.pop())

        return reverse_pile

#----------------------------------------------------------------------------------------------
# TEST
#----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    test = Graphe([("level1",(0,0),["level2","level4"]),
                   ("level2",(0,0),["level3","level1"]),
                   ("level3",(0,0),["level5","level2"]),
                   ("level4",(0,0),["level1","level5"]),
                   ("level5",(0,0),["level3","level4"])])
    
    print(test.dict)
    print(test.shortestPath("level1","level3"))
    
                
        
