import numpy as np
import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran labirin (lebar x tinggi)
width = 41  # Lebar labirin
height = 41  # Tinggi labirin
cell_size = 15  # Ukuran setiap sel dalam piksel

# Fungsi untuk membuat labirin menggunakan algoritma Recursive Backtracking
def create_maze(width, height):
    maze = np.ones((height, width))
    visited = np.zeros((height, width))
    stack = []

    def is_valid(x, y):
        return 0 < x < height - 1 and 0 < y < width - 1 and not visited[x][y]

    start = (1, 1)
    stack.append(start)
    visited[start] = 1

    while stack:
        x, y = stack[-1]
        neighbors = []

        if is_valid(x - 2, y):
            neighbors.append((x - 2, y))
        if is_valid(x + 2, y):
            neighbors.append((x + 2, y))
        if is_valid(x, y - 2):
            neighbors.append((x, y - 2))
        if is_valid(x, y + 2):
            neighbors.append((x, y + 2))

        if neighbors:
            next_cell = random.choice(neighbors)
            nx, ny = next_cell
            maze[x + (nx - x) // 2][y + (ny - y) // 2] = 0
            maze[nx][ny] = 0
            visited[nx][ny] = 1
            stack.append(next_cell)
        else:
            stack.pop()

    goal = (height - 2, width - 2)
    maze[goal] = 0
    
    return maze, start, goal

# Fungsi untuk menampilkan labirin dan karakter
def display_maze(maze, player_pos):
    for x in range(maze.shape[0]):
        for y in range(maze.shape[1]):
            if maze[x][y] == 1:
                pygame.draw.rect(screen, (255, 255, 255), (y * cell_size, x * cell_size, cell_size, cell_size))  # Dinding
            else:
                pygame.draw.rect(screen, (0, 0, 0), (y * cell_size, x * cell_size, cell_size, cell_size))  # Jalur

    # Menampilkan posisi karakter (warna biru)
    pygame.draw.rect(screen, (0, 0, 255), (player_pos[1] * cell_size, player_pos[0] * cell_size, cell_size, cell_size))

    # Menampilkan titik start (warna hijau)
    pygame.draw.rect(screen, (0, 255, 0), (1 * cell_size, 1 * cell_size, cell_size, cell_size))
    font = pygame.font.Font(None, 36)
    start_label = font.render('Start', True, (0, 0, 0))
    screen.blit(start_label, (1 * cell_size + 5, 1 * cell_size + 5))

    # Menampilkan titik goal (warna merah)
    pygame.draw.rect(screen, (255, 0, 0), ((height - 2) * cell_size, (width - 2) * cell_size, cell_size, cell_size))
    goal_label = font.render('Goal', True, (0, 0, 0))
    screen.blit(goal_label, ((height - 2) * cell_size + 5, (width - 2) * cell_size + 5))

# Ukuran layar
screen = pygame.display.set_mode((width * cell_size, height * cell_size))
pygame.display.set_caption("Labirin")

# Membuat labirin
maze, start, goal = create_maze(width, height)
player_pos = start

# Loop utama
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    # Kontrol pergerakan
    if keys[pygame.K_w]:  # Up
        new_pos = (player_pos[0] - 1, player_pos[1])
        if maze[new_pos] == 0:  # Memastikan jalur valid
            player_pos = new_pos
    if keys[pygame.K_s]:  # Down
        new_pos = (player_pos[0] + 1, player_pos[1])
        if maze[new_pos] == 0:  # Memastikan jalur valid
            player_pos = new_pos
    if keys[pygame.K_a]:  # Left
        new_pos = (player_pos[0], player_pos[1] - 1)
        if maze[new_pos] == 0:  # Memastikan jalur valid
            player_pos = new_pos
    if keys[pygame.K_d]:  # Right
        new_pos = (player_pos[0], player_pos[1] + 1)
        if maze[new_pos] == 0:  # Memastikan jalur valid
            player_pos = new_pos

    # Cek apakah pemain mencapai goal
    if player_pos == goal:
        print("Selamat! Kamu telah mencapai tujuan!")
        running = False
    
    # Menampilkan labirin
    screen.fill((0, 0, 0))  # Menghapus layar
    display_maze(maze, player_pos)
    pygame.display.flip()  # Mengupdate tampilan

# Keluar dari Pygame
pygame.quit()


