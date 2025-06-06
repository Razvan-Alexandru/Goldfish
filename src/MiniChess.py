import math
import copy
import time
import argparse
from Heuristics import HeuristicsEvaluator
from Player import AI, Human

FILE:    int = 0b01
CONSOLE: int = 0b10
class MiniChess:
    def __init__(self, time_limit, max_turns, use_alpha_beta, play_mode, heuristic):
        self.current_game_state = self.init_board()
        self.output = []
        self.evaluator = HeuristicsEvaluator(self, heuristic)
        self.time_limit = time_limit
        self.max_turns = max_turns
        self.use_alpha_beta = use_alpha_beta
        self.play_mode = play_mode
        play_mode_arr = play_mode.split("-")
        self.player1 = Human() if play_mode_arr[0] == "H" else AI(self.use_alpha_beta,self.time_limit, self.evaluator)
        self.player2 = Human() if play_mode_arr[1] == "H" else AI(self.use_alpha_beta,self.time_limit, self.evaluator)

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
            [['bK', 'bQ', 'bB', 'bN', '.' ],
            [ '.' , '.' , 'bp', 'bp', '.' ],
            [ '.' , '.' , '.' , '.' , '.' ],
            [ '.' , 'wp', 'wp', '.' , '.' ],
            [ '.' , 'wN', 'wB', 'wQ', 'wK']],
            "turn": 'white',
            "turns":   1, # count of turns
            "capture": 0, # turn since last capture
            "outcome": '' # white, black, draw
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
        self.log()
        for i, row in enumerate(game_state["board"], start=1):
            self.log(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        self.log()
        self.log("     A   B   C   D   E")
        self.log()

    """
    Log to console and/or output file

    Args:
        - message: String message to log
        - mode:    Integer with bit fields FILE, CONSOLE
    """
    def log(self, message = '', mode: int = FILE | CONSOLE):
        if (mode & FILE): 
            self.output.append(message)
        if (mode & CONSOLE): 
            print(message)
    """
    Exit the game and write to console
    """
    def safe_exit(self):
        with open('output.txt', 'w') as out:
            out.write('\n'.join(self.output))
        exit(0)

    def on_board(self, x: int, y: int) -> bool:
        return 0 <= x < len(self.current_game_state["board"][0]) and \
               0 <= y < len(self.current_game_state["board"])
    
    def empty(self, x: int, y: int) -> bool:
        return self.current_game_state["board"][y][x] == '.'
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
        move_validations: dict = {
            'p': self.valid_pawn_moves,
            'K': self.valid_king_moves,
            'N': self.valid_knight_moves,
            'B': self.valid_bishop_moves,
            'Q': self.valid_queen_moves
        }

        moves = []
        color = game_state["turn"][0]
        for j, row in enumerate(game_state["board"]):
            for i, cell in enumerate(row):
                # Skip for empty square or incorrect turn
                if cell == '.' or cell[0] != color: 
                    continue
                moves.extend(
                    move_validations.get(cell[1], self.unknown_piece)(game_state, j, i)
                )
            
        return moves

    """
    Quit program if there is an invalid piece
    """
    def unknown_piece(self, *args):
        self.log("A piece on the board is not recognized. Exiting...")
        self.safe_exit()
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
        state = {"black": (1, 'w'), "white": (-1, 'b')}
        direction, opponent = state[game_state["turn"]]
        # Move forward
        if self.on_board(i, j + direction) and self.empty(i, j + direction):
            moves.append(((j, i), (j + direction, i)))
        # Capture
        for diagonal in [-1, 1]:  
            x = i + diagonal
            y = j + direction
            if self.on_board(x, y) and opponent in game_state["board"][y][x]:
                moves.append(((j, i), (y, x)))
                
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
            if self.on_board(x, y) and not game_state["board"][y][x].startswith(game_state["turn"][0]):
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
            if self.on_board(x, y) and not game_state["board"][y][x].startswith(game_state["turn"][0]):
                moves.append(((j, i), (y, x)))
        return moves
    """
    Returns a list of valid moves for the Queens

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_queen_moves(self, game_state, j, i):
        moves = self.valid_bishop_moves(game_state, j, i)
        for (x_dir, y_dir) in [(1, 0), (-1, 0), (0, 1), (0, -1)]: #Vertical and Horizontal
                x, y = i, j
                while self.on_board(x:=x+x_dir, y:=y+y_dir):
                    if self.empty(x, y):
                        moves.append(((j, i), (y, x)))
                    elif not game_state["board"][y][x].startswith(game_state["turn"][0]):
                        moves.append(((j, i), (y, x)))
                        break
                    else:
                        break

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
            while self.on_board(x:=x+x_dir, y:=y+y_dir):
                if self.empty(x, y):
                    moves.append(((j, i), (y, x)))
                elif not game_state["board"][y][x].startswith(game_state["turn"][0]):
                    moves.append(((j, i), (y, x)))
                    break
                else:
                    break
        return moves
    """
    Verify if the game is ending on this move

    Returns:
        - game_over:    bool | Truthy if the game is over, falsy otherwise
    """
    def game_should_end(self):
        if self.current_game_state["turns"] - self.current_game_state["capture"] >= self.max_turns:
            self.current_game_state["outcome"] = 'draw'

        if (self.current_game_state["outcome"]):
            announcement = 'Draw' if self.current_game_state["outcome"] == 'draw' \
                else f'{self.current_game_state["outcome"].capitalize()} won'
            self.log(f'{announcement} in {self.current_game_state["turns"]} turns')
            return True
        
        return False
    """
    Modify to board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):
        start, end = move

        start_row, start_col = start
        end_row, end_col = end

        moving_piece = game_state["board"][start_row][start_col]
        capt_piece = game_state["board"][end_row][end_col]

        # Turns since last capture
        ## Set to next turn because the current turn is not over yet
        if capt_piece != '.':
            game_state["capture"] = game_state["turns"] + 1
            # self.evaluator.update_e0(game_state, capt_piece) # This function will evaluate the current board evaluation during each turn

        # Queening
        if (moving_piece == 'wp' and end_row == 0) or \
        (moving_piece == 'bp' and end_row == len(game_state["board"]) - 1):
            moving_piece = f'{game_state["turn"][0]}Q'

        # King capture
        if capt_piece == 'wK' or capt_piece == 'bK':
            game_state["outcome"] = game_state["turn"]

        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = moving_piece
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
        self.log("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.", CONSOLE)
        latch: bool = True

        while True:
            self.display_board(self.current_game_state)

            # Game over ---\
            if (self.game_should_end()):
                self.safe_exit()
            # Players make moves ---\
            self.log(f'Turn #{self.current_game_state["turns"]}')
            isCurrentPlayerAI = False
            if self.current_game_state["turn"] == "white":
                move = self.player1.make_move(self)
                isCurrentPlayerAI = isinstance(self.player1, AI)
            else:
                move = self.player2.make_move(self)
                isCurrentPlayerAI = isinstance(self.player2, AI)

            if move != None and move.lower() == 'exit':
                self.log("Game exited.")
                self.safe_exit()                
           
            self.log(f'{self.current_game_state['turn'].capitalize()} played {move}', FILE)

            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
                if(isCurrentPlayerAI):
                    self.log(f'AI made invalid move ({move}). {self.current_game_state["turn"]} lost.')
                    self.safe_exit()
                else:
                    self.log("Invalid move. Try again.")
                    continue

            self.make_move(self.current_game_state, move)
            self.current_game_state["turns"] += (latch := not latch)

