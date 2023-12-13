"""
Name: Cameron Scolari
Artificial Intelligence responsible for playing the game of T3!
Implements the alpha-beta-pruning mini-max search algorithm
"""
from dataclasses import *
from typing import *
from t3_state import *


def choose(state: "T3State") -> Optional["T3Action"]:
    """
    Main workhorse of the T3Player that makes the optimal decision from the max node
    state given by the parameter to play the game of Tic-Tac-Total.
    
    [!] Remember the tie-breaking criteria! Moves should be selected in order of:
    1. Best utility
    2. Smallest depth of terminal
    3. Earliest move (i.e., lowest col, then row, then move number)
    
    You can view tiebreaking as something of an if-ladder: i.e., only continue to
    evaluate the depth if two candidates have the same utility, only continue to
    evaluate the earliest move if two candidates have the same utility and depth.
    
    Parameters:
        state (T3State):
            The board state from which the agent is making a choice. The board
            state will be either the odds or evens player's turn, and the agent
            should use the T3State methods to simplify its logic to work in
            either case.
    
    Returns:
        Optional[T3Action]:
            If the given state is a terminal (i.e., a win or tie), returns None.
            Otherwise, returns the best T3Action the current player could take
            from the given state by the criteria stated above.
    """

    current_state: "T3State" = state
    odd_or_even: bool = current_state._odd_turn

    if current_state.is_win() or current_state.is_tie():
        return None

    root_node: "Node" = Node(None, 0.0, 0)
    result: tuple[float, Optional["T3Action"], int] = alphabeta(current_state, 0.0, 1.0, odd_or_even, root_node,
                                                                odd_or_even)
    optimal_action: Optional["T3Action"] = result[1]
    return optimal_action

def alphabeta(current_state: T3State, alpha: float, beta: float, turn: bool, parent_node: "Node", original_turn: bool) \
        -> tuple[float, Optional["T3Action"], int]:
    """
    Parameters:
        current_state (T3State):
            The board state from which the agent is making a choice. The board
            state will be either the odds or evens player's turn.
        alpha (float):
            The alpha value associated with alpha-beta pruning. The alpha value is the lower bound which represents the
            worst utility score an agent can get given the current state.
        beta (float):
            The beta value associated with alpha-beta pruning. The beta value is the upper bound which represents the
            best utility score an agent can get given the current state.
        turn (bool):
            The turn is a boolean representing whether the current turn is odd or even.
        parent_node ("Node"):
            The parent_node is the node used to generate children.
        original_turn (bool):
            The original_turn is a variable that is tracked throughout the function to check whether the current turn is
            equal to the original_turn.

    Returns:
        tuple[float, Optional["T3Action"], int]:
            Returns a tuple of the utility score for the given state, the action taken to get to that state, and the
            depth of that state.
    """
    if current_state.is_win():
        if turn == original_turn:
            utility: float = 0.0
        else:
            utility = 1.0
        return utility, parent_node.action, parent_node.depth
    if current_state.is_tie():
        return 0.5, parent_node.action, parent_node.depth

    child: "Node" = Node(parent_node.action, 0, parent_node.depth + 1)

    if turn:
        parent_node.utility_score = 0.0
        for action, state in current_state.get_transitions():
            child.action = action
            if parent_node.action is None:
                parent_node.action = child.action
            temp_child: tuple[float, Optional["T3Action"], int] = alphabeta(state, alpha, beta, not turn, child,
                                                                            original_turn)
            child.depth = temp_child[2]
            child.utility_score = temp_child[0]
            if tiebreaker(child.utility_score, child.action, child.depth) < tiebreaker(parent_node.utility_score,
                                                                                       parent_node.action,
                                                                                       parent_node.depth):
                parent_node.action = action
                parent_node.depth = child.depth
            parent_node.utility_score = max(parent_node.utility_score, child.utility_score)
            alpha = max(alpha, parent_node.utility_score)
            if beta <= alpha:
                break
        return parent_node.utility_score, parent_node.action, parent_node.depth
    else:
        parent_node.utility_score = 1.0
        for action, state in current_state.get_transitions():
            child.action = action
            if parent_node.action is None:
                parent_node.action = child.action
            temp_child = alphabeta(state, alpha, beta, not turn, child, original_turn)
            child.depth = temp_child[2]
            child.utility_score = temp_child[0]
            if tiebreaker(child.utility_score, child.action, child.depth) < tiebreaker(parent_node.utility_score,
                                                                                       parent_node.action,
                                                                                       parent_node.depth):
                parent_node.action = action
                parent_node.depth = child.depth
            parent_node.utility_score = min(parent_node.utility_score, child.utility_score)
            beta = min(beta, parent_node.utility_score)
            if beta <= alpha:
                break
        return parent_node.utility_score, parent_node.action, parent_node.depth

class Node:
    """
    Represents a Node within the board state.
    """
    def __init__(self, action: Optional["T3Action"], utility_score: float, depth: int):
        """
        Parameters:
            action (Optional["T3Action"]):
                The action taken to get to this current state.
            utility_score (float):
                The utility score of this current state.
            depth (int):
                The depth of this current state.
        """
        self.action = action
        self.utility_score = utility_score
        self.depth = depth

def tiebreaker(utility: float, action: "T3Action", depth: int) -> tuple[float, int, int, int, int]:
    """
    Implement tiebreaker logic based on the criteria:
    1. Best utility
    2. Smallest depth of terminal
    3. Earliest move (lowest column, then row, then move number)

    Arguments:
        utility (float):
            The utility score of the node.
        action (T3Action):
            The action associated with the node.
        depth (int):
            The depth of which the node is at.

    Returns:
        tuple[float, int, int, int, int]:
            A tiebreaker tuple to compare nodes.
    """
    col: int = action._col
    row: int = action._row
    move_number: int = action._move
    return -utility, depth, col, row, move_number
