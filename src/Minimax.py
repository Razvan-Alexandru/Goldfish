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

    def minimax(self, depth, maximizing_player):
        self.start_time = time.time()
        stack = [(self.game.current_game_state, depth, -math.inf, math.inf, maximizing_player)]
        best_move = None
        best_score = -math.inf if maximizing_player else math.inf

        while stack:
            game_state, current_depth, alpha, beta, is_maximizing = stack.pop()

            if time.time() - self.start_time >= self.time_limit:
                break
            
            if current_depth == 0 or self.game.game_should_end():
                score = self.evaluator.score["e0"]
                continue

            valid_moves = self.game.valid_moves(game_state)
            for move in valid_moves:
                new_game_state = copy.deepcopy(game_state)
                self.game.make_move(new_game_state, move)
                captured_piece = game_state["board"][move[1][0]][move[1][1]]
                if captured_piece != '.':
                    self.evaluator.update_e0(new_game_state, captured_piece)
                
                score = self.evaluator.score["e0"]

                if is_maximizing:
                    if score > best_score:
                        best_score = score
                        best_move = move
                    if self.use_alpha_beta:
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
                else:
                    if score < best_score:
                        best_score = score
                        best_move = move
                    if self.use_alpha_beta:
                        beta = min(beta, score)
                        if beta <= alpha:
                            break

                stack.append((new_game_state, current_depth - 1, alpha, beta, not is_maximizing))

        return best_move
