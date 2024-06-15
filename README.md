# Sand Simulation
A simple sand simulation program using Python, PyOpenGL, and Pygame. Users can create sand particles that fall under gravity, interact with each other, and collide with obstacles. The program also allows users to draw and remove obstacles on the screen.

## Features
- Sand particles fall under the influence of gravity.
- Users can spawn sand particles by clicking the mouse.
- Users can draw obstacles by holding the '1' key and clicking the mouse.
- Users can remove obstacles by holding the '2' key and clicking the mouse.
- Sand particles interact with obstacles and stop when they collide with them.

## Requirements
- Python 3.x
- Pygame
- PyOpenGL
- NumPy

## Installation

 Clone the repository:
```bash
git clone https://github.com/dagweg/sandsim.git
cd sandsim
```
Create a virtual environment
```bash
py -m venv venv
```
Activate the environment
```bash
# In Windows
.\venv\Scripts\activate
# In Unix
source venv/scripts/activate # or
source venv/bin/activate
```
Install the required packages:
```bash
pip install pygame PyOpenGL numpy
```

## Usage
Run the main script to start the simulation:

```bash
# In Windows
py sand_simulation.py
# In Unix
python app.py # or
python3 app.py
```

## Controls
Left Mouse Button: Spawn sand particles where the mouse is clicked.
Hold '1' Key and Left Mouse Button: Draw obstacles on the screen.
Hold '2' Key and Left Mouse Button: Remove obstacles from the screen.

## Code Overview
- Initialization
`initialize_pygame()`: Initializes Pygame and sets up the display window.
`initialize_opengl()`: Sets up the OpenGL context for rendering.
- Grid Management
`grid`: A 2D NumPy array representing the presence of sand particles.
`obstacles`: A 2D NumPy array representing the presence of obstacles.
- Main Functions
`spawn_sand(x, y)`: Spawns a sand particle at the specified position.
`place_obstacle(x, y, remove=False)`: Places or removes an obstacle at the specified position.
`update_sand()`: Updates the position of sand particles based on gravity and collisions.
`draw_sand()`: Renders the sand particles and obstacles on the screen.
- Main Loop
The main() function initializes Pygame and OpenGL, handles user input, updates the simulation, and renders the particles and obstacles. It runs at 60 frames per second.

Example
Here's a screenshot of the sand simulation in action:
![image](https://github.com/dagweg/sandsim/assets/90281138/080a7244-6006-4cd4-8fdf-ccdb814b8163)


### Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

### License
This project is licensed under the MIT License.
