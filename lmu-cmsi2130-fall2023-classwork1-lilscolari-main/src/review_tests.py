import unittest
import pytest
import queue
from review_exercises import *

class ReviewTests(unittest.TestCase):
    """
    Unit tests for validating answers on the review exercise. Notes:
    - Your correctness score on assignments will typically be assessed by a more complete,
      grading set of unit tests compared to a subset provided in the skeleton, but for this
      introduction, the full set of grading tests are provided.
    - A portion of your style grade will also come from proper type hints; remember to
      validate your submission using `mypy .` and ensure that no issues are found.
    """
    
    # Warmup Tests
    # ---------------------------------------------------------------------------
    
    def test_is_sublist_basic(self) -> None:
        self.assertTrue(is_sublist([1, 3, 2, 2, 1, 3], [1, 2, 3]))
        self.assertFalse(is_sublist([1, 3, 2, 2, 1, 3], [1, 2]))
        
    def test_is_sublist_efficiency(self) -> None:
        BIG_TEST_SIZE = 20000
        self.assertTrue(is_sublist([i for i in range(BIG_TEST_SIZE)], [i for i in range(BIG_TEST_SIZE-1, -1, -1)]))
        self.assertFalse(is_sublist([i for i in range(BIG_TEST_SIZE)], [i for i in range(BIG_TEST_SIZE, 0, -1)]))
    
    # Forneymon Tests
    # ---------------------------------------------------------------------------
    def test_forneymon_equal(self) -> None:
        fm1 = Forneymon("Dampymon", 42, set())
        fm2 = Forneymon("Dampymon", 42, set())
        fm3 = Forneymon("Dampymon", 24, set())
        fm4 = Forneymon("Zappymon", 42, set())
        equal_err = "[X] Ensure that your equal method properly checks for the Forneymon type and then compares attributes."
        self.assertEqual(fm1, fm2, equal_err)
        self.assertNotEqual(fm1, fm3, equal_err)
        self.assertNotEqual(fm1, fm4, equal_err)
        self.assertNotEqual(fm1, "poop", equal_err)
        
    def test_forneymon_hash(self) -> None:
        fm_collection = set()
        fm1 = Forneymon("Dampymon", 42, set())
        fm2 = Forneymon("Dampymon", 42, {fm1})
        fm3 = Forneymon("Dampymon", 24, set())
        hash_err = "[X] Ensure that your __hash__ method hashes only the _name and _health attributes."
        fm_collection.add(fm1)
        fm_collection.add(fm2)
        self.assertEqual(1, len(fm_collection), hash_err)
        fm_collection.add(fm3)
        self.assertEqual(2, len(fm_collection), hash_err)
        
    def test_forneymon_friends(self) -> None:
        fm_collection: set["Forneymon"] = set()
        fm1 = Forneymon("Dampymon", 42, set())
        fm2 = Forneymon("Zappymon", 42, {fm1})
        fm_collection.add(fm1)
        fm_collection.add(fm2)
        fm3 = Forneymon("Friendimon", 101, fm_collection)
        fm3.lose_friend(fm2)
        aliasing_err = "[X] Ensure that your _friends attribute is not an alias of (i.e., reference to) the constructor's argument."
        self.assertEqual(2, len(fm_collection), aliasing_err)
        self.assertIn(fm1, fm_collection, aliasing_err)
        self.assertIn(fm2, fm_collection, aliasing_err)
        self.assertIn(fm1, fm3.get_friends(), aliasing_err)
        self.assertEqual(1, len(fm3.get_friends()), aliasing_err)
        
    def test_forneymon_triage(self) -> None:
        fm1 = Forneymon("Ouch", 3, set())
        fm2 = Forneymon("Im", 1, set())
        fm3 = Forneymon("Hurt", 2, set())
        compare_err = "[X] Ensure that your __lt__ method compares the Forneymon's _health attributes."
        fm_triage: "queue.PriorityQueue[Forneymon]" = queue.PriorityQueue()
        for fm in [fm1, fm2, fm3]: fm_triage.put(fm)
        self.assertEqual(fm2, fm_triage.get(), compare_err)
        self.assertEqual(fm3, fm_triage.get(), compare_err)
        self.assertEqual(fm1, fm_triage.get(), compare_err)
        
    def test_forneymon_name(self) -> None:
        fm1 = Forneymon("Doublemon", 3, set())
        self.assertEqual("DoublemonDoublemon", str(fm1), "[X] Ensure your __str__ method returns the _name attribute repeated twice (hint: you can multiply strings in Python).")
        
if __name__ == '__main__':
    unittest.main()