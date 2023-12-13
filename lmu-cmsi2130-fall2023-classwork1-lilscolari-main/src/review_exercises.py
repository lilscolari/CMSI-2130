'''
CMSI 2130 - Classwork 1
Author: Cameron Scolari

Complete each exercise as described in the Classwork spec, ensuring that its subsequent
unit test is satisfied by running the associated review_tests.py as indicated in the spec.
'''

from dataclasses import *
from typing import *
import copy


# Warmup Problems
# ---------------------------------------------------------------------------

# FIXME: Add type hints to the parameters and return type of this method
def is_sublist(list1: list[int], list2: list[int]) -> bool:
    '''
    Returns a bool designating whether or not all ints in list1 also appear
    in list2
    
    Parameters:
        list1 (list[int]):
            A list of ints for whom membership is being checked against list2
        list2 (list[int]):
            A list of ints against which list1's members are being checked
    
    Returns:
          bool:
              True if all of list1's ints are also in list2 without needing the
              reverse to be true
        
    Examples:
        is_sublist([1, 3, 2, 1, 3], [1, 2, 3]) => True
        is_sublist([1, 3, 2, 1, 3], [1, 2]) => False
    '''
    # [!] Warning: this method is implemented VERY POORLY at the moment
    # FIXME: Improve the efficiency below through a better choice of data
    # structure and revising the logic!
    return set(list1) == set(list2)


# Forneymon Problems
# ---------------------------------------------------------------------------
class Forneymon:
    '''
    Skeleton class outline for hit new blockbuster game: Forneymon.

    Attributes:
        _name (str):
            The Forneymon's name like "Burneymon" or "Dampymon"
        _health (int):
            The Forneymon's remaining hit points
        _friends (set["Forneymon"]):
            A set of Forneymon references that point to other Forneymon with
            whom this one is friends
    '''

    # FIXME: Add type hints to the parameters of the Forneymon constructor
    def __init__(self, name: str, health: int, friends: set["Forneymon"]):
        '''
        Default constructor for initializing a new Forneymon with the given
        name, health (number of hit points), and set of friends

        Parameters:
            name (str):
                The Forneymon's name like "Burneymon" or "Dampymon"
            health (int):
                The Forneymon's remaining hit points
            friends (set["Forneymon"]):
                A set of Forneymon references that point to other Forneymon with
                whom this one is friends
        '''
        # FIXME: Add type hints to the attributes of the Forneymon class
        self._name: str = name
        self._health: int = health
        # FIXME: Prevent self._friends from being an alias of the argument friends
        self._friends: set["Forneymon"] = copy.deepcopy(friends)

    # TODO: Override the __eq__ method for this class
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Forneymon):
            return self._name == other._name and self._health == other._health
        return False

    # TODO: Override the __hash__ method for this class
    def __hash__(self) -> int:
        return hash((self._name, self._health))

    # TODO: Override the __lt__ method for this class
    def __lt__(self, other: "Forneymon") -> bool:
        return self._health < other._health

    # TODO: Override the __str__ method for this class
    def __str__(self) -> str:
        return self._name * 2

    def add_friend(self, other: "Forneymon") -> None:
        '''
        Adds a reference to the given Forneymon to the set of this Forneymon's friends.
        
        Parameters:
            other (Forneymon):
                The friend to add to this Forneymon's set of friends.
        '''
        self._friends.add(other)

    def lose_friend(self, other: "Forneymon") -> None:
        '''
        Removes a reference to the given Forneymon from the set of this Forneymon's friends.
        So sad :(
        
        Parameters:
            other (Forneymon):
                The friend to remove from this Forneymon's set of friends.
        '''
        self._friends.remove(other)

    def get_friends(self) -> set["Forneymon"]:
        '''
        Returns a deep copy of the set of this Forneymon's friends.
        
        Returns:
            set[Forneymon]:
                A copy of this Forneymon's set of friends.
        '''
        return copy.deepcopy(self._friends)
