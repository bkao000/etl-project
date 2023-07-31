import unittest
from datetime import date, datetime
from transformation import Transformation

class TransformationTestCase(unittest.TestCase):
    
    def setUp(self):
        self.transformation = Transformation()
        
    def test_StringToInteger(self):
        result = self.transformation.StringToInteger('111')
        self.assertEqual(result, 111)
        
    def test_StringToFloat(self):
        result = self.transformation.StringToFloat('5,150.5', 2)
        self.assertEqual(result, '%.2f' % 5150.50)

    def test_StringToFloat(self):
        result = self.transformation.StringToFloat('6150.5', 2)
        self.assertEqual(result, '%.2f' % 6150.50)

    def test_FormatDate(self):
        result = self.transformation.FormatDate('2018', '12', '15')
        self.assertEqual(result, datetime(2018, 12, 15, 0, 0, 0))

    def test_StringToDate(self):
        result = self.transformation.StringToDate('2020-01-01', '%Y-%m-%d')
        self.assertEqual(result, date(2020, 1, 1))

    def test_StringToTitleCase(self):
        result = self.transformation.StringToTitleCase('Iceberg lettuce')
        self.assertEqual(result, 'Iceberg Lettuce')

    def test_StringToUpperCase(self):
        result = self.transformation.StringToUpperCase('Iceberg lettuce')
        self.assertEqual(result, 'ICEBERG LETTUCE')

    def test_StringToLowerCase(self):
        result = self.transformation.StringToLowerCase('Iceberg lettuce')
        self.assertEqual(result, 'iceberg lettuce')

if __name__ == '__main__':
    unittest.main()