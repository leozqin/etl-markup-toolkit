# Calculation Actions
[Click here to return to the README](../README.md)

[Click here to return to the Actions page](actions.md)

## Comparison
The `comparison` action compares one or more fields to each other or to specific values within itself and returns a boolean outcome.

Arguments:
- `name`: the name of the boolean column resulting from the comparison
- `else`: optional, default `false`: the value that should be used when the comparison does not evaluate to `true`
- `type`: optional, default `and`: when multiple conditions are involved, the circumstance in which the evaluation should be true, either when all of them are true (`and`) or when any of them are true (`or`)
- `comparisons`: an array of objects, which specify the conditions that should be considering during the comparison. Each object in the array should have the following attributes:
    - `type`: the operator used to carry out the comparison. Supported operators are `=`, `!=`, `>`, `>=`, `<`, and `<=`
    - `columns`: optional, but required if there is no `column` attribute in the object: an array of columns with length 2 that are used as the left and right side of the comparison statement with the configured operator. Only the first two items in the array will be considered.
    - `column`: optional, but required if there is no `columns` attribute in the object: the field that should be used in the comparison
    - `value`: optional, but required if there is a `column` attribute in the object: the value whose presence in the `column` should yield a `true` comparison

In short - the comparison object allows you to define comparisons between columns or values within a column, and use multiple such comparisons to determine the outcome of the overall comparison.

For example:
```yaml
- action: comparison
  name: any_condition_will_do
  type: or
  comparisons:
  - type: ">"
    columns:
    - a_smaller_column
    - a_larger_column
  - type: ">"
    column: a_numeric_column
    value: 50
```

## Aggregation
The `aggregation` action groups by one or more fields and calculates aggregations for other specified fields.

Arguments:
- `columns`: the columns that should be grouped on when taking the aggregation
- `aggregations`: an array of objects that define the aggregation that should be take place based on the grouping defined in `columns`. Each object in the array should have the following attributes:
    - `type`: the nature of the aggregation that should be done. The following aggregation types are supported: `count`, `count_distinct`, `collect_list`, `collect_set`, `average`, `sum`, `first`, `min`, `max`
    - `target`: the field against which the aggregation should be collected, not required if the aggregation type is `count`
    - `name`: the name of the field that should result from collecting the aggregation

More detail on how these individual aggregations function can be found by finding the [corresponding Spark function](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html?highlight=read%20csv#module-pyspark.sql.functions)

Example:
```yaml
- action: aggregate
  columns:
  - make
  aggregations:
  - type: sum
    name: sum_of_things
    target: thing
  - type: average
    name: average_thing
    target: thing
  - type: collect_set
    name: known_things
    target: thing
  - type: count
    name: count_rows_of_things
  - type: count_distinct
    name: types_of_things
    target: thing
```

## Checksum
The `checksum` action calculates the checksum value for a field.

Arguments:
- `type`: the checksum algorithm that should be used to calculate the checksum. The following checksum types are supported: `md5`, `crc32`, `xxhash64`, `hash`, `sha1`, `sha224`, `sha256`, `sha384`, `sha512`
- `columns`: the columns for which a checksum value should be calculated

If the column is not a string column, it will be converted to one prior to the checksum being calculated. More detail on how these individual checksums are calculated can be found by finding the [corresponding Spark function](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html?highlight=read%20csv#module-pyspark.sql.functions).

Example:
```yaml
- action: checksum
  type: sha256
  columns:
  - a_securely_salted_field
```

## Scalar
The `scalar` action applies a scalar function to one or more fields.

Arguments:
- `type`: the scalar function that should be applied to the field. The following functions are supported: `abs`, `acos`, `asin`, `atan`, `ceiling`, `cos`, `cosh`, `degrees`, `exp`, `exp_minus_one`, `factorial`, `floor`, `length`, `log10`, `log_plus_one`, `log2`, `radians`, `sin`, `sinh`, `sqrt`, `tan`, `tanh`
- `columns`: the columns to which the scalar function should be applied

More detail on how these individual scalar functions work can be found by finding the [corresponding Spark function](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html?highlight=read%20csv#module-pyspark.sql.functions).

## Math
The `math` action does a mathematical operation using one or more operands.

Arguments:
- `name`: the name of the field containing the result of the mathematical operations
- `operator`: the operator for the operation you want to do. The supported operations are `add`, `subtract`, `multiple`, `divide`, `exponent`, `modulo`
- `columns`: the columns that will be used in the mathematical operation. The operator will be applied in the order of the columns specified, which can make a difference for operators that are order-dependent.

```yaml
- action: math
  operator: add
  name: total_apples
  columns:
    - my_apples
    - your_apples
```

## Window
The `window` action does calculations over a configurable window.

Arguments:
- `name`: the name of the field containing the result of the window function
- `type`: the type of the window function that should be calculated. Supported values are `sum`, `row_num`, `rank`, `dense_rank`, `cume_dist`, and `percent_rank`
- `target`: optional, default `null`: the name of the column with which the same function should be applied. Only required for `sum` type.
- `partition_by`: optional, default `[]` (partition over the entire workflow): an array of the columns that should be included within the partition expression
- `order_by`: optional, default `[]` (no sorting applied): an array of key-value pairs corresponding to the way in which the partition should be sorted to apply the window function. May be required for certain function types.

Example:
```yaml
- action: window
  type: dense_rank
  partition_by:
    - some_column
  order_by:
    - some_other_column: asc
    - yet_another_column: desc
  name: dense_ranked_column