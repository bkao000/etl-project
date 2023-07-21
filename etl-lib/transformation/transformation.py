""" This library provides functions for data transformation """
import locale
import datetime

class Transformation:
        
    def about(self):
        print("This Library provides functions for data transformation")
        
    def StringToInt(self, s):
        return int(s)

    def FormatDate(self, year, month, day):
        return datetime.datetime(int(year), int(month), int(day))

    def StringToFloat(self, s, decimal_places):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        format_str = '%.'+str(decimal_places)+'f'
        return ( format_str % locale.atof(s))