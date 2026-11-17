import json
from pathlib import Path
import unittest
from optimizer import solve, step

class OptimizerTests(unittest.TestCase):
    def setUp(self):
        self.s = json.loads(Path("fixtures/scenario.json").read_text())
    def test_search_and_trace(self):
        r = solve(self.s)
        self.assertEqual(r["evaluated"], 216)
        self.assertGreater(r["feasible"], 0)
        self.assertEqual(len(r["best"]["trace"]), 3)
        self.assertTrue(all(x["cash"] >= self.s["minimum_cash"] for x in r["best"]["trace"]))
        self.assertEqual(r, solve(self.s))
    def test_fleet_limit(self):
        self.assertIsNone(step(self.s, (200, 4, 0, 0), 26, (4, 1)))
    def test_no_feasible_plan(self):
        with self.assertRaises(ValueError):
            solve({**self.s, "minimum_cash": 1000000})
if __name__ == "__main__":
    unittest.main()
