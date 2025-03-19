from Minimax import Minimax


class Player:
    def make_move(self,game):
        raise NotImplementedError("Subclasses must implement make_move method")
    
class Human(Player):
    def make_move(self,game):
        move = input(f'{game.current_game_state['turn'].capitalize()} to move: ')
        return move
    
class AI(Player):
    def __init__(self, use_alpha_beta, time_limit, evaluator):
        self.use_alpha_beta = use_alpha_beta
        self.time_limit = time_limit
        self.evaluator = evaluator
    def make_move(self,game):
        minimax = Minimax(game, self.evaluator, self.use_alpha_beta,self.time_limit)
        move = minimax.minimax(300, True) if game.current_game_state['turn'] == "white" else minimax.minimax(300, False)
        return move