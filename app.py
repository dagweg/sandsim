import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Initialize constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SAND_SIZE = 5
GRAVITY = 1

# Initialize the simulation grid
grid_width = SCREEN_WIDTH // SAND_SIZE
grid_height = SCREEN_HEIGHT // SAND_SIZE
grid = np.zeros((grid_height, grid_width), dtype=bool)  # Grid for sand particles
obstacles = np.zeros((grid_height, grid_width), dtype=bool)  # Grid for obstacles
obstacleSize = 1

def initialize_pygame():
    """
    Initializes Pygame and sets up the display window.
    Returns the screen object.
    """
    pygame.init()  # Initialize all Pygame modules
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    # Create an OpenGL display window with double buffering
    pygame.display.set_caption("Sand Simulation")  # Set the window title
    return screen  # Return the Pygame screen object

def initialize_opengl():
    """
    Sets up the OpenGL context for rendering.
    """
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Set the viewport size
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix
    glLoadIdentity()  # Reset the projection matrix
    gluOrtho2D(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0)  # Set up an orthographic projection (flipped y-axis)
    glMatrixMode(GL_MODELVIEW)  # Switch back to modelview matrix
    glLoadIdentity()  # Reset the modelview matrix
    glClearColor(0, 0, 0, 1.0)  # Set the clear color to black

def spawn_sand(x, y):
    """
    Spawns a sand particle at the given (x, y) position.
    """
    grid_x = x // SAND_SIZE  # Convert x position to grid column
    grid_y = y // SAND_SIZE  # Convert y position to grid row
    if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:  # Check if the position is within grid bounds
        if not obstacles[grid_y, grid_x]:  # Only place sand if there is no obstacle
            grid[grid_y, grid_x] = True  # Set the grid cell to True (sand particle exists)

# directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1),(0,0)]
#         for dx,dy in directions:
#             obstacles[grid_y+dy, grid_x+dx] = not remove

def place_obstacle(x, y, remove=False):
    """
    Places or removes an obstacle at the given (x, y) position.
    """
    grid_x = x // SAND_SIZE  # Convert x position to grid column
    grid_y = y // SAND_SIZE  # Convert y position to grid row
    if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:  # Check if the position is within grid bounds
        # obstacles[grid_y, grid_x] = not remove  # Place or remove the obstacle
        for i in range(-obstacleSize, obstacleSize + 1):
            for j in range(-obstacleSize, obstacleSize + 1):
                if 0 <= grid_x + i < grid_width and 0 <= grid_y + j < grid_height:
                    obstacles[grid_y + j, grid_x + i] = not remove

def update_sand():
    """
    Updates the position of each sand particle according to gravity and collision rules.
    """
    global grid
    new_grid = np.copy(grid)  # Create a copy of the current grid to apply updates
    for y in range(grid_height - 2, -1, -1):  # Iterate from the second-last row to the top
        for x in range(grid_width):  # Iterate over each column
            if grid[y, x]:
                if not grid[y + 1, x] and not obstacles[y + 1, x]:  # Move down if empty and no obstacle
                    new_grid[y, x] = False
                    new_grid[y + 1, x] = True
                elif x > 0 and not grid[y + 1, x - 1] and not obstacles[y + 1, x - 1]:  # Move down-left
                    new_grid[y, x] = False
                    new_grid[y + 1, x - 1] = True
                elif x < grid_width - 1 and not grid[y + 1, x + 1] and not obstacles[y + 1, x + 1]:  # Move down-right
                    new_grid[y, x] = False
                    new_grid[y + 1, x + 1] = True
    grid = new_grid  # Update the grid with the new positions

