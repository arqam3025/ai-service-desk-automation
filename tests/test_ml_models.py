import unittest
from ml_models import synthetic_tickets, train_and_evaluate, predict_ticket

class MLTests(unittest.TestCase):
    def test_repeatable_data(self):
        a = synthetic_tickets()
        b = synthetic_tickets()
        self.assertEqual(a[0], b[0])
    def test_evaluation(self):
        _, _, scores = train_and_evaluate()
        self.assertEqual(scores['test_rows'], 80)
        self.assertGreaterEqual(scores['classification_accuracy'], 0)
    def test_predict(self):
        result = predict_ticket('Password reset', 'Cannot login to portal')
        self.assertGreaterEqual(result['simulated_sla_breach_risk'], 0)
        self.assertLessEqual(result['simulated_sla_breach_risk'], 1)

if __name__ == '__main__':
    unittest.main()
