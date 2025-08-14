import pygame
import numpy as np

# --- Config ---
Celula_SIZE = 10
Grilla_WIDTH = 80
Grilla_HEIGHT = 60
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((Grilla_WIDTH * Celula_SIZE, Grilla_HEIGHT * Celula_SIZE))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Grilla: 0 = dead, 1 = alive
Grilla = np.zeros((Grilla_HEIGHT, Grilla_WIDTH), dtype=int)

running = True
paused = True

def draw_Grilla(surface, Grilla):
    surface.fill(BLACK)
    for y in range(Grilla_HEIGHT):
        for x in range(Grilla_WIDTH):
            if Grilla[y, x] == 1:
                rect = pygame.Rect(x * Celula_SIZE, y * Celula_SIZE, Celula_SIZE, Celula_SIZE)
                pygame.draw.rect(surface, WHITE, rect)
    pygame.display.flip()

def update_Grilla(Grilla):
    GrillaNueva = np.copy(Grilla)
    for y in range(Grilla_HEIGHT):
        for x in range(Grilla_WIDTH):
            # Count alive neighbors
            neighbors = np.sum(Grilla[max(0, y-1):min(Grilla_HEIGHT, y+2),
                                    max(0, x-1):min(Grilla_WIDTH, x+2)]) - Grilla[y, x]
            # Rules
            if Grilla[y, x] == 1 and (neighbors < 2 or neighbors > 3):
                GrillaNueva[y, x] = 0
            elif Grilla[y, x] == 0 and neighbors == 3:
                GrillaNueva[y, x] = 1
    return GrillaNueva

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_c:
                Grilla[:] = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // Celula_SIZE, my // Celula_SIZE
            Grilla[gy, gx] = 1 - Grilla[gy, gx]  # Toggle Celula

    if not paused:
        Grilla = update_Grilla(Grilla)

    draw_Grilla(screen, Grilla)
    clock.tick(FPS)

pygame.quit()