"""Known-answer tests for community randomization scores and the release projection."""

from importlib.util import find_spec
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


@unittest.skipUnless(find_spec("numpy") and find_spec("scipy"), "Install Haryana research requirements.")
class HaryanaTests(unittest.TestCase):
    def test_known_effect_with_fixed_nuisance(self):
        import numpy as np

        from evaluate_haryana import score_difference

        # One of three villages receives assignment in a block. A misspecified
        # nuisance model does not change the expected contrast under this lottery.
        probability = np.full(3, 1 / 3)
        m = np.array([[1.0, 12.0], [3.0, 9.0], [7.0, 6.0]])
        y0, y1 = np.array([2.0, 4.0, 8.0]), np.array([2.0, 6.0, 9.0])
        scores = []
        for a in np.eye(3):
            scores.append(score_difference(np.where(a == 1, y1, y0), a, probability, m))
        np.testing.assert_allclose(np.mean(scores, axis=0), y1 - y0)
        with self.assertRaisesRegex(ValueError, "support"):
            score_difference(y1, np.ones(3), np.ones(3), m)

    def test_capacity_with_boundary_ties_and_small_roster(self):
        import numpy as np

        from evaluate_haryana import capacity_rule

        np.testing.assert_allclose(capacity_rule(np.array([0.0, 1.0, 1.0, 2.0, 2.0])),
                                   [0, 0.25, 0.25, 1, 1])
        np.testing.assert_allclose(capacity_rule(np.array([2.0])), [0.5])

    def test_cluster_mean_matches_independent_cluster_means(self):
        import numpy as np

        from evaluate_haryana import cluster_mean

        groups = [str(i) for i in range(12)]
        values = np.arange(12.0)
        result = cluster_mean(np.repeat(values, 2), np.repeat(groups, 2).tolist())
        self.assertAlmostEqual(result["estimate"], values.mean())
        self.assertAlmostEqual(result["standard_error"], values.std(ddof=1) / np.sqrt(len(groups)))
        with self.assertRaisesRegex(ValueError, "Too few"):
            cluster_mean(np.array([1.0]), ["one"])

    def test_empirical_policy_projection_is_allowlisted(self):
        from export_haryana import project

        report = json.loads((ROOT / "research/reports/haryana_empirical.json").read_bytes())
        projection = json.loads((ROOT / "web/src/haryana.json").read_bytes())
        self.assertEqual(project(report), projection)
        report["policy_experiment"]["heldout_arm_villages"]["control"] = 10
        with self.assertRaisesRegex(ValueError, "disclosure"):
            project(report)
