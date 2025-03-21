class HeuristicsEvaluator:
    def __init__(self, chess, heuristic):
        self.chess = chess
        self.heuristic = heuristic
        self.score = 0
        heuristic_map : dict = {
            "e0": self.evaluate_e0,
            "e1": self.evaluate_e1,
            "e2": self.evaluate_e2
        }
        self.evaluate = heuristic_map.get(heuristic, self.evaluate_e0)

    """
    Evaluate the board at the end of each move, this is not efficient
    but I added it in case we will need it in the future.
    """
    def evaluate_e0(self, game_state):
        piece_value = {'p': 1, 'B': 3, 'N': 3, 'Q': 9, 'K': 999}
        score = 0
        for row in game_state["board"]:
            for cell in row:
                if cell != '.':
                    value = piece_value.get(cell[1], 0)
                    score += value if cell[0] == 'w' else -value
        return score

    def update_e0(self, game_state, capt_piece):
        piece_values = {'p': 1, 'B': 3, 'N': 3, 'Q': 9, 'K': 999}

        self.score -= piece_values.get(capt_piece[1], 0) * (1 if capt_piece[0] == 'w' else -1)
        return self.score

    def evaluate_e1(self, game_state):
        white_moves = len(self.chess.valid_moves({**game_state, "turn": "white"}))
        black_moves = len(self.chess.valid_moves({**game_state, "turn": "black"}))
        return white_moves - black_moves  # More mobility is better

    def evaluate_e2(self, game_state):
        return 1 * self.evaluate_e0(game_state) + 0.3 * self.evaluate_e1(game_state)

