'''
CMSI 2130 - Classwork 2
Author: Mike Hennessy and Cameron Scolari

Modify only this file as part of your submission, as it will contain all of the logic
necessary for implementing the breadth-first tree search that solves the basic maze
pathfinding problem.
'''

from queue import Queue
from maze_problem import *
from dataclasses import *


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

    player_loc: tuple[int, int]
    action: str
    parent: Optional["SearchTreeNode"]

    def __str__(self) -> str:
        return "@: " + str(self.player_loc)


def find_solution_path(node: "SearchTreeNode" | Any) -> list[str]:
    """
    Helper method that unravels path taken from initial state to goal state.

    Parameters:
        node (SearchTreeNode):
            Current node along the path from initial state to goal state.

    Returns
        list[str]:
            A solution to the problem: a sequence of actions leading from the
            initial state to the goal (a maze with all targets destroyed).
    """

    solution_path: list[str] = []

    # Iterates through every node in path but the initial_state node:
    while node.parent is not None:
        solution_path.insert(0, node.action)
        # Previous node in path:
        node = node.parent

    # Returns solution_path once initial_state node is reached:
    return solution_path


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

    initial_state: "SearchTreeNode" = SearchTreeNode(problem.get_initial_loc(), "", None)

    frontier: Queue["SearchTreeNode"] = Queue()
    frontier.put(initial_state)

    while not frontier.empty():
        parent_node: "SearchTreeNode" = frontier.get()
        children: dict[str, tuple[int, int]] = problem.get_transitions(parent_node.player_loc)
        for child in children.items():
            # Creates an instance of the SearchTreeNode class:
            new_node: "SearchTreeNode" = SearchTreeNode(child[1], child[0], parent_node)
            # Enter helper method if location of new node is the location of the goal state:
            if new_node.player_loc == problem.get_goal_loc():
                return find_solution_path(new_node)
            frontier.put(new_node)
    # Returns None is no solution to the maze is possible:
    return None
