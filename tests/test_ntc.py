import unittest
from ntc import NTC


class TestNTC(unittest.TestCase):
    def setUp(self):
        self.ntc = NTC()

    def test_name_valid_color(self):
        result = self.ntc.name('#6195ED', 'en')
        self.assertIn('color', result)
        self.assertIn('shade', result)

    def test_name_invalid_color(self):
        result = self.ntc.name('invalidcolor', 'en')
        self.assertIsNone(result)

    def test_exact_match(self):
        result = self.ntc.name('#FFFFFF', 'en')
        self.assertEqual(result['color']['name'], 'White')
        self.assertTrue(result['color']['exact'])

    def test_locale_fallback(self):
        result = self.ntc.name('#6195ED', 'nonexistent')
        self.assertIn('color', result)
        self.assertIn('shade', result)


if __name__ == '__main__':
    unittest.main()
