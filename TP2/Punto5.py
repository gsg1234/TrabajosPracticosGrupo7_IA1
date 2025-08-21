import pygame
import sys
import heapq
import time
from collections import deque

# -------------------------------
# Definición del grafo y funciones
# -------------------------------

coordenadas = {
    'A': (3, 3), 'B': (4, 3),
    'C': (3, 2), 'D': (4, 2), 'E': (5, 2),
    'G': (0, 1), 'I': (1, 1), 'W': (2, 1), 'K': (3, 1), 'M': (4, 1), 'N': (5, 1),
    'P': (0, 0), 'Q': (1, 0), 'R': (2, 0), 'T': (3, 0), 'F': (4, 0)
}

paredes = [
    ('W', 'R'), ('T', 'F'), ('C', 'D'), ('D', 'E')
]

costos = {letra: 1 for letra in coordenadas.keys()}
costos['W'] = 30

INICIO = 'I'
FIN = 'F'

def manhattan(a, b):
    ra, ca = coordenadas[a]
    rb, cb = coordenadas[b]
    return abs(ra - rb) + abs(ca - cb)

def vecinos(celda):
    r, c = coordenadas[celda]
    vecinos_validos = []
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r + dr, c + dc
        if (nr, nc) in coordenadas.values():
            vecino = [k for k,v in coordenadas.items() if v == (nr, nc)][0]
            if (celda, vecino) not in paredes and (vecino, celda) not in paredes:
                vecinos_validos.append(vecino)
    return sorted(vecinos_validos)

# Algoritmos de búsqueda
def dfs(inicio, objetivo):
    pila = [(inicio, [inicio])]
    visitados = set()
    while pila:
        actual, camino = pila.pop()
        if actual == objetivo:
            return camino
        if actual in visitados:
            continue
        visitados.add(actual)
        for vecino in sorted(vecinos(actual), reverse=True):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))
    return None

def busqueda_avara(inicio, objetivo):
    frontera = []
    heapq.heappush(frontera, (manhattan(inicio, objetivo), inicio, [inicio]))
    visitados = set()
    while frontera:
        _, actual, camino = heapq.heappop(frontera)
        if actual == objetivo:
            return camino
        if actual in visitados:
            continue
        visitados.add(actual)
        for vecino in sorted(vecinos(actual)):
            if vecino not in visitados:
                h = manhattan(vecino, objetivo)
                heapq.heappush(frontera, (h, vecino, camino + [vecino]))
    return None

def busqueda_a_estrella(inicio, objetivo):
    frontera = []
    heapq.heappush(frontera, (manhattan(inicio, objetivo), 0, inicio, [inicio]))
    visitados = {}
    while frontera:
        f, g, actual, camino = heapq.heappop(frontera)
        if actual == objetivo:
            return camino
        if actual in visitados and visitados[actual] <= g:
            continue
        visitados[actual] = g
        for vecino in sorted(vecinos(actual)):
            nuevo_g = g + costos[vecino]
            h = manhattan(vecino, objetivo)
            nuevo_f = nuevo_g + h
            heapq.heappush(frontera, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
    return None

# -------------------------------
# Interfaz con pygame
# -------------------------------

pygame.init()

CELL_SIZE = 80
WIDTH = (max(x for x, _ in coordenadas.values()) + 1) * CELL_SIZE
HEIGHT = (max(y for _, y in coordenadas.values()) + 1) * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animación de algoritmos de búsqueda")

FONT = pygame.font.SysFont("Arial", 20)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE  = (0, 0, 200)
YELLOW= (255, 255, 0)
ORANGE= (255, 165, 0)
CYAN  = (0, 200, 200)
GREY  = (200, 200, 200)

def draw_board(path=None, color=YELLOW):
    screen.fill(WHITE)

    # Dibujar celdas
    for letra, (x, y) in coordenadas.items():
        rect = pygame.Rect(x*CELL_SIZE, HEIGHT-(y+1)*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREY, rect, 1)

        # Inicio y Fin
        if letra == INICIO:
            pygame.draw.rect(screen, GREEN, rect)
        elif letra == FIN:
            pygame.draw.rect(screen, BLUE, rect)

        # Etiqueta
        text = FONT.render(letra, True, BLACK)
        screen.blit(text, (rect.x+CELL_SIZE//3, rect.y+CELL_SIZE//3))

        if costos[letra] > 1:
            cost_text = FONT.render(str(costos[letra]), True, RED)
            screen.blit(cost_text, (rect.x+5, rect.y+5))

    # Dibujar paredes
    for a, b in paredes:
        xa, ya = coordenadas[a]
        xb, yb = coordenadas[b]
        x1, y1 = xa*CELL_SIZE, HEIGHT-(ya+1)*CELL_SIZE
        x2, y2 = xb*CELL_SIZE, HEIGHT-(yb+1)*CELL_SIZE
        if xa == xb:  # pared horizontal
            px = xa*CELL_SIZE
            py = min(y1, y2) + CELL_SIZE
            pygame.draw.line(screen, RED, (px, py), (px+CELL_SIZE, py), 5)
        else:  # pared vertical
            px = min(x1, x2) + CELL_SIZE
            py = y1
            pygame.draw.line(screen, RED, (px, py), (px, py+CELL_SIZE), 5)

    # Dibujar camino parcial si existe
    if path:
        for i in range(len(path)-1):
            x1, y1 = coordenadas[path[i]]
            x2, y2 = coordenadas[path[i+1]]
            cx1, cy1 = x1*CELL_SIZE+CELL_SIZE//2, HEIGHT-(y1+1)*CELL_SIZE+CELL_SIZE//2
            cx2, cy2 = x2*CELL_SIZE+CELL_SIZE//2, HEIGHT-(y2+1)*CELL_SIZE+CELL_SIZE//2
            pygame.draw.line(screen, color, (cx1, cy1), (cx2, cy2), 5)

def animar_camino(camino, color, nombre):
    for i in range(1, len(camino)+1):
        draw_board(camino[:i], color)
        titulo = FONT.render(nombre, True, BLACK)
        screen.blit(titulo, (10, 10))
        pygame.display.flip()
        time.sleep(0.5)

# Ejecutar algoritmos
camino_dfs = dfs(INICIO, FIN)
camino_avara = busqueda_avara(INICIO, FIN)
camino_astar = busqueda_a_estrella(INICIO, FIN)

print("Búsqueda Primero en Profundidad:", camino_dfs)
print("Búsqueda Avara:", camino_avara)
print("Búsqueda A*:", camino_astar)

# -------------------------------
# Animación secuencial
# -------------------------------
running = True
while running:
    animar_camino(camino_dfs, YELLOW, "DFS")
    time.sleep(1)
    animar_camino(camino_avara, ORANGE, "Búsqueda Ávara")
    time.sleep(1)
    animar_camino(camino_astar, CYAN, "A*")
    time.sleep(2)
    running = False  # Termina después de mostrar todo

pygame.quit()
sys.exit()