"""
Validates that the input value is a postive integer

Args:
    - Value
Returns:
    - Value
"""
def validate_positiveInt(value):
    try:
        intValue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid input: {value} is not an integer.")
    if intValue <= 0:
        raise argparse.ArgumentTypeError(f"{value} must be a postive integer.")
    return intValue
    


if __name__ == "__main__":
    # Parsing Args
    parser = argparse.ArgumentParser(description="MiniChess AI Game")
    parser.add_argument("time_limit", type=validate_positiveInt, help="Maximum allowed time per move (seconds)")
    parser.add_argument("max_turns", type=validate_positiveInt, help="Maximum number of turns before game ends")
    parser.add_argument("use_alpha_beta", type=int, choices=[0,1], help="Use Alpha-Beta pruning? (0 = No, 1 = Yes).")
    parser.add_argument("play_mode", type=str, choices=["H-H","H-AI","AI-H","AI-AI"], help="Is Player 1 an AI? (H-H H-AI AI-H AI-AI.)")
    parser.add_argument("heuristic", type=str, choices=["e0", "e1", "e2"], help="Which heuristic to use (e0, e1, e3)")
    args = parser.parse_args()
    
    game = MiniChess( 
        time_limit=args.time_limit,
        max_turns=args.max_turns,
        use_alpha_beta=bool(args.use_alpha_beta),
        play_mode=args.play_mode,
        heuristic=args.heuristic,
        )
    game.play()