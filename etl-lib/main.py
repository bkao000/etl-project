from transformation import Transformation

t = Transformation()

t.about()
print('Data transformation examples:\n')
print('\tStringToInteger(\'111\') = {0}'.format(t.StringToInteger('111')))
print('\tFormatDate(\'2018\', \'12\', \'15\') = {0}'.format(t.FormatDate('2018', '12', '15')))
print('\tStringToFloat(\'2,500.51\', \'2\') = {0}'.format(t.StringToFloat('2,500.51', 2)))
print('\tStringToFloat(\'3500.5\', \'2\') = {0}'.format(t.StringToFloat('3500.5', 2)))
print('\tStringToFloat(\'500.5\', \'2\') = {0}'.format(t.StringToFloat('500.5', 2)))
print('\tStringToTitleCase(\'Iceberg lettuce\') = {0}'.format(t.StringToTitleCase('Iceberg lettuce')))
print('\tStringToLowerCase(\'Iceberg lettuce\') = {0}'.format(t.StringToLowerCase('Iceberg lettuce')))
print('\tStringToUpperCase(\'Iceberg lettuce\') = {0}'.format(t.StringToUpperCase('Iceberg lettuce')))
print('\n*** End ***\n')