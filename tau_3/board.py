import random
import os


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[" " for _ in range(width)] for _ in range(height)]
        self.start = None
        self.stop = None
        self.obstacles = []
        self.path = []

    def generate_start_and_stop(self):
        edges = (
            [(0, i) for i in range(self.width)] +
            [(self.height - 1, i) for i in range(self.width)] +
            [(i, 0) for i in range(self.height)] +
            [(i, self.width - 1) for i in range(self.height)]
        )
        self.start, self.stop = random.sample(edges, 2)

        self.board[self.start[0]][self.start[1]] = "A"
        self.board[self.stop[0]][self.stop[1]] = "B"

    def generate_obstacles(self, num_obstacles):
        for _ in range(num_obstacles):
            while True:
                x = random.randint(0, self.height - 1)
                y = random.randint(0, self.width - 1)
                if (x, y) != self.start and (x, y) != self.stop and (x, y) not in self.obstacles:
                    self.obstacles.append((x, y))
                    self.board[x][y] = "X"
                    break

    def move(self, current_position, direction):
        x, y = current_position
        if direction == "up":
            new_position = (x - 1, y)
        elif direction == "down":
            new_position = (x + 1, y)
        elif direction == "left":
            new_position = (x, y - 1)
        elif direction == "right":
            new_position = (x, y + 1)
        else:
            raise ValueError("Invalid direction")


        if (
            0 <= new_position[0] < self.height and
            0 <= new_position[1] < self.width and
            new_position not in self.obstacles
        ):
            return new_position
        else:
            return current_position

    def display_board(self):
        for row in self.board:
            print(" ".join(row))

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            for row in self.board:
                f.write(" ".join(row) + "\n")
            f.write(f"\nPath: {self.path}\n")


if __name__ == "__main__":
    width, height = 10, 10
    num_obstacles = 15

    board = Board(width, height)
    board.generate_start_and_stop()
    board.generate_obstacles(num_obstacles)
    board.display_board()


    current_position = board.start
    moves = ["right", "down", "down", "right"]
    for move in moves:
        current_position = board.move(current_position, move)
        board.path.append(current_position)

    board.save_to_file("board.txt")
    print("\nPath:", board.path)
