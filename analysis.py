import matplotlib.pyplot as plt
import numpy as np
import os

RESULTS_FILE = os.path.join("results", "tour_result.txt")

def load_knight_path(results_file):
    """Load the knight's path from the results file."""
    path = []
    completed = False

    with open(results_file, "r") as file:
        for line in file:
            if line.startswith("Step"):
                _, step_info = line.split(": ")
                x, y = map(int, step_info.strip("()\n").split(", "))
                path.append((x, y))
            elif line.startswith("Tour Completed"):
                completed = "True" in line
    return path, completed

def plot_knight_path(path, board_size, completed):
    """Plot the knight's path on a chessboard."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xticks(np.arange(board_size))
    ax.set_yticks(np.arange(board_size))
    ax.invert_yaxis()
    ax.set_aspect("equal")

    board_pattern = np.zeros((board_size, board_size))
    for i in range(board_size):
        for j in range(board_size):
            if (i + j) % 2 == 0:
                board_pattern[i, j] = 1

    ax.imshow(board_pattern, cmap="gray", interpolation="nearest", extent=[0, board_size, 0, board_size])

    x_coords, y_coords = zip(*path)
    ax.plot(y_coords, x_coords, marker="o", color="blue", markersize=10, linewidth=2, label="Knight's Path")

    for step, (x, y) in enumerate(path):
        ax.text(y, x, str(step + 1), ha="center", va="center", color="red", fontsize=8)

    tour_status = "Completed" if completed else "Incomplete"
    ax.set_title(f"Knight's Tour Path - {tour_status}", fontsize=16)
    ax.legend()

    plt.show()

if __name__ == "__main__":
    if not os.path.exists(RESULTS_FILE):
        print("Results file not found. Run the knight simulation first.")
    else:
        path, completed = load_knight_path(RESULTS_FILE)
        board_size = max(max(x, y) for x, y in path) + 1
        plot_knight_path(path, board_size, completed)