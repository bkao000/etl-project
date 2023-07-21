import unittest
from transformation import Transformation

class TransformationTestCase(unittest.TestCase):
    
    def setUp(self):
        self.transformation = Transformation()
        
    def test_string_to_integer(self):
        result = self.transformation.StringToInt('111')
        self.assertEqual(result, 111)
        
    def test_string_to_float(self):
        result = self.transformation.StringToFloat('5,150.5', 2)
        self.assertEqual(result, '%.2f' % 5150.50)

    def test_string_to_float(self):
        result = self.transformation.StringToFloat('6150.5', 2)
        self.assertEqual(result, '%.2f' % 6150.50)

if __name__ == '__main__':
    unittest.main()