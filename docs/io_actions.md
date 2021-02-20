# IO Actions

## Read
The `read` action is used to read data from a file system.

Arguments:
- `location`: the location from where the data should be read. Should include a compliant protocol where necessary.
- `format`: the format of the data that is being read. The current supported types are:
    - `csv`: for files that use a delimiter
    - `json`: for files that are structured as json lines
    - `parquet`: for files that use the [Parquet](https://parquet.apache.org/) file format
    - `orc` for files that use the [Optimized Row Columnar](https://orc.apache.org/) file format
- `schema`: optional: a path to a json representation of a spark dataframe schema
- `columns`: optional: a list of column names in the order that they are stored
- additional arguments are passed directly to spark

Some notes on `schema`:
- `parquet` and `orc` are self-describing formats, so an argument to `schema` is not necessary
- `schema` is supported for both `csv` and `json`
- if both `columns` and `schema` are passed for csv, the `schema` will take priority
- passing a `schema` for json is option but highly recommended, else spark will infer a schema for the json

Example:
``` yaml
- action: read
  format: csv
  sep: ","
  location: "hdfs:///path/to/my/data"
  schema: "/path/to/my/schema.json"
  columns:
    - first_column
    - second_column
```

## Write
The `write` action is used to write data to a filesystem

Arguments
- `location`: the location to which the data should be written. Should include a compliant protocol where necessary.
- `format`: the format of the data that is being written. The current supported types are:
    - `csv`: for files that use a delimiter
    - `json`: for files that are structured as json lines
    - `parquet`: for files that use the [Parquet](https://parquet.apache.org/) file format
    - `orc` for files that use the [Optimized Row Columnar](https://orc.apache.org/) file format
- additional arguments are passed directly to spark

Example:
``` yaml
- action: write
  format: orc
  location: "hdfs:///path/to/my/data"
  partitionBy:
    - third_column
    - fourth_column
  columns:
    - first_column
    - second_column
```