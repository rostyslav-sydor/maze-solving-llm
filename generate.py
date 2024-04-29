import numpy as np
import matplotlib.pyplot as plt
from os import mkdir, path

from maze_dataset.generation import LatticeMazeGenerators
from maze_dataset.maze import TargetedLatticeMaze, SolvedMaze
from maze_dataset.plotting import MazePlot
from maze_dataset.tokenization import MazeTokenizer, TokenizationMode

maze_struct = "plain4x4test"
base_dir = f"dataset/{maze_struct}"

if not path.exists(base_dir):
    mkdir(f"{base_dir}")
    mkdir(f"{base_dir}/images")
    mkdir(f"{base_dir}/solutions")
    mkdir(f"{base_dir}/tokens")

for n in range(100):
    N = 4
    M = 4
    maze = LatticeMazeGenerators.gen_dfs(np.array([N,M]))
    tgt_maze = TargetedLatticeMaze.from_lattice_maze(maze, (0,0), (N-1,M-1))
    solved_maze = SolvedMaze.from_targeted_lattice_maze(tgt_maze)
    tokens = solved_maze.as_tokens(maze_tokenizer=MazeTokenizer(
                                            tokenization_mode=TokenizationMode.AOTP_UT_rasterized, max_grid_size=100,
                                            ))
    
    idx = int([idx + 1 for idx, val in
            enumerate(tokens) if val == "<PATH_START>"][0])

    if (not path.isdir(f"{base_dir}/maze{n+1}")):
        mkdir(f"{base_dir}/maze{n+1}")
    
    # save image
    MazePlot(maze).plot()
    # plt.savefig(f"{base_dir}/maze{n+1}/maze.png", dpi=300)
    plt.savefig(f"{base_dir}/maze{n+1}/maze.png")
    plt.savefig(f"{base_dir}/images/maze{n+1}.png")

    # save tokens
    with open(f"{base_dir}/maze{n+1}/maze.txt", "w+") as file:
        file.write(" ".join(tokens[:idx-1]))
    
    with open(f"{base_dir}/tokens/maze{n+1}.txt", "w+") as file:
        file.write(" ".join(tokens[:idx-1]))

    # save solution
    with open(f"{base_dir}/maze{n+1}/solution.txt", "w+") as file:
        file.write(" ".join(tokens[idx-1:]))
    
    with open(f"{base_dir}/solutions/maze{n+1}.txt", "w+") as file:
        file.write(" ".join(tokens[idx-1:]))
