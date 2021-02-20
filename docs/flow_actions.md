# Flow Actions

## Select
The `select` action selects the specified columns, dropping all other columns.

Arguments:
- `columns`: a list of the columns that should be selected

Example:
```yaml
- action: select
  columns:
    - some_column
    - some_other_column
```

## Drop
The `drop` action drops the specified columns, keeping all other columns.

Arguments:
- `columns`: a list of the columns that should be dropped

Example:
```yaml
- action: drop
  columns:
    - some_column
    - some_other_column
```

## Rename
The `rename` action renames certain fields from one name to another, optionally making a copy instead.

Arguments:
- `columns`: a list of key-value pairs, where the key is name of the column that should be renamed, and the value is the name to which it should be renamed
- `copy`: optional, default `false`: whether the columns should be copied to their new name, instead of being replaced.

Example:
```yaml
- action: rename
  copy: true
  columns:
    some_column: some_column_new_name
    some_other_column: some_other_column_new_name
```

## Join
The `join` action joins the workflow to another workflow as the left one.

Arguments:
- `right`: the `shortname` for the other workflow that should be joined to the current one. This shortname must exist within the config file for the ETL Process.
- `how`: the manner in which the workflows should be joined. Can be the keyword value of [any spark-supported join type](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html?highlight=read%20csv#pyspark.sql.DataFrame.join)
- `columns`: a set of key-value pairs, where the key is the column in the current (left) workflow and the value is the column in the other (right) workflow to which it corresponds.
- `broadcast_right`: optional, default `false`: whether the other (right) workflow should be broadcast prior to joining, which improves join performance at the cost of using more memory. This should only be `true` for relatively small workflows.

Example:
```yaml
- action: join
  how: inner
  right: other_workflow
  broadcast_right: true
  columns:
    some_field: some_field
    some_other_field: yet_another_field
```