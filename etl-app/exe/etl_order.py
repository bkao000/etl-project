import csv
from ruamel.yaml import YAML
from pathlib import Path
import locale
import datetime
from datetime import date
import transformation           # custom built etl transformation library

path = Path('./etl-app/cfg/order.yaml')
yaml = YAML(typ='safe')
mapping = yaml.load(path)['mapping']

output_header = []
output_header_flag = False
output_row_lst = []         # List to save output data of a row
output_rst = []             # List to save output rows
invalid_row_lst = []
invalid_row_flag = False

t = transformation.Transformation()

with open('./etl-app/src/orders.csv') as order_file:
    reader = csv.DictReader(order_file)
    
    for row in reader:
        #print(row)
        for i in range(len(mapping)):
            # Get target data header once
            if output_header_flag is False:
                output_header.append(mapping[i]['tgt'])
            
            # Transform data based on target field definition in yaml file
            match mapping[i]['type']:
                case 'Integer':
                    try:
                        tgt_int_value = t.StringToInteger(row[mapping[i]['src']])
                        output_row_lst.append(tgt_int_value)
                    except ValueError:
                        tgt_int_value = None
                    if tgt_int_value is None:
                        invalid_row_flag = True# Invalid row needs to be captured
                case 'BigDecimal':
                    try:
                        tgt_float_value = t.StringToFloat(row[mapping[i]['src']], 2)
                        output_row_lst.append(tgt_float_value)
                    except ValueError:
                        tgt_float_value = None
                        # Invalid row needs to be captured
                case 'Date':
                    if mapping[i]['function'] == 'FormatDate':
                        tgt_date_value = t.FormatDate(row[mapping[i]['src'][0]], row[mapping[i]['src'][1]], row[mapping[i]['src'][2]])
                    else:
                        tgt_date_value = None
                    if tgt_date_value:
                        output_row_lst.append(tgt_date_value)
                    else:
                        invalid_row_flag = True
                case 'String':
                    if mapping[i]['src'] == 'n/a':
                        tgt_str_value = mapping[i]['default']
                    else:
                        tgt_str_value = row[mapping[i]['src']]
                        try:
                            match mapping[i]['case']:
                                case 'TitleCase':
                                    tgt_str_value = t.StringToTitleCase(tgt_str_value)
                                case 'LowerCase':
                                    tgt_str_value = t.StringToLowerCase(tgt_str_value)
                                case 'UpperCase':
                                    tgt_str_value = t.StringToUpperCase(tgt_str_value)
                                case _:
                                    print('Undefined String Case Type: {0}'.format(mapping[i]['case']))
                                    # Invalid row needs to be captured
                        except:
                            pass # print('case not defined')
                            # Invalid row needs to ba captured
                    output_row_lst.append(tgt_str_value)
                case _:        
                        print('{0}: {1}     {2}'.format(mapping[i]['tgt'], mapping[i]['src'], mapping[i]['type'])) 
        if invalid_row_flag is False:
            if output_header_flag is False:
                output_rst.append(output_header)
                output_header_flag = True
            output_rst.append(output_row_lst)
        else:
            invalid_row_lst.append(row.values())
            invalid_row_flag = False# append the current row transformed output to result data set
        output_row_lst = []                 # clear the row buffer
 
current_date = str(date.today())

# Write results to output file    
with open('./etl-app/tgt/order_'+current_date+'.csv', 'w+') as output_file:
    write = csv.writer(output_file)
    write.writerows(output_rst)
    
with open('./etl-app/err/order-err_'+current_date+'.csv', 'w+') as bad_data_file:
    write = csv.writer(bad_data_file)
    write.writerow(reader.fieldnames)
    write.writerows(invalid_row_lst)
    