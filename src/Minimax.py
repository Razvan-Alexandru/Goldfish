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

    def generate_game_tree(self, game_state, depth, is_maximizing):
        root_node = MinimaxTreeNode(game_state, self.evaluator, maxDepth=depth, depth=0, is_maximizing=is_maximizing)
        nodes_to_explore = [root_node]
        
        while nodes_to_explore:
            current_node = nodes_to_explore.pop()
            
            if current_node.depth < depth:
                current_node.generate_children(self.game) 
                # Sorting for optimal pruning
                if self.use_alpha_beta:
                    current_node.children.sort(
                    key=lambda x: (x.score if x.score is not None else -math.inf) if current_node.is_maximizing else (x.score if x.score is not None else math.inf),
                    reverse=current_node.is_maximizing
                     )
                    
                nodes_to_explore.extend(current_node.children)  

        return root_node

    # Returns the best move
    def getMove(self, game_state, depth, maximizing_player):
        self.start_time = time.time()
        root_node = self.generate_game_tree(game_state, depth, maximizing_player)
        
        alpha = -math.inf
        beta = math.inf
        best_move = None

        best_move = self.minimax(root_node, depth, alpha, beta, maximizing_player,self.use_alpha_beta).move

        if best_move:
            best_move = self.convert_to_notation(best_move[0], best_move[1])
            print(f'{self.game.current_game_state["turn"].capitalize()} to move: {best_move}')
        
        return best_move
            
    def minimax(self, node, depth, alpha, beta, maximizingPlayer, use_alpha_beta):
        # Base case
        if depth == 0 or not node.children:
            return node 

        best_node = None 

        if maximizingPlayer:
            v = -math.inf  
            for child in node.children:
                child_node = self.minimax(child, depth - 1, alpha, beta, False, use_alpha_beta)
                score = child_node.score
                if score > v: 
                    v = score
                    best_node = child_node
                alpha = max(alpha, v) 
                if use_alpha_beta and beta <= alpha: 
                    break  
            return best_node

        else:
            v = math.inf  
            for child in node.children:
                child_node = self.minimax(child, depth - 1, alpha, beta, True, use_alpha_beta)
                score = child_node.score
                if score < v:
                    v = score
                    best_node = child_node
                beta = min(beta, v)  
                if beta <= alpha:
                    break
            return best_node
  
# Tree node for Minimax
class MinimaxTreeNode:
    def __init__(self, game_state, evaluator, maxDepth, move=None, depth=0, is_maximizing=False):
        self.game_state = game_state
        self.move = move
        self.depth = depth
        self.is_maximizing = is_maximizing
        self.children = []
        self.score = None
        self.evaluator = evaluator
        self.maxDepth = maxDepth

    def generate_children(self, game):
        # Generate valid moves based on the current game state
        valid_moves = game.valid_moves(self.game_state)        
        # For each valid move, create a child node
        for move in valid_moves:
            new_game_state = copy.deepcopy(self.game_state)
            game.make_move(new_game_state, move)
            child_node = MinimaxTreeNode(new_game_state, self.evaluator ,self.maxDepth, move, self.depth + 1, not self.is_maximizing)
           
            # Max depth reached, evaluate node
            if child_node.depth >= self.maxDepth: 
                child_node.score = self.evaluator.evaluate(child_node.game_state)
            
            # Add the child node to the current node's children
            self.children.append(child_node)