def draw_sand():
    """
    Renders the sand particles on the screen.
    """
    glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen with the clear color
    glColor3f(0.76,0.70,0.50)  # Sand color
    glBegin(GL_QUADS)  # Start drawing quads (rectangles)
    for y in range(grid_height):  # Iterate over each row
        for x in range(grid_width):  # Iterate over each column
            if grid[y, x]:  # If there is a sand particle at (x, y)
                screen_x = x * SAND_SIZE  # Calculate the screen x position
                screen_y = y * SAND_SIZE  # Calculate the screen y position
                glVertex2f(screen_x, screen_y)  # Bottom-left corner of the quad
                glVertex2f(screen_x + SAND_SIZE, screen_y)  # Bottom-right corner of the quad
                glVertex2f(screen_x + SAND_SIZE, screen_y + SAND_SIZE)  # Top-right corner of the quad
                glVertex2f(screen_x, screen_y + SAND_SIZE)  # Top-left corner of the quad
    glEnd()  # End drawing quads

    glColor3f(0.6,0.2,0.2)  # Brick color
    glBegin(GL_QUADS)  # Start drawing quads (rectangles)
    for y in range(grid_height):  # Iterate over each row
        for x in range(grid_width):  # Iterate over each column
            if obstacles[y, x]:  # If there is an obstacle at (x, y)
                screen_x = x * SAND_SIZE  # Calculate the screen x position
                screen_y = y * SAND_SIZE  # Calculate the screen y position
                glVertex2f(screen_x, screen_y)  # Bottom-left corner of the quad
                glVertex2f(screen_x + SAND_SIZE, screen_y)  # Bottom-right corner of the quad
                glVertex2f(screen_x + SAND_SIZE, screen_y + SAND_SIZE)  # Top-right corner of the quad
                glVertex2f(screen_x, screen_y + SAND_SIZE)  # Top-left corner of the quad
    glEnd()  # End drawing quads

    pygame.display.flip()  # Swap the front and back buffers to display the rendered image

def main():
    """
    Main function to run the sand simulation.
    """
    screen = initialize_pygame()  # Initialize Pygame and create the display window
    initialize_opengl()  # Set up the OpenGL context
    clock = pygame.time.Clock()  # Create a clock object to manage the frame rate
    running = True  # Variable to control the main loop

    mouse_held = False  # Variable to track if the mouse button is held down
    place_obstacle_mode = False  # Variable to track if we are placing or removing obstacles
    remove_obstacle_mode = False  # Variable to track if we are removing obstacles
    shift_held = False  # Variable to track if the Shift key is held down

    while running:  # Main loop
        for event in pygame.event.get():  # Process each event in the event queue
            if event.type == pygame.QUIT:  # If the user closes the window
                running = False  # Exit the main loop
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse button is pressed
                mouse_held = True  # Set mouse_held to True
            elif event.type == pygame.MOUSEBUTTONUP:  # If the mouse button is released
                mouse_held = False  # Set mouse_held to False
            elif event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_1:  # If the '1' key is pressed
                    place_obstacle_mode = True  # Enable placing obstacles
                elif event.key == pygame.K_2:  # If the '2' key is pressed
                    remove_obstacle_mode = True  # Enable removing obstacles
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # If Shift key is pressed
                    shift_held = True  # Enable shift mode
            elif event.type == pygame.KEYUP:  # If a key is released
                if event.key == pygame.K_1:  # If the '1' key is released
                    place_obstacle_mode = False  # Disable placing obstacles
                elif event.key == pygame.K_2:  # If the '2' key is released
                    remove_obstacle_mode = False  # Disable removing obstacles
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # If Shift key is released
                    shift_held = False  # Disable shift mode

        if mouse_held:  # If the mouse button is held down
            x, y = pygame.mouse.get_pos()  # Get the current mouse position
            if place_obstacle_mode:  # If placing obstacles mode is enabled
                place_obstacle(x, y)  # Place an obstacle at the mouse position
            elif remove_obstacle_mode:  # If removing obstacles mode is enabled
                place_obstacle(x, y, remove=True)  # Remove an obstacle at the mouse position
            else:
                spawn_sand(x, y)  # Spawn a sand particle at the mouse position
                if shift_held:  # If Shift key is held down
                    for _ in range(10):  # Emit lots of sand
                        spawn_sand(x + np.random.randint(-5, 5) * SAND_SIZE, y + np.random.randint(-5, 5) * SAND_SIZE)

        update_sand()  # Update the positions of the sand particles
        draw_sand()  # Render the sand particles and obstacles
        clock.tick(60)  # Cap the frame rate at 60 frames per second

    pygame.quit()  # Quit Pygame and clean up

if __name__ == "__main__":
    main()  # Run the main function if this script is executed

