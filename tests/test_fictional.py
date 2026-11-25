from unittest import TestCase
from patient_outreach.fictional import SHARES, allocate, run


class FrozenPolicyTests(TestCase):
    def test_allocation_handles_ties_at_exact_capacity(self):
        policy = allocate((2, 2, 1), 0.2)
        self.assertAlmostEqual(sum(p*w for p,w in zip(policy,SHARES,strict=True)), 0.2)
        self.assertEqual(policy[0],policy[1])
        self.assertEqual(policy[2],0)

    def test_frozen_seeds_and_results_repeat(self):
        report = run(4, 500, 500)
        self.assertEqual(report, run(4, 500, 500))
        self.assertNotEqual(report["training_seed"],report["evaluation_seed"])
        self.assertEqual(report["results"]["uniform"]["estimate"]["value"],0)
