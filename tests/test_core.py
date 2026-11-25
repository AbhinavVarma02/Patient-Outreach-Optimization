import hashlib
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from patient_outreach.acquisition import Entry, load_manifest, receive
from patient_outreach.estimators import contrast_scores, difference_in_means, holm, summarize
from patient_outreach.power import Pilot


class EstimatorTests(unittest.TestCase):
    def test_aipw_exact_fixture(self):
        scores = contrast_scores([0, 1], [0, 1], [0.5, 0.5], [0.25, 0.25], [0, 0], [1, 1])
        self.assertEqual(scores, [0.25, 0.25])
        self.assertEqual(summarize(scores).se, 0)

    def test_ipw_and_holm(self):
        scores = contrast_scores([0, 1], [1, 1], [0.75, 0.75], [1, 1], [0, 0], [0, 0])
        self.assertEqual(scores, [-4, 4/3])
        self.assertEqual(holm([0.04, 0.01, 0.03]), [0.06, 0.03, 0.06])

    def test_invalid_propensity_and_missing_outcome(self):
        with self.assertRaises(ValueError):
            contrast_scores([0], [0], [1], [1], [0], [0])
        with self.assertRaises(ValueError):
            difference_in_means([0, 0, 1, 1], [0, 0, 1, float("nan")])

    def test_intent_to_treat(self):
        effect = difference_in_means([0, 1, 0, 1], [0, 1, 0, 1])
        self.assertEqual((effect.value, effect.lower, effect.upper), (1, 1, 1))


class PilotTests(unittest.TestCase):
    def test_two_sided_threshold_and_attrition(self):
        pilot = Pilot(0.315, 0.026, 0.20, 2, 0.7, 0.5, 0.05, 0.05)
        n = pilot.enrollment(0.8)
        assert n is not None
        self.assertGreaterEqual(pilot.power(n), 0.8)
        self.assertLess(pilot.power(n-1), 0.8)
        self.assertAlmostEqual(pilot.rates()[1] - pilot.rates()[0], 0.00364)
        self.assertGreater(n, Pilot(0.315, 0.026, 0.20, 2, 0.7, 0.5, 0.05).enrollment(0.8))

    def test_identical_policies(self):
        pilot = Pilot(0.32, 0.02, 1, 3, 1, 0.5, 0.05)
        self.assertIsNone(pilot.enrollment(0.8))
        self.assertAlmostEqual(pilot.power(500), 0.05)

    def test_impossible_subgroup(self):
        with self.assertRaises(ValueError):
            Pilot(0.98, 0.04, 0.2, 2, 0.7, 0.5, 0.05).rates()


class AcquisitionTests(unittest.TestCase):
    def test_pinned_manifest(self):
        manifest = load_manifest()
        self.assertEqual(len(manifest), 20)
        self.assertEqual({entry.study for entry in manifest}, {1, 2, 3, 4})

    def test_verified_atomic_write_and_quarantine(self):
        with TemporaryDirectory() as folder:
            target = Path(folder) / "example.txt"
            data = b"example"
            entry = Entry(1, target.name, "/dummy", "x/example.txt", len(data), hashlib.sha256(data).hexdigest())
            receive(entry, io.BytesIO(data), target)
            self.assertEqual(target.read_bytes(), data)
            with self.assertRaisesRegex(ValueError, "quarantined"):
                receive(entry, io.BytesIO(b"mismatch"), target)
            self.assertEqual(target.read_bytes(), data)
            self.assertEqual(len(list((target.parent / "quarantine").iterdir())), 1)
