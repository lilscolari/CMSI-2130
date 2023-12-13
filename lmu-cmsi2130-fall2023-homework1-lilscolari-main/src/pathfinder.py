'''
CMSI 2130 - Homework 1
Author: Cameron Scolari

Modify only this file as part of your submission, as it will contain all of the logic
necessary for implementing the A* pathfinder that solves the target practice problem.
'''
from maze_problem import MazeProblem
from dataclasses import *
from typing import *
from queue import PriorityQueue


@dataclass
class SearchTreeNode:
    """
    SearchTreeNodes contain the following attributes to be used in generation of
    the Search tree:

    Attributes:
        player_loc (tuple[int, int]):
            The player's location in this node.
        action (str):
            The action taken to reach this node from its parent (or empty if the root).
        parent (Optional[SearchTreeNode]):
            The parent node from which this node was generated (or None if the root).
    """
    # >> [MC] Don't forget to add docstrings for shot_targets, gn, and fn!

    player_loc: tuple[int, int]
    action: str
    parent: Optional["SearchTreeNode"]
    shot_targets: list[tuple[int, int]]
    # >> [MC] Poor variable name -- what's this hold, what's its purpose? (-0.5)
    # past cost:
    gn: int
    # total cost:
    fn: float

    def __lt__(self, other: "SearchTreeNode") -> bool:
        return self.fn < other.fn
# >> [MC] Leave just a single newline between the end of one method and the start of the next


def find_solution_path(node: "SearchTreeNode") -> list[str]:
    """
        Helper method that unravels path taken from initial state to goal state.

        Parameters:
            node (SearchTreeNode):
                Current node along the path from initial state to goal state.

        Returns:
            list[str]:
                A solution to the problem: a sequence of actions leading from the
                initial state to the goal (a maze with all targets destroyed).
        """
    solution_path: list[str] = []
    while node.parent is not None:
        solution_path.insert(0, node.action)
        node = node.parent
    return solution_path


def heuristic(node: "SearchTreeNode", targets_left: set[tuple[int, int]]) -> float:
    """
    Heuristic method that calculates the estimated future cost given the current node and the remaining targets.

    Parameters:
        node (SearchTreeNode):
            Current node along the path from initial state to goal state.
        targets_left (set[tuple[int, int]]):
            A set containing the targets still yet to be shot.
    Returns:
        float:
            An estimated future cost.
    """
    current_location: tuple[int, int] = node.player_loc
    # future cost:
    hn: float = 0
    min_distance: float = float('inf')
    for target_loc in targets_left:
        distance_x: int = abs(current_location[0] - target_loc[0])
        distance_y: int = abs(current_location[1] - target_loc[1])
        min_distance = min(min_distance, distance_x, distance_y)
        hn += min_distance
    hn += 2

    return node.gn + hn


def pathfind(problem: "MazeProblem") -> Optional[list[str]]:
    """
      The main workhorse method of the package that performs A* graph search to find the optimal
      sequence of actions that takes the agent from its initial state and shoots all targets in
      the given MazeProblem's maze, or determines that the problem is unsolvable.

      Parameters:
          problem (MazeProblem):
              The MazeProblem object constructed on the maze that is to be solved or determined
              unsolvable by this method.

      Returns:
          Optional[list[str]]:
              A solution to the problem: a sequence of actions leading from the
              initial state to the goal (a maze with all targets destroyed). If no such solution is
              possible, returns None.
      """
    initial_state: "SearchTreeNode" = SearchTreeNode(problem.get_initial_loc(), "", None, [], 0, 1)
    initial_targets: set[tuple[int, int]] = problem.get_initial_targets()
    frontier: PriorityQueue["SearchTreeNode"] = PriorityQueue()
    frontier.put(initial_state)
    graveyard: list[tuple[tuple[int, int], list[tuple[int, int]]]] = []
    while not frontier.empty():
        parent_node: "SearchTreeNode" = frontier.get()
        graveyard.append((parent_node.player_loc, parent_node.shot_targets))
        children: dict[str, dict[str, Any]] = problem.get_transitions(parent_node.player_loc, initial_targets ^
                                                                      set(parent_node.shot_targets))
        for action, other in children.items():
            new_node: "SearchTreeNode" = SearchTreeNode(other["next_loc"], action, parent_node,
                                                        list(parent_node.shot_targets), parent_node.gn, 0)
            new_node.gn += other["cost"]
            new_node.fn = heuristic(new_node, initial_targets ^ set(parent_node.shot_targets))
            new_node.shot_targets.extend(other["targets_hit"])
            if set(new_node.shot_targets) == initial_targets:
                return find_solution_path(new_node)
            if (new_node.player_loc, new_node.shot_targets) not in graveyard:
                frontier.put(new_node)
    return None

# ===================================================
# >>> [MC] Summary
# A great submission that shows strong command of
# programming fundamentals, generally good style,
# and a good grasp on the problem and supporting
# theory of A*. Indeed, there is definitely
# a lot to like in what you have above, but
# I think you could have tested it a little more just
# to round out the several edge cases that evaded your
# detection. Give yourself more time to test + debug
# future submissions and you'll be golden!
# ---------------------------------------------------
# >>> [MC] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
#
# [~] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [X] Proper docstrings provided for ALL methods
# [X] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:          88 / 100 (-2 / missed unit test)
# Mypy Penalty:        -0 (-2 if mypy wasn't clean)
# Style Penalty:       -0.5
# Total:                87.5 / 100
# ===================================================