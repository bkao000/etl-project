from transformation import Transformation

t = Transformation()

t.about()
print(t.StringToInt('111'))
print(t.FormatDate('2018', '12', '15'))
print(t.StringToFloat('2,500.51', 2))
print(t.StringToFloat('3500.5', 2))
print(t.StringToFloat('500.5', 2))