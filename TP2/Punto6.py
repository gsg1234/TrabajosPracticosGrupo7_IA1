import pygame
import heapq

#Se inicia el juego con la imagen de obstáculos y se implementa el algoritmo A* para encontrar el camino más corto desde un punto de inicio a un punto objetivo, evitando los obstáculos.
# El usuario puede hacer clic para seleccionar el punto de inicio y el objetivo, y el algoritmo calculará el camino más corto, que se mostrará en verde. Los obstáculos se muestran en negro
# y el punto de inicio y objetivo en azul y amarillo, respectivamente.


# --- Configuración ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 17, 17
CELL_SIZE = WIDTH // COLS

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 50)
GREEN = (0, 120, 0)
RED = (255, 0, 0)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding")

# --- Crear tablero vacío ---
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# --- Obstáculos según la imagen (puedes cambiarlo) ---
# columna central y base en L
for r in range(4, 15):
    grid[r][8] = 1
for c in range(9, 12):
    grid[14][c] = 1
grid[2][10] = 1
grid[3][9] = 1

# --- Funciones de dibujo ---
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE
            if grid[r][c] == 1:
                color = BLACK
            pygame.draw.rect(win, color, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(win, BLACK, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_path(path):
    for (r, c) in path:
        pygame.draw.rect(win, GREEN, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

# --- A* ---
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            path.remove(goal)  # Remove the goal from the path
            return path

        r, c = current
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            neighbor = (nr, nc)
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 0:
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

# --- Main loop ---
running = True
start = None
goal = None
path = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            r, c = y // CELL_SIZE, x // CELL_SIZE
            if start is None:
                start = (r, c)
            elif goal is None:
                goal = (r, c)
                if goal == start:
                    start = None
                    goal = None
                    path = []
                else:
                    path = astar(start, goal)
            else: 
                start = (r, c)
                goal = None
                path = []

    win.fill(WHITE)
    draw_grid()
    if start:
        pygame.draw.rect(win, BLUE, (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if goal:
        pygame.draw.rect(win, YELLOW, (goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if path:
        draw_path(path)
    pygame.display.flip()

pygame.quit()
