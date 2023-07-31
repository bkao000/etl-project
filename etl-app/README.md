# About The Project
A system to transform the source data in csv format to the target data in csv format with definitions configured in a yaml file.

### Design Document
etl-project/etl-app/doc/etl-project-design.pdf

### Requirements
python 3.10
module ruamel-yaml
module transformation

### Installation
1. Uncompress etl-project.tgz file.
2. Ensure python 3.10 is installed and set up in system path
3. Install ruamel-yaml module
    - Run the command:
        python -m pip install ruamel-yaml
4. Install transformation module
    - Change to etl-project/etl-lib/transformation directory
    - Run these commands:
        python setup.py sdist
        python install .
    - See module README.md for usage and unittest
5. export ETL_PROJECT=(path to etl-project)

### Get started
How to run the job to process orders data?

```
Run the command: 
    python ${ETL_PROJECT}/etl-app/exe/orders.py [-s source_file] [-c config_file] [-o output_file]
    Python ${ETL_PROJECT}/etl-app/exe/etl_order.py [--source_file=source_file] [--config_file=config_file] [--output_file=output_file]

* If you don't provide any options for source file, config file and output file the following default files will be used.
    Source file: ${ETL_PROJECT}/etl-app/src/orders.csv
    Config file: ${ETL_PROJECT}/etl-app/cfg/order.yaml 
    Output file: ${ETL_PROJECT}/etl-app/tgt/order-output.csv

* Error file name is by adding a prefix 'err-' to the output file name: ${ETL_PROJECT}/etl-app/tgt/err-order-output.csv
```

### Tests
Tests can be conducted by providing specific source data file and/or specific yaml file.

* Test yaml file configured with target String in TitleCase.
python ${ETL_PROJECT}/etl-app/exe/etl_order.py -s orders.csv -c order-test-titlecase.yaml -o order-output-test-titlecase.csv

* Test yaml file configured with target String in UpperCase.
python ${ETL_PROJECT}/etl-app/exe/etl_order.py -s orders.csv -c order-test-uppercase.yaml -o order-output-test-uppercase.csv

* Test yaml file configured with target String in LowerCase.
python ${ETL_PROJECT}/etl-app/exe/etl_order.py -s orders.csv -c order-test-lowercase.yaml -o order-output-test-lowercase.csv

* Test yaml file configured with target String in CamelCase and CamelCase does not exist in transformation module.
python ${ETL_PROJECT}/etl-app/exe/etl_order.py -s orders.csv -c order-test-undefined-case.yaml -o order-output-test-undefined-case.csv

* Test yaml file for target data type requires a function defined but is missing.
python ${ETL_PROJECT}/etl-app/exe/etl_order.py -s orders.csv -c order-test-no-function.yaml -o order-output-test-no-function.csv

* Test yaml file for target data not available from source and should be defined with a default value.
python ${ETL_PROJECT}/etl-app/exe/etl_order.py -s orders.csv -c order-test-no-default.yaml -o order-output-test-no-default.csv

