import pygame
import numpy as np

# --- Config ---
CELL_SIZE = 8
GRID_WIDTH = 100
GRID_HEIGHT = 80
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ANT_COLOR = (255, 0, 0)

# Directions: 0 = up, 1 = right, 2 = down, 3 = left
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption("Langton's Ant")
clock = pygame.time.Clock()

# Grid: 0 = white, 1 = black
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

# Ant position and direction
ant_x, ant_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
ant_dir = 0  # facing up

running = True
paused = False

def draw_grid(surface, grid, ant_pos):
    surface.fill(WHITE)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x] == 1:
                pygame.draw.rect(surface, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw ant
    ax, ay = ant_pos
    pygame.draw.rect(surface, ANT_COLOR, (ax * CELL_SIZE, ay * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def step(grid, ant_x, ant_y, ant_dir):
    if grid[ant_y, ant_x] == 0:  # white → turn right
        ant_dir = (ant_dir + 1) % 4
        grid[ant_y, ant_x] = 1
    else:  # black → turn left
        ant_dir = (ant_dir - 1) % 4
        grid[ant_y, ant_x] = 0

    dx, dy = DIRS[ant_dir]
    ant_x = (ant_x + dx) % GRID_WIDTH
    ant_y = (ant_y + dy) % GRID_HEIGHT
    return grid, ant_x, ant_y, ant_dir

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_c:
                grid[:] = 0
                ant_x, ant_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
                ant_dir = 0

    if not paused:
        grid, ant_x, ant_y, ant_dir = step(grid, ant_x, ant_y, ant_dir)

    draw_grid(screen, grid, (ant_x, ant_y))
    clock.tick(FPS)

pygame.quit()
