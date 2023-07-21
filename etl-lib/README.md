# A library for data transformation functions.

### Installation
pi install transformation

### Get started
How to transform data to transform data with this library:

```Python
from transformation import Transformation

#Instantiate a Transformation object
transformation = Transformation()

# Transform data from string to Integer
result = transformation.StringToInt(2)

# Transform data from Year, Month, Date fields to Date format
result = transformation.FormatDate('2020', '12', '20')
```
