import math
import copy
import time
import argparse

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()

    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
    """
    def init_board(self):
        state = {
                "board": 
                [['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']],
                "turn": 'white',
                }
        return state

    """
    Prints the board
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()

    """
    Check if the move is valid    
    
    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move which we check the validity of ((start_row, start_col),(end_row, end_col))
    Returns:
        - boolean representing the validity of the move
    """
    def is_valid_move(self, game_state, move):
        return move in self.valid_moves(game_state)

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_moves(self, game_state):
        # Return a list of all the valid moves.
        # Implement basic move validation
        # Check for out-of-bounds, correct turn, move legality, etc
        moves = []
        colorPrefix = "b" if game_state["turn"] == "black" else "w"
        for j, row in enumerate(game_state["board"]):
            for i, cell in enumerate(row):
                #Pawn
                if cell == f'{colorPrefix}p':
                    moves.extend(self.valid_pawn_moves(game_state,j,i))
                if cell == f'{colorPrefix}K':
                    moves.extend(self.valid_king_moves(game_state,j,i))
                if cell == f'{colorPrefix}N':
                    moves.extend(self.valid_knight_moves(game_state,j,i))
                if cell == f'{colorPrefix}B':
                    moves.extend(self.valid_bishop_moves(game_state,j,i))
        # TODO add all valid moves
        return moves

    """
    Returns a list of valid moves for pawns

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]

    """
    def valid_pawn_moves(self, game_state,j,i):
        #Setting up variables
        moves = []
        direction = -1 
        start_row = 3
        opponent = "b"
        if game_state["turn"] == "black":
            direction = 1
            start_row = 1
            opponent = "w"
        #if j + direction is on the board and is empty then valid move
        if 0 <= j + direction < len(game_state["board"]) and game_state["board"][j + direction][i] == ".":
            moves.append(((j, i), (j + direction, i)))
        #if j is starting row for pawn and position + 2 is empty then valid move  
        if j == start_row and game_state["board"][j + 2 * direction][i] == ".":
            moves.append(((j, i), (j + 2 * direction, i)))
        # Verify left and right diagonal for capturing
        for diagonal in [-1, 1]:  
            x = i + diagonal
            y = j + direction
            # if new x and y are on the board and have an opponent piece on them then valid move
            if 0 <= x < len(game_state["board"][0]) and 0 <= y < len(game_state["board"]) and opponent in game_state["board"][y][x]:
                moves.append(((j, i), (y, x)))

        # #For debugging purposes
        # for move in moves:
        #    print(f"Pawn moves from {move[0]} to {move[1]}")

        return moves
    """
    Returns a list of valid moves for the kings

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_king_moves(self, game_state, j, i):
        moves = []
        for (x_dir, y_dir) in [
            (-1, 1),  (0, 1),  (1, 1), 
            (-1, 0),           (1, 0), 
            (-1, -1), (0, -1), (1, -1)
        ]:
            x = i + x_dir
            y = j + y_dir
            if 0 <= x < len(game_state["board"][0]) and 0 <= y < len(game_state["board"]) \
            and not game_state["board"][y][x].startswith(game_state["turn"][0]):
                moves.append(((j, i), (y, x)))
        return moves
    """
    Returns a list of valid moves for the knights

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_knight_moves(self, game_state, j, i):
        moves = []
        for (x_dir, y_dir) in [# Horse moves
            (2, -1), (2, 1),   # --|
            (1, 2),  (-1, 2),  # ¯|¯
            (-2, 1), (-2, -1), # |--
            (-1, -2), (1, -2)  # _|_
        ]:
            x = i + x_dir
            y = j + y_dir
            if 0 <= x < len(game_state["board"][0]) and 0 <= y < len(game_state["board"]) \
            and not game_state["board"][y][x].startswith(game_state["turn"][0]):
                moves.append(((j, i), (y, x)))
        return moves
    """
    Returns a list of valid moves for the bishops

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_bishop_moves(self, game_state, j, i):
        moves = []
        for (x_dir, y_dir) in [(1, 1), (-1, -1), (1, -1), (-1, 1)]: # Diagonals / and \ 
            x, y = i, j
            while 0 <= (x:=x+x_dir) < len(game_state["board"][0]) and 0 <= (y:=y+y_dir) < len(game_state["board"]):
                if game_state["board"][y][x] == '.':
                    moves.append(((j, i), (y, x)))
                elif not game_state["board"][y][x].startswith(game_state["turn"][0]):
                    moves.append(((j, i), (y, x)))
                    break
                else:
                    break
        return moves
    """
    Modify to board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):
        start = move[0]
        end = move[1]
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return game_state

    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end)  tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    """
    Game loop

    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        while True:
            self.display_board(self.current_game_state)
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)

            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
                print("Invalid move. Try again.")
                continue

            self.make_move(self.current_game_state, move)

if __name__ == "__main__":
    game = MiniChess()
    game.play()