import json
import os

with open("board_config.json", "r") as config_file:
    config = json.load(config_file)

BOARD_SIZE = config.get("board_size", 8)
START_POSITION = tuple(config.get("start_position", [0, 0]))
RESULTS_DIR = "results"

MOVES = [(2, 1), (2, -1), (-2, 1), (-2, -1),
         (1, 2), (1, -2), (-1, 2), (-1, -2)]

class KnightTour:
    def __init__(self, board_size, start_position):
        self.board_size = board_size
        self.board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
        self.path = []
        self.board[start_position[0]][start_position[1]] = 0
        self.path.append(start_position)

    def is_valid_move(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == -1

    def get_degree(self, x, y):
        # Count valid onward moves from a given position
        count = 0
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny):
                count += 1
        return count

    def warnsdorff_next_move(self, x, y):
        # Choose the next move based on Warnsdorff's rule (minimum degree heuristic)
        next_moves = []
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny):
                degree = self.get_degree(nx, ny)
                next_moves.append((degree, nx, ny))

        # Sort moves by degree and select the move with the lowest degree
        if next_moves:
            next_moves.sort()  # Sort by degree, then by position
            _, nx, ny = next_moves[0]
            return nx, ny
        return None

    def run_tour(self):
        x, y = self.path[0]
        move_count = 1

        while len(self.path) < self.board_size * self.board_size:
            next_move = self.warnsdorff_next_move(x, y)
            if next_move is None:
                break  # No further moves available (dead end)
            x, y = next_move
            self.board[x][y] = move_count
            self.path.append((x, y))
            move_count += 1

        return len(self.path) == self.board_size * self.board_size  # True if complete tour

    def save_results(self):
        os.makedirs(RESULTS_DIR, exist_ok=True)
        filename = os.path.join(RESULTS_DIR, "tour_result.txt")
        with open(filename, "w") as file:
            for step, (x, y) in enumerate(self.path):
                file.write(f"Step {step + 1}: ({x}, {y})\n")
            file.write("Tour Completed: " + str(len(self.path) == self.board_size * self.board_size) + "\n")

if __name__ == "__main__":
    tour = KnightTour(BOARD_SIZE, START_POSITION)
    if tour.run_tour():
        print("Knight's Tour completed successfully!")
    else:
        print("Knight's Tour could not complete.")
    tour.save_results()
