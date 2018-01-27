
class Vertex: #wierzchołek
    def __init__(self, node):
        self.id = node
        self.adjacent = {}      #sąsiadujący
        self.distance = 10 ** 100   #Ustaw odległość do nieskończoności dla wszystkich węzłów
        self.visited = False    #Zaznacz wszystkie węzły nieodwiedzone
        self.previous = None    #Poprzednik

    def add_neighbor(self, neighbor, weight=0): #dodaj sąsiedni (element, waga)
        self.adjacent[neighbor] = weight    # do słownika sąsiadujących dodaj sąsiada i ustaw wagę na ..

    def get_connections(self):  #zwróć sąsiadów
        return self.adjacent.keys() #zwróć wszystkie klucze

    def get_id(self):   #zwróć id
        return self.id

    def get_weight(self, neighbor):     #waga siąsiada
        return self.adjacent[neighbor]  #pytamy słownik z kluczem sąsiada o wagę

    def set_distance(self, dist):   #ustaw dystans (domyślnie nieskończoność)
        self.distance = dist

    def get_distance(self):     #zwróć dystans
        return self.distance

    def set_previous(self, prev):   # ustaw poprzedni wierzchołek
        self.previous = prev

    def set_visited(self):  #ustaw aktualny wierzchołek na odwiedzony
        self.visited = True

    def __str__(self):  #wyświetlanie
                        #wyświetlamy aktualne id oraz iterujemy po sąsiadach
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def __lt__(self, other): #porównujemy dystans z innym dystansem
        return self.distance < other.distance


class Graph:    #Graf zbiór wierzchołków wierzchołków
    def __init__(self):
        self.vert_dict = {}     #słownik wierzchołków
        self.num_vertices = 0   #ilość wierzchołków w grafie

    def __iter__(self):     #iteracja
        return iter(self.vert_dict.values()) #iterujemy po wartościach wszystkich wierzchołków

    def add_vertex(self, node):     #dodaj wierzchołek do grafu
        self.num_vertices = self.num_vertices + 1   #zwiększamy ilość wierzchołków w grafie o jeden
        new_vertex = Vertex(node)   #tworzymy instancje klasy wierzchołek
        self.vert_dict[node] = new_vertex   #dla klucza node przypisujemy nowy wierzchołek
        return new_vertex   #zwracamy wierzchołek

    def get_vertex(self, n):    #zwróć wierzchołek n
        if n in self.vert_dict:     #jeżeli n występuje w swłowniku wierzchołków
            return self.vert_dict[n]    #zwórć wierzchołek o kluczu n
        else:                      #jeśli nie występuje
            return None     #zwróć none

    def add_edge(self, frm, to, cost=0):    #dodaj krawędzie koszt opcionalnie to 0
        if frm not in self.vert_dict:   #jeżeli   *od* nie występuje w słowniku wierzchołków
            self.add_vertex(frm)        #dodaj nowy wierzchołek *od*   czyli gdy dodajemy pierwszy element i on nie ma udstawionego od
        if to not in self.vert_dict:    #jeśli nie występuje *do*
            self.add_vertex(to)         #dodaj wierzchołek *do*

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)  #ustaw *OD* jakos sąsiada *DO* z kosztem
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)  #ustaw *DO* jako sąsiada *OD* z kosztem
                                                                    #ponieważ "OD" jest sąsiadem "DO" i w drugą stronę
    def get_vertices(self):     #zwróć klucze słownika wierzchołków
        return self.vert_dict.keys()

    def set_previous(self, current):    #ustaw jaki poprzedniego odwiedzonego aktualnego
        self.previous = current

    def get_previous(self, current):    #zwróć poprzedniego
        return self.previous


def shortest(v, path):              #TO DO
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

import heapq
""" Algorytm kolejki sterty (kolejka priorytetowa a.k.a.).
Sterty są tablicami, dla których a [k] <= a [2 * k + 1] i a [k] <= a [2 * k + 2] dla
wszystkie k, licząc elementy od 0. Dla porównania
nieistniejące elementy są uważane za nieskończone. Ciekawe
właściwością sterty jest to, że [0] jest zawsze jej najmniejszym elementem.


heap = [] # tworzy pustą stertę
heappush (heap, item) # przesuwa nowy element na stercie
item = heappop (heap) # wyskakuje najmniejszy element ze sterty
item = heap [0] # najmniejszy element na stercie bez popping it
stackify (x) # przekształca listę w stertę, na miejscu, w czasie liniowym
item = heapreplace (heap, item) # wyskakuje i zwraca najmniejszy element, i dodaje
                                # nowy przedmiot; rozmiar sterty pozostaje niezmieniony

"""


def dijkstra(aGraph, start):        # Prima przyjmuje graf i start
    start.set_distance(0)           # Zaczynamy od ustawienia dystatnsu na zero

                          #Wstaw kolejkę  do kolejki priorytetową
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue): #dopuki wszystkie wierzchołki nie będą odwiedzone

        uv = heapq.heappop(unvisited_queue)     # Wyrzuca wierzchołek o najmniejszej odległości
        current = uv[1]     #weź pierwszy element tej tablicy
        current.set_visited()   #ustaw go na odwiedzony

        for next in current.adjacent: # pętla po elementach Sąsiednich
            if next.visited: #jeśli odwiedziłeś, pomiń
                continue
            new_dist = current.get_distance() + current.get_weight(next) #ustaw dystans na aktualny + następnego elementu

            if new_dist < next.get_distance():  #jeżeli nowy dystans jest większy o następnego dystansu  (czyli gdy to się "OPŁACA")
                next.set_distance(new_dist)     #ustaw następnemu elementowi nowy dystans
                next.set_previous(current)
                print('updated : current = %s next = %s new_dist = %s' \
                      % (current.get_id(), next.get_id(), next.get_distance()))
            else:                           #jeżeli nowy dystans jest mniejszy o następnego dystansu  (czyli gdy to się "NIEOPŁACA")
                print('not updated : current = %s next = %s new_dist = %s' \
                      % (current.get_id(), next.get_id(), next.get_distance()))

        # Przebuduj stertę
        # 1. PoP każdy przedmiot
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Umieść wszystkie wierzchołki nieodwiedzone w kolejce
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


if __name__ == '__main__':

    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b', 7)
    g.add_edge('a', 'c', 9)
    g.add_edge('a', 'f', 14)
    g.add_edge('b', 'c', 10)
    g.add_edge('b', 'd', 15)
    g.add_edge('c', 'd', 11)
    g.add_edge('c', 'f', 2)
    g.add_edge('d', 'e', 6)
    g.add_edge('e', 'f', 9)

    print('Graph data:')
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))

    dijkstra(g, g.get_vertex('a'))

    for t in ['d', 'e', 'f']:
        target = g.get_vertex(t)
        path = [t]
        shortest(target, path)
        print('The shortest path for %s : %s' % (t, path[::-1]))
