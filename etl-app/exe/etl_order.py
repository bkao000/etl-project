import csv
#import yaml
from ruamel.yaml import YAML
from pathlib import Path
import locale
import datetime
import transformation
#import os
#from lib.transformation.transformation import Transformation
#import sys
#print('sys.path = {0}'.format(sys.path))
#print('cwd = {0}'.format(os.getcwd()))

#sys.path.append('/Users/brendakao/my-app/crisp-lib')

#data = yaml.load(open('./cfg/order.yaml'))
#print(data['OrderID']['col'])

path = Path('./etl-app/cfg/order.yaml')
yaml = YAML(typ='safe')
mapping = yaml.load(path)['mapping']
#print(type(mapping)) 
#print(data)
#print(mapping[0]['tgt'])

'''
with open('./cfg/order.yaml') as cfg_file:
    docs = yaml.safe_load_all(cfg_file)
    for doc in docs:
        print(doc[0])
cfg_file.close()    
'''

output_rst = []
output_header_lst = []
output_row_lst = []
set_output_header = False

t = transformation.Transformation()
# with open('/Users/brendakao/my-app/crisp-test/src/orders.csv') as order_file:
with open('./etl-app/src/orders.csv') as order_file:
#    print(os.getcwd())
    reader = csv.DictReader(order_file)

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    
    for row in reader:
        print(row)
        for i in range(len(mapping)):
            #print(mapping[i]['tgt'])
            #print(mapping[i]['type'])
            #tgt_type = mapping[i]['type']
            if  set_output_header is False:
                output_header_lst.append(mapping[i]['tgt'])
            match mapping[i]['type']:
                case 'Integer':
                    try:
                        #tgt_int_value = int(row[mapping[i]['src']])
                        tgt_int_value = t.StringToInt(row[mapping[i]['src']])
                    except ValueError:
                        tgt_int_value = None
                    print('{0}: {1}     {2}'.format(mapping[i]['tgt'], tgt_int_value, mapping[i]['type']))
                    output_row_lst.append(tgt_int_value)
                case 'BigDecimal':
                    try:
                        #tgt_float_value = '%.2f' % locale.atof(row[mapping[i]['src']])
                        tgt_float_value = t.StringToFloat(row[mapping[i]['src']], 2)
                    except ValueError:
                        tgt_float_value = None
                    output_row_lst.append(tgt_float_value)
                    print('{0}: {1}     {2}'.format(mapping[i]['tgt'], tgt_float_value, mapping[i]['type']))
                case 'Date':
                    if mapping[i]['function'] == 'FormatDate':
                        #date_string = '%s-%2s-%2s' % (row[mapping[i]['src'][0]], row[mapping[i]['src'][1]].zfill(2), row[mapping[i]['src'][2]].zfill(2)) 
                        #print(date_string)
                        #tgt_date_value = datetime.strptime(date_string, "%Y-%m-%d")
                        #tgt_date_value = datetime.datetime(int(row[mapping[i]['src'][0]]), int(row[mapping[i]['src'][1]]), int(row[mapping[i]['src'][2]]))
                        tgt_date_value = t.FormatDate(row[mapping[i]['src'][0]], row[mapping[i]['src'][1]], row[mapping[i]['src'][2]])
                        #print(tgt_date_value)
                        print('{0}: {1}     {2}'.format(mapping[i]['tgt'], tgt_date_value, mapping[i]['type'])) 
                    else:
                        print('{0}: {1}     {2}'.format(mapping[i]['tgt'], row[mapping[i]['src']], mapping[i]['type']))
                    output_row_lst.append(tgt_date_value)
                case 'String':
                    #print('{0}: {1}     {2}'.format(mapping[i]['tgt'], mapping[i]['src'], mapping[i]['type']))
                    if mapping[i]['src'] == 'n/a':
                        tgt_str_value = mapping[i]['default']
                    else:
                        tgt_str_value = row[mapping[i]['src']]
                        print('1: tgt_str_value = {0}'.format(tgt_str_value))
                        try:
                            if mapping[i]['case'] == 'TitleCase':
                                tgt_str_value = tgt_str_value.title()    
                                #print('case = |{0}|'.format(mapping[i]['case']))
                            print('2: tgt_str_value = {0}'.format(tgt_str_value))
                        except:
                            pass # print('case not defined')
                    print('{0}: {1}     {2}'.format(mapping[i]['tgt'], tgt_str_value, mapping[i]['type']))
                    output_row_lst.append(tgt_str_value)
                case _:        
                        print('{0}: {1}     {2}'.format(mapping[i]['tgt'], mapping[i]['src'], mapping[i]['type'])) 
        if set_output_header is False:
            output_rst.append(output_header_lst)   
            set_output_header = True
        output_rst.append(output_row_lst)
        output_row_lst = []
    '''
        (order_number, year, month, day, product_number, product_name, count, extra_col1, extra_col2, empty_col) = row
        print('order_number = '+row['Order Number'])
        print('year = '+row['Year'])
        print('month = '+row['Month'])
        print('day = '+row['Day'])
        print('product_number = '+row['Product Number'])
        print('product_name = '+row['Product Name'])
        print('count = '+row['Count'])
        print('unit = kg')
    '''

    order_file.close()
    
print(output_rst)
with open('./etl-app/tgt/order.csv', 'w+') as output_file:
    write = csv.writer(output_file)
    write.writerows(output_rst)