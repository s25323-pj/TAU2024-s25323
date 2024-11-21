import pytest
from board import Board


def test_move_valid():
    board = Board(5, 5)
    board.start = (2, 2)
    board.obstacles = [(1, 2), (3, 2)]
    assert board.move((2, 2), "up") == (2, 2)
    assert board.move((2, 2), "down") == (2, 2)
    assert board.move((2, 2), "right") == (2, 3)


def test_move_out_of_bounds():
    board = Board(5, 5)
    board.start = (0, 0)
    assert board.move((0, 0), "up") == (0, 0)
    assert board.move((0, 0), "left") == (0, 0)


def test_move_to_obstacle():
    board = Board(5, 5)
    board.start = (2, 2)
    board.obstacles = [(2, 3)]
    current_position = (2, 2)

    new_position = board.move(current_position, "right")
    assert new_position == (2, 2)

def test_move_outside_board():
    board = Board(5, 5)
    board.start = (0, 0)
    current_position = (0, 0)

    new_position = board.move(current_position, "left")
    assert new_position == (0, 0)

    new_position = board.move(current_position, "up")
    assert new_position == (0, 0)


def test_generate_obstacles():
    board = Board(10, 10)
    board.generate_start_and_stop()
    board.generate_obstacles(20)

    assert board.start not in board.obstacles
    assert board.stop not in board.obstacles

    for obstacle in board.obstacles:
        x, y = obstacle
        assert 0 <= x < board.height
        assert 0 <= y < board.width


def test_path_tracking():
    board = Board(5, 5)
    board.start = (0, 0)
    current_position = board.start
    board.path = [current_position]

    current_position = board.move(current_position, "right")
    board.path.append(current_position)

    current_position = board.move(current_position, "down")
    board.path.append(current_position)

    assert board.path == [(0, 0), (0, 1), (1, 1)]

