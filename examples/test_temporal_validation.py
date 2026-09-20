import unittest

from temporal_validation import (
    RaceKey,
    Result,
    actual_order,
    grid_baseline,
    prior_results,
    spearman_order,
)


class TemporalValidationTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            Result(RaceKey(2025, 1), "A", 1, 2),
            Result(RaceKey(2025, 1), "B", 2, 1),
            Result(RaceKey(2025, 2), "A", 1, 1),
            Result(RaceKey(2025, 2), "B", 2, 2),
            Result(RaceKey(2026, 1), "A", 2, 1),
            Result(RaceKey(2026, 1), "B", 1, 2),
        ]

    def test_future_results_cannot_enter_training_cutoff(self):
        target = RaceKey(2025, 2)
        baseline = prior_results(self.rows, target)
        with_more_future = self.rows + [
            Result(RaceKey(2026, 2), "C", 3, 1)
        ]
        self.assertEqual(baseline, prior_results(with_more_future, target))
        self.assertEqual({row.race for row in baseline}, {RaceKey(2025, 1)})

    def test_grid_baseline_and_rank_score(self):
        race = RaceKey(2026, 1)
        self.assertEqual(grid_baseline(self.rows, race), ["B", "A"])
        self.assertEqual(actual_order(self.rows, race), ["A", "B"])
        self.assertEqual(spearman_order(["B", "A"], ["A", "B"]), -1.0)

    def test_duplicate_drivers_are_rejected(self):
        with self.assertRaises(ValueError):
            spearman_order(["A", "A"], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
