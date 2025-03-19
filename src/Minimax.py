import math
import time
import copy
from Heuristics import HeuristicsEvaluator

class Minimax:
    def __init__(self, game, evaluator, use_alpha_beta=True, time_limit=5):
        self.game = game
        self.evaluator = evaluator
        self.use_alpha_beta = use_alpha_beta
        self.time_limit = time_limit

    """
    Converts the move coordinates into letter number form (Ex: B3, B4)

    Args:
        - Start, end
    Returns:
        - Letter Number format
    """
    def convert_to_notation(self, start, end):
        start_col = chr(start[1] + ord('A'))
        start_row = 5 - start[0] 
        start_notation = f"{start_col}{start_row}"

        end_col = chr(end[1] + ord('A'))
        end_row = 5 - end[0]
        end_notation = f"{end_col}{end_row}"

        return start_notation+" "+end_notation

    def minimax(self, depth, maximizing_player):
        self.start_time = time.time()
        stack = [(self.game.current_game_state, depth, -math.inf, math.inf, maximizing_player, None)]
        best_move = None
        best_score = -math.inf if maximizing_player else math.inf

        while stack:
            game_state, current_depth, alpha, beta, is_maximizing, parent_move = stack.pop()

            # Time limit
            if time.time() - self.start_time >= self.time_limit:
                break
            
            # Base case
            if current_depth == 0 or self.game.game_should_end():
                score = self.evaluator.evaluate_e0(game_state)

                if parent_move is not None and current_depth == depth:
                    if maximizing_player and score > best_score:
                        best_score = score
                        best_move = parent_move
                    elif not maximizing_player and score < best_score:
                        best_score = score
                        best_move = parent_move
                continue

            valid_moves = self.game.valid_moves(game_state)
            if not valid_moves:
                continue

            for move in valid_moves:
                
                new_game_state = copy.deepcopy(game_state)
                self.game.make_move(new_game_state, move)

                next_player_maximizing = not is_maximizing
                score = self.evaluator.evaluate_e0(new_game_state)

                if current_depth == depth:
                    if maximizing_player:
                        if score > best_score:
                            best_score = score
                            best_move = move
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = move

                # Alpha beta pruning check
                if self.use_alpha_beta:
                    if maximizing_player:
                        alpha = max(alpha, score)
                    else:
                        beta = min(beta, score)
                    if beta <= alpha: # Check if should prune
                        break 

                stack.append((new_game_state, current_depth - 1, alpha, beta, next_player_maximizing, move))

        best_move = self.convert_to_notation(best_move[0], best_move[1])
        print(f'{self.game.current_game_state['turn'].capitalize()} to move: {best_move} ')
        return best_move