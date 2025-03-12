class HeuristicsEvaluator:
    def __init__(self, game_state):
        self.score = {"e0": 0} # Could have used the evaluate_e0 function, but at the start if the game this value is always 0.

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
                    value = piece_values.get(cell[1], 0)
                    score += value if cell[0] == 'w' else -value
        return score

    def update_e0(self, game_state, capt_piece):
        piece_values = {'p': 1, 'B': 3, 'N': 3, 'Q': 9, 'K': 999}

        self.score -= piece_values.get(capt_piece[1], 0) * (1 if capt_piece[0] == 'w' else -1)
        return self.score
