import csv
from ruamel.yaml import YAML
from pathlib import Path
from datetime import date
import transformation           # custom built etl transformation library
import re
import os
import getopt, sys

# Read project root path
etl_project = os.environ.get("ETL_PROJECT")
if not etl_project:
    print('Environment variable ETL_PROJECT is not defined. Please run command "export ETL_PROJECT=(path to etl-project directory)"')
    exit()
etl_app = etl_project+'/etl-app'

# Read command line arguments
argumentList = sys.argv[1:]
options = "hs:c:o:"
long_options = ["help", "source_file=", "config_file=", "output_file="]
source_file = "orders.csv"
config_file = "order.yaml"
output_file = "order-output.csv"
try:
    # Parse arguments
    opts, args = getopt.getopt(argumentList, options, long_options)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Usage:\n{0}/etl-app/exe/etl_order.py [-s source_file] [-c config_file] [-o output_file]'.format(etl_project))
            print('{0}/etl-app/exe/etl_order.py [--source_file=source_file] [--config_file=config_file] [--output_file=output_file]'.format(etl_project))
        elif opt in ("-s", "--source_file"):
            source_file = arg
        elif opt in ("-c", "--config_file"):
            config_file = arg
        elif opt in ("-o", "--output_file"):
            output_file = arg
except getopt.errors as err:
    print(str(err))

source_file_full_path = etl_app+'/src/'+source_file         # set source file path
config_file_full_path = etl_app+'/cfg/'+config_file         # set config file path
output_file_full_path = etl_app+'/tgt/'+output_file         # set output file path
error_file_full_path = etl_app+'/err/err_'+output_file      # set error file path

path = Path(config_file_full_path)
yaml = YAML(typ='safe')
mapping = yaml.load(path)['mapping']

# Get target field names
output_header = []
for i in range(len(mapping)):
    output_header.append(mapping[i]['tgt'])

# Initialize variables 
output_row_lst = []         # Output row buffer
output_rst = []             # Output rows
err_row_lst = []            # Error row buffer
err_rst = []                # Error rows
err_desc = ''               # Error description
t = transformation.Transformation()     # ETL transformation functions

with open(source_file_full_path) as order_file:        # Read input data
    reader = csv.DictReader(order_file)        
    for row in reader:                                      # Process row by row
        current_field = ''
        if len(row) != len(reader.fieldnames):              # If count of input fields doesn't match count of header fields log error row
            err_desc ='Incorrect number of input data fields'
            current_field = '*** row level error ***'
        else:
            for i in range(len(mapping)):                   # Process each input row to a generate target row based on definitions in yaml file
                # Transform data based on target field definition in yaml file
                tgt_value = None                            # Set default target field value to None
                current_field = mapping[i]['src']
                match mapping[i]['type']:                   # Transform based on target field type
                    case 'Integer':
                        tgt_value = t.StringToInteger(row[mapping[i]['src']])
                    case 'BigDecimal':
                        tgt_value = t.StringToFloat(row[mapping[i]['src']], 2)
                    case 'Date':
                        try:
                            function = mapping[i]['function']# Use function defined in yaml file to transform data to Date
                        except:
                            function = None
                            err_desc = 'Job stopped with Date function not configured.'
                        if function:
                            match function:
                                case 'FormatDate':
                                    tgt_value = t.FormatDate(row[mapping[i]['src'][0]], row[mapping[i]['src'][1]], row[mapping[i]['src'][2]])
                                case 'StringToDate':
                                    tgt_value = t.StringToDate(mapping[i]['src'], mapping[i]['format'])
                                case _:
                                    err_desc = 'Job stopped with unrecognized function.'
                                    break
                    case 'String':
                        if mapping[i]['src'] == 'n/a':      # Data doesn't come from source
                            try:                            
                                tgt_value = mapping[i]['default']       # Fetch data from default value defined in yaml file
                            except:
                                err_desc = 'Job stopped with missing default value'
                                current_field = 'src: %s, tgt: %s' % (mapping[i]['src'], mapping[i]['tgt'])
                        else:                            
                            try:    # If source format is configured validate the data 
                                src_format = mapping[i]['format']
                            except:
                                src_format = None
                            # Data will be transformed from source
                            if src_format and not re.match(src_format, row[mapping[i]['src']]):  # Validate source data format based on definition in yaml file
                                err_desc = 'Source format \'%s\' not match' % mapping[i]['format']
                            else:
                                tgt_value = row[mapping[i]['src']]    
                                try:    # If target string case is defined transform the data
                                    match mapping[i]['case']:
                                        case 'TitleCase':
                                            tgt_value = t.StringToTitleCase(tgt_value)
                                        case 'LowerCase':
                                            tgt_value = t.StringToLowerCase(tgt_value)
                                        case 'UpperCase':
                                            tgt_value = t.StringToUpperCase(tgt_value)
                                        case _:
                                            err_desc = 'Job stopped with undefined String Case Type: %s' % mapping[i]['case']
                                            break
                                except:
                                        pass
                    case _:        
                        err_desc = 'Unrecognized target type'
                if tgt_value is not None:       
                    output_row_lst.append(tgt_value)
                else:
                    if err_desc == '':
                        err_desc = 'Invalid ' + mapping[i]['type']
                    break
            ### End of for-loop for fields process for a row
        if err_desc == '':
            if len(output_row_lst) == len(output_header):
                output_rst.append(output_row_lst)
            else:
                 err_desc = 'Incorrect number of output fields'        
        if err_desc != '':
            row_data = list(map(lambda x:x if x is not None else '', list(row.values())))
            err_row_lst.append([err_desc, current_field, row_data])
            err_rst.append(err_row_lst)
            if re.match('^Job stopped', err_desc):
                break
            else:
                err_desc = ''
        output_row_lst = []                 # clear the row buffer
    ### End of for-loop for rows process for an input file
    
current_date = str(date.today())
# Open output file    
with open(output_file_full_path, 'w+') as output_file:
    write = csv.writer(output_file)
    write.writerow(output_header)
    write.writerows(output_rst)

# Open err file    
with open(error_file_full_path, 'w+') as bad_data_file:
    write = csv.writer(bad_data_file)
    err_header = ['Error Type', 'Source Field', 'Data ['+','.join(reader.fieldnames)+']']
    err_row_lst.insert(0, err_header)
    write.writerows(err_row_lst)

