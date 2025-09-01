import random
from flask import Flask, request
from uuid import uuid4, UUID

app = Flask(__name__)

games = []


@app.post("/games")
def create_new_game():
    new_id = uuid4()
    new_game = {
        "id": new_id,
        "player_x_moves": [],
        "player_o_moves": [],
    }
    games.append(new_game)

    return f"New game create with id {new_id}"


def is_valid_move(move_str):
    if len(move_str) != 2:
        return False

    first_char, second_char = [*move_str]

    if first_char not in ["A", "B", "C"]:
        return False
    if second_char not in ["1", "2", "3"]:
        return False

    return True


def get_all_moves():
    pairs = []
    for letter in ["A", "B", "C"]:
        for number in ["1", "2", "3"]:
            pairs.append(f"{letter}{number}")
    return pairs


def get_available_moves(game):
    available_moves = get_all_moves()

    for x_move in game["player_x_moves"]:
        available_moves.remove(x_move)
    for o_move in game["player_o_moves"]:
        available_moves.remove(o_move)

    return available_moves


def generate_computer_move(list):
    return random.choice(list)


def is_tie(game):
    available_moves = get_available_moves(game)
    return len(available_moves) == 0


def is_horizontal_win(moves_list):
    numbers = ["1", "2", "3"]

    for number in numbers:
        if len([move for move in moves_list if number in move]) == 3:
            return True

    return False


def is_vertical_win(moves_list):
    letters = ["A", "B", "C"]

    for letter in letters:
        if len([move for move in moves_list if letter in move]) == 3:
            return True

    return False


def is_diagonal_win(moves_list):
    diag_1_moves = ["A1", "B2", "C3"]
    diag_2_moves = ["A3", "B2", "C1"]

    return all(move in moves_list for move in diag_1_moves) or all(
        move in moves_list for move in diag_2_moves
    )


def is_corners_win(moves_list):
    winning_moves = ["A1", "A3", "C1", "C3"]

    return all(move in moves_list for move in winning_moves)


def is_win(moves_list):
    return (
        is_horizontal_win(moves_list)
        or is_vertical_win(moves_list)
        or is_corners_win(moves_list)
        or is_diagonal_win(moves_list)
    )


def is_available(game, move_str):
    available_moves = get_available_moves(game)
    return move_str in available_moves


@app.post("/games/<string:game_id>")
def add_move_to_game(game_id):
    new_move = request.json["move"]
    if not is_valid_move(new_move):
        return "Invalid move! Please enter a valid 2 char string!"

    game = next(game for game in games if UUID(game_id) == game["id"])
    if not is_available(game, new_move):
        return "That space is not available, please enter another move!"

    # Players turn
    game["player_x_moves"].append(new_move)
    if is_win(game["player_x_moves"]):
        return "You win!"
    if is_tie(game):
        return "You have tied!"

    # Computers turn
    available_moves = get_available_moves(game)
    computer_move = generate_computer_move(available_moves)
    game["player_o_moves"].append(computer_move)
    if is_win(game["player_o_moves"]):
        return "You lose!"

    return game


@app.get("/games/<string:game_id>")
def get_game(game_id):
    try:
        game = next(game for game in games if UUID(game_id) == game["id"])
    except StopIteration:
        return "Game not found!"

    return game
