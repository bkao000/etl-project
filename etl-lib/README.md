# About The Library
A library for data transformation functions.

### Requirements
python 3.10
### Installation
Install transformation module
    - Change to etl-project/etl-lib/transformation directory
    - Run these commands:
        python setup.py sdist
        python install .

### Usage
How to transform data to transform data with this library:

```Python
from transformation import Transformation

#Instantiate a Transformation object
transformation = Transformation()

# Transform data from string to Integer
result = transformation.StringToInteger('2')
print(result)
>>> 2

# Transform data from string to Float
result = transformation.StringToFloat('2,500.1', 2)
print(result)
>>> 2500.10

# Transform data from Year, Month, Date fields to Date format
result = transformation.FormatDate('2018', '12', '15')
print(result)
>>> 2018-12-15 00:00:00

# Transform data from Year, Month, Date fields to Date format
result = transformation.StringToDate('2020-01-01', '%Y-%m-%d')
print(result)
>>> 2020-01-01

# Transform string to title case
result = transformation.StringToTitleCase('Iceberg lettuce')
print(result)
>>> Iceberg Lettuce

# Transform string to title case
result = transformation.StringToUpperCase('Iceberg lettuce')
print(result)
>>> ICEBERG LETTUCE

# Transform string to title case
result = transformation.StringToLowerCase('Iceberg lettuce')
print(result)
>>> iceberg lettuce
```
