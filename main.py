import pygame
import random
import os

# Define colors
GREEN = (9, 150, 100)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0) #lime green
WHITE = (255, 255, 255)

# Define constants
WIDTH = 1920
HEIGHT = 1080
CELL_SIZE = 10
FOREST_SIZE = (WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)
TREE_DENSITY = 0.6

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Forest Fire Simulation")

# Load images
tree_img = pygame.image.load(os.path.join('assets', 'tree.png')).convert_alpha()
tree_fire_img = pygame.image.load(os.path.join('assets', 'tree_fire.png')).convert_alpha()

# Create forest
def create_forest():
    forest = [[None for y in range(FOREST_SIZE[1])] for x in range(FOREST_SIZE[0])]
    for x in range(FOREST_SIZE[0]):
        for y in range(FOREST_SIZE[1]):
            if random.random() < TREE_DENSITY:
                forest[x][y] = tree_img
    return forest

forest = create_forest()

# Define function to simulate fire spread
def spread_fire(x, y):
    if x < 0 or x >= FOREST_SIZE[0] or y < 0 or y >= FOREST_SIZE[1]:
        return
    if forest[x][y] == tree_img and random.random() < FIRE_SPREAD_PROBABILITY:
        forest[x][y] = tree_fire_img
        spread_fire(x - 1, y)
        spread_fire(x + 1, y)
        spread_fire(x, y - 1)
        spread_fire(x, y + 1)

# Ask user for input
fuel_moisture = float(input("Enter fuel moisture: "))
wind_speed = float(input("Enter wind speed: "))
slope_factor = float(input("Enter slope factor: "))
k = 0.2  # set a constant value for k

# Calculate fire spread probability
FIRE_SPREAD_PROBABILITY = k * (1 - fuel_moisture) * wind_speed * slope_factor

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Simulate fire spread from clicked cell
            x, y = pygame.mouse.get_pos()
            x //= CELL_SIZE
            y //= CELL_SIZE
            if forest[x][y] == tree_img:
                forest[x][y] = tree_fire_img
                spread_fire(x, y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                forest = create_forest()
                FIRE_SPREAD_PROBABILITY = k * (1 - fuel_moisture) * wind_speed * slope_factor

    # Draw forest
    def draw_forest():
        for x in range(FOREST_SIZE[0]):
            for y in range(FOREST_SIZE[1]):
                if forest[x][y] == tree_img:
                    img = tree_img
                elif forest[x][y] == tree_fire_img:
                    img = tree_fire_img
                    spread_fire(x - 1, y)
                    spread_fire(x + 1, y)
                    spread_fire(x, y - 1)
                    spread_fire(x, y + 1)
                else:
                    continue
                screen.blit(img, (x * CELL_SIZE, y * CELL_SIZE))

    # Main game loop
    reset = False
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Simulate fire spread from clicked cell
                x, y = pygame.mouse.get_pos()
                x //= CELL_SIZE
                y //= CELL_SIZE
                if forest[x][y] == tree_img:
                    forest[x][y] = tree_fire_img
                    spread_fire(x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    # Reset the simulation and generate a new forest
                    forest = [[None for y in range(FOREST_SIZE[1])] for x in range(FOREST_SIZE[0])]
                    for x in range(FOREST_SIZE[0]):
                        for y in range(FOREST_SIZE[1]):
                            if random.random() < TREE_DENSITY:
                                forest[x][y] = tree_img
                    reset = True

        # Reset the simulation if Q is pressed
        if reset:
            reset = False
            continue

        # Draw forest   
        screen.fill(BLACK)
        draw_forest()

        # Update display
        pygame.display.flip()

        # Limit frame rate
        clock.tick(30)

    # Clean up
    pygame.quit()
