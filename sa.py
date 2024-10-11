import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window size
WIDTH, HEIGHT = 600, 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)

# Difficulty settings
DIFFICULTIES = {
    "Easy": {"start_size": 11, "start_level": 1},
    "Medium": {"start_size": 15, "start_level": 5},
    "Hard": {"start_size": 19, "start_level": 10},
    "Super Hard": {"start_size": 23, "start_level": 15}
}
background = pygame.image.load("images/maze.jpg") 
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# Generate maze (recursive backtracking)
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]  # Maze filled with walls
    start_row, start_col = 1, 1  # Starting point (1,1)

    # Directions (right, left, up, down) for random traversal
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

    def carve_path(r, c):
        maze[r][c] = 0  # Free space
        random.shuffle(directions)  # Random direction choice

        for direction in directions:
            nr, nc = r + direction[0], c + direction[1]
            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and maze[nr][nc] == 1:
                maze[nr - direction[0] // 2][nc - direction[1] // 2] = 0  # Remove a wall between adjacent cells
                carve_path(nr, nc)

    carve_path(start_row, start_col)
    return maze

# Draw maze
def draw_maze(maze, cell_size):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(window, color, (col * cell_size, row * cell_size, cell_size, cell_size))

# Player movement (checking for walls)
def move_player(player_pos, direction, maze):
    new_row = player_pos[0] + direction[0]
    new_col = player_pos[1] + direction[1]

    if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == 0:
        return new_row, new_col
    return player_pos

# Draw level counter
def draw_level(level):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Level: {level}", True, BLUE)
    window.blit(text, (10, 10))

# Difficulty selection screen
def select_difficulty():
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)
    buttons = []
    for i, difficulty in enumerate(DIFFICULTIES.keys()):
        text = font.render(difficulty, True, BLACK)
        rect = text.get_rect(center=(WIDTH // 2, 200 + i * 80))
        buttons.append((rect, difficulty))

    while True:
        window.blit(background, (0, 0))  # Draw background

        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 128))  # White with 50% opacity
        window.blit(overlay, (0, 0))

        # Draw title
        title = title_font.render("Select Difficulty", True, BLUE)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        window.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, difficulty in buttons:
                    if button.collidepoint(event.pos):
                        return difficulty

        for button, difficulty in buttons:
            if button.collidepoint(mouse_pos):
                color = LIGHT_BLUE
            else:
                color = GRAY
            pygame.draw.rect(window, color, button)
            pygame.draw.rect(window, BLUE, button, 2)
            text = font.render(difficulty, True, BLACK)
            window.blit(text, button)

        pygame.display.flip()

# Main game function
def main():
    # Select difficulty
    difficulty = select_difficulty()
    start_size = DIFFICULTIES[difficulty]["start_size"]
    level = DIFFICULTIES[difficulty]["start_level"]

    clock = pygame.time.Clock()

    # Variables needed for level start
    rows, cols = start_size, start_size
    cell_size = WIDTH // cols
    maze = generate_maze(rows, cols)

    # Player starting position
    player_pos = (1, 1)
    goal_pos = (rows - 2, cols - 2)  # Goal in the bottom right corner

    # Introduce movement timer
    move_delay = 150  # 150 ms wait between movements
    last_move_time = pygame.time.get_ticks()  # Timestamp of the last movement

    while True:
        window.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Current time
        current_time = pygame.time.get_ticks()

        # Check if enough time has passed for movement
        if current_time - last_move_time > move_delay:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_pos = move_player(player_pos, (0, -1), maze)
            if keys[pygame.K_RIGHT]:
                player_pos = move_player(player_pos, (0, 1), maze)
            if keys[pygame.K_UP]:
                player_pos = move_player(player_pos, (-1, 0), maze)
            if keys[pygame.K_DOWN]:
                player_pos = move_player(player_pos, (1, 0), maze)

            # Update the last movement time
            last_move_time = current_time

        # Draw maze and player
        draw_maze(maze, cell_size)
        pygame.draw.rect(window, BLUE, (player_pos[1] * cell_size, player_pos[0] * cell_size, cell_size, cell_size))
        pygame.draw.rect(window, RED, (goal_pos[1] * cell_size, goal_pos[0] * cell_size, cell_size, cell_size))  # Display goal

        # Display level counter
        draw_level(level)

        # Check if the player has reached the goal
        if player_pos == goal_pos:
            level += 1  # Increase level
            rows += 2  # Increase maze size
            cols += 2
            cell_size = WIDTH // cols  # New cell size
            maze = generate_maze(rows, cols)  # Generate new, larger maze
            player_pos = (1, 1)  # Player starts over
            goal_pos = (rows - 2, cols - 2)  # New goal

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()