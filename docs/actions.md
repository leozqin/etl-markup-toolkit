# Actions
Actions are the most atomic unit of configuration within EMT. Each action corresponds to a native spark operation that is carried out upon execution of the ETL Process. All actions take arguments in the form of key-value pairs. Some arguments require/support complex types such as arrays and arrays of objects.

[Click here to return to the README](../README.md)

# Universal arguments
All actions support the following arguments:

`comment`: A way of passing un-executed data from the configuration into the ETL Process. Typically, this can be a string with more details about why the action works in a certain way, but `yaml`-compliant complex types are also supported.

`diagnostic_mode`: This is a boolean value that instructs EMT to emit additional logging during the processing of this action. The values are that emitted during diagnostic mode can be controlled by the global configs. By default, this is `false`

```yaml
- action: do_nothing
  comment: wow, an action that does nothing
  diagnostic_mode: true
```

# I/O Actions
I/O actions are concerned with reading and writing data.

The supported I/O Actions are (click through to read more):
1. [Read - Read data from a filesystem](io_actions.md#read)
2. [Write - Write data using to a filesystem](io_actions.md#write)

# Flow Actions
Flow actions are concerned with control flow of the data

The supported Flow actions are (click through to read more):
1. [Select - Select only certain fields](flow_actions.md#select)
2. [Drop - Drop certain fields](flow_actions.md#drop)
3. [Rename - Rename certain fields from one name to another](flow_actions.md#rename)
4. [Join - Join the current workflow to another one](flow_actions.md#join)
5. [Filter - Filter the rows in the workflow and optionally send them to another workflow](flow_actions.md#filter)
6. [Do Nothing - takes no action](flow_actions.md#do-nothing)
7. [Union Workflows - unions two or more workflows together](flow_actions.md#union-workflows)
8. [Copy Workflows - copy an existing workflow into a new one](flow_actions.md#copy-workflows)
9. [Cache - persist the workflow using the specified storage level](flow_actions.md#cache)
10. [Coalesce - reduce the number of partitions for the workflow](flow_actions.md#coalesce)
11. [Repartition - shuffle the data by column(s) or into a number of partitions](flow_actions.md#repartition)
12. [Explode - turns a single row into multiple rows based on an array field](flow_actions.md#explode)

# Calculation Actions
Calculation actions use one or more fields to calculate another value.

The support Calculation actions are (click through to read more):
1. [Comparison - Compare one or more fields and return a boolean outcome](calc_actions.md#comparison)
2. [Aggregation - Group by one or more fields and take aggregations](calc_actions.md#aggregation)
3. [Checksum - Calculate the checksum value for a field](calc_actions.md#checksum)
4. [Scalar - Apply a scalar function to one or more columns](calc_actions.md#scalar)
5. [Math - Do a mathematical operation on one or more operands](calc_actions.md#math)

# Value Actions
Value actions change the value of a field by applying formatting or replacing certain values with others.

The supported Value actions are (click through to read more):
1. [Replace Values - Replace values in one or more columns with another value](value_actions.md#replace-values)
2. [Convert Values - converts columns from one datatype to another](value_actions.md#convert-values)
3. [Standardize Values - standardizes value from one mapped value to another](value_actions.md#standardize-values)
4. [Constant - adds a column with a constant value](value_actions.md#constant)
5. [Concatenate - concatenates two or more columns, with or without a separator](value_actions.md#concatenate)
6. [String Format - applies formatting to a string column](value_actions.md#string-format)
7. [String Pad - pads a string until it is a certain length](value_actions.md#string-pad)
8. [Parse Date - extracts date parts or metadata from date fields](value_actions.md#parse-date)
9. [Split - convert a field into an array field using a delimiter](value_actions.md#split)
10. [Substring - extract a substring from a string field](value_actions.md#substring)