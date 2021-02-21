# Value Actions
[Click here to return to the README](../README.md)

[Click here to return to the Actions page](actions.md)

## Replace Values
The `replace_values` step replaces values in one or more columns with another value.

Arguments:
- `replace`: the value that should be replaced
- `with`: the value with which instances of `replace` should be replaced
- `columns`: optional: an array of the columns to which the replacement should be applied. If no `columns` argument exists then the replacement will be applied to every column.

Example:
```yaml
- action: replace_values
  replace: "?"
  with: null
```

## Convert Values
The `convert_values` converts columns from one datatype to another.

Arguments:
- `type`: the type to which the column should be converted. The supported types are `str`, `date`, `timestamp`, `int`, `double`, and `float`.
- `format`: optional, default `null`: the format that should be used to carry out the conversion. This argument is only evaluated when the value of `type` is `date` or `timestamp`. If the value of this argument is `null` then the default format for that type will be used.
- `columns`: the columns that should be converted into the specified `type`

Example:
```yaml
- action: convert
  type: double
  columns:
  - some_field
  - some_other_field
  - yet_another_field
```

## Standardize Values
The `standardize_values` actions standardizes value from one mapped value to another.

Arguments:
- `mapping`: an object containing key-value pairs, where the key is the original value and the value is the one to which the original value should be standardized.
- `else`: the value that should be used when the original value is not found within the `mapping`
- `columns`: the columns to which the standardization should be applied

Example:
```yaml
- action: standardize_values
  columns:
    - country_abbv
    - country_code
  else: Unknown Country
  mapping:
    USA: United States of America
    US: United States of America
    DE: Germany
    GER: Germany
```

## Constant
The `const` action adds a column with a constant value to all rows of the workflow.

Arguments:
- `name`: the name of the column that should be added
- `value`: the value to set for all rows of that column

Example:
```yaml
- action: const
  name: is_marshmallow_delicious
  value: true
```

## Concatenate
The `concat` action concatenates two or more columns, with or without a separator.

Arguments:
- `name`: the name of the new column containing the concatenated data
- `sep`: optional, default `null`: the character that should be used to separate the concatenated fields
- `columns`: the columns that should be concatenated. The order in which the columns are concatenated matches the order of this array.

Example:
```yaml
- action: concat
  name: city_state
  sep: ", "
  columns:
    - city
    - state
```

## String Format
The `str_format` action applies formatting to a string column.

Arguments:
- `format`: the type of formatting that should be applied. The supported types are `upper`, `lower`, `proper`, `trim`, `left_trim`, `right_trim`, `reverse`
- `columns`: the columns to which the formatting will be applied

Example:
```yaml
- action: str_format
  format: proper
  columns:
    - full_name
    - another_full_name
```

## String Pad
The `str_pad` action pads a string until it is a certain length using the specified character

Arguments:
- `side`: the side of the string that should be padded, supported value are `left` and `right`
- `with`: the character that should be used for the padding
- `length`: the character length to which the string should be padded
- `columns`: the columns that should be padded in the specified manner

Example:
```yaml
- action: str_pad
  with: "0"
  length: 5,
  columns:
    - zip_code
    - another_zip_code