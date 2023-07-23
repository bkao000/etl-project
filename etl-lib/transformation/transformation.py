""" This library provides functions for data transformation """
import locale
import datetime
from ruamel.yaml import YAML

class Transformation:
        
    def about(self):
        print("\n*** This Library provides functions for data transformation ***\n")
        
    def StringToInteger(self, s):
        try:
            return int(s)
        except:
            return None

    def FormatDate(self, year, month, day):
        try:
            return datetime.datetime(int(year), int(month), int(day))
        except:
            return None

    def StringToFloat(self, s, decimal_places):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        format_str = '%.'+str(decimal_places)+'f'
        return ( format_str % locale.atof(s))
    
    def StringToTitleCase(self, s):
        return s.title()
    
    def StringToLowerCase(self, s):
        return s.lower()
    
    def StringToUpperCase(self, s):
        return s.upper()
        