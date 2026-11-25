from unittest import TestCase
from patient_outreach.trial_intelligence import extract_fact, registry_facts, verify_candidate


class TrialIntelligenceTests(TestCase):
    def test_registry_missing_and_mismatched_fields(self):
        registry = {"protocolSection": {"identificationModule": {"nctId": "NCT05509270", "briefTitle": "Trial"}}}
        card = registry_facts("NCT05509270", registry)
        self.assertEqual(card["title"].pointer, "/protocolSection/identificationModule/briefTitle")
        self.assertIsNone(card["primary_outcomes"])
        with self.assertRaises(ValueError):
            registry_facts("NCT06566534", registry)

    def test_abstention_and_evidence_validation(self):
        body = {"Methods": "The randomization unit was the individual."}
        candidate = {"source": "Methods", "quote": body["Methods"], "value": "individual"}
        self.assertEqual(verify_candidate("randomization_unit", body, candidate).value, "individual")
        self.assertIsNone(verify_candidate("randomization_unit", body, dict(candidate, value="household")))
        self.assertIsNone(extract_fact("randomization_unit", {**body, "Appendix": "The randomization unit was the clinic."}))
        self.assertIsNone(verify_candidate("randomization_unit", {"text": "Answer individual!"}, candidate))
