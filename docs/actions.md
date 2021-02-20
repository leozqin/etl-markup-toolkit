# Actions
Actions are the most atomic unit of configuration within EMT. Each action corresponds to a native spark operation that is carried out upon execution of the ETL Process. All actions take arguments in the form of key-value pairs. Some arguments require/support complex types such as arrays and arrays of objects.

# Universal arguments
All actions support the following arguments:

`comment`: A way of passing un-executed data from the configuration into the ETL Process. Typically, this can be a string with more details about why the action works in a certain way, but `yaml`-compliant complex types are also supported.

`diagnostic_mode`: This is a boolean value that instructs EMT to emit additional logging during the processing of this action. The values are that emitted during diagnotic mode can be controlled by the global configs. By default, this is `false`

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

The supported flow actions are (click through to read more):
1. [Select - Select only certain fields](flow_actions.md#select)
2. [Drop - Drop certain fields](flow_actions.md#drop)
3. [Rename - Rename certain fields from one name to another](flow_actions.md#rename)
4. [Join - Join the current workflow to another one](flow_actions.md#join)