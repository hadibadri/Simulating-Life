import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

ON = 255
OFF = 0
vals = [ON, OFF]

# Representing the grid
def randomGrid(N):
    """
    Returns a grid of NxN random values.
    """
    # x = np.array([[0, 0, 255], [255, 255, 0], [0, 255, 0]])  # 255 for ON, 0 for OFF
    # plt.imshow(x, interpolation='nearest') # imshow() is used to represent the matrix 
    # plt.show()

    # Setting initial conditions
    #np.random.choice([0,255], 4*4, p = [0.1, 0.9]).reshape(4, 4)
    
    return np.random.choice(vals, N*N, p = [0.2, .8]).reshape(N, N)

def addGlider(i, j, grid):
    """
    adds a glider on top left cell at (i, j)
    """
    glider = np.array([[0, 0, 255],
                      [255, 0, 255],
                      [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider
    
def update(frameNum, img, grid, N):
    # Copying the grid since we require 8 neighbours for calculation and we must go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            """
            Compute 8 neighbour sum using toroidal conditionss.
            x and y wrap around so that the simulation takes place on a toroidal surface.
            """
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1), (j+1)] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1), (j+1)])/255)
            
            # Applying conway's rule
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    # Update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img

def main(N=100, updateInterval=50, glider=False, gosper=False):
    """
    Runs the Conway's Game of Life simulation.

    Args:
        N (int, optional): Grid size. Defaults to 100.
        updateInterval (int, optional): Animation update interval in milliseconds. Defaults to 50.
        glider (bool, optional): Start with a glider pattern. Defaults to False.
        gosper (bool, optional): Start with a Gosper glider gun pattern (not implemented yet). Defaults to False.
    """

    # Set grid size
    if N <= 8:
        print("Grid size must be greater than 8. Using default 100.")
        N = 100

    # Declare grid
    grid = np.array([])

    # Check if glider/demo flag is specified
    if glider:
        grid = np.zeros(N * N).reshape(N, N)
        addGlider(1, 1, grid)
    else:
        grid = randomGrid(N)

    # Setup the animations
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N),
                                 frames=10,
                                 interval=updateInterval) 


    plt.show()


if __name__ == "__main__":
    # You can call the main function here with desired arguments
    main(N=200, updateInterval=20, glider=True)