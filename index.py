
import numpy as np
import pygame
import random
import heapq
import time

# Inisialisasi Pygame
pygame.init()

# Ukuran labirin (lebar x tinggi)
width = 41
height = 41
cell_size = 15

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

# A* Algorithm
def a_star(maze, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))  # (f_score, position)
    came_from = {}
    
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    expanded_nodes = []  # To keep track of expanded nodes

    while open_set:
        current = heapq.heappop(open_set)[1]
        expanded_nodes.append(current)  # Add to expanded nodes

        if current == goal:
            return reconstruct_path(came_from, current), expanded_nodes

        for neighbor in get_neighbors(current, maze):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return [], expanded_nodes

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, maze):
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for d in directions:
        neighbor = (pos[0] + d[0], pos[1] + d[1])
        if maze[neighbor] == 0:  # valid path
            neighbors.append(neighbor)
    return neighbors

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]  # reverse path

# Fungsi untuk menampilkan labirin dan karakter
def display_maze(maze, player_pos, expanded_nodes=[]):
    # Menampilkan labirin
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

    # Menampilkan titik goal (warna merah)
    pygame.draw.rect(screen, (255, 0, 0), ((height - 2) * cell_size, (width - 2) * cell_size, cell_size, cell_size))

    # Menampilkan node yang telah diekspansi (warna ungu)
    for node in expanded_nodes:
        pygame.draw.rect(screen, (128, 0, 128), (node[1] * cell_size, node[0] * cell_size, cell_size, cell_size))

# Ukuran layar
screen = pygame.display.set_mode((width * cell_size, height * cell_size))
pygame.display.set_caption("Labirin dengan A*")

# Membuat labirin
maze, start, goal = create_maze(width, height)

# Menjalankan A* untuk menemukan jalur
start_time = time.time()  # Mulai timer
path, expanded_nodes = a_star(maze, start, goal)
end_time = time.time()  # Akhiri timer
elapsed_time = end_time - start_time  # Hitung waktu yang dibutuhkan

# Menampilkan waktu yang dibutuhkan
print(f"Waktu yang dibutuhkan untuk menemukan jalur: {elapsed_time:.2f} detik")

# Loop utama
running = True
step_index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    
    # Jika ada node yang perlu diekspansi
    if step_index < len(expanded_nodes):
        display_maze(maze, start, expanded_nodes[:step_index + 1])
        step_index += 1
    else:
        # Setelah semua node diekspansi, tampilkan labirin tanpa jalur
        display_maze(maze, start)
    
    pygame.display.flip()
    time.sleep(0.1)  # Mengatur kecepatan animasi

# Keluar dari Pygame
pygame.quit()
