# Errata
Here are a few other considerations that have no better place to put them.

[Click here to return to the README](../README.md)

## Use Cases for References
### Reference by Key
The primary (but by no means exclusive) use case envisioned for storing references by key is changing the input and output locations for data, so that you can use the same config file for different instances of an ETL Process.

### Reference by Location
A suggested use case for storing reference by location is to share configuration between different ETL Processes. This can be very useful when standardizing values within the same field and you want to ensure that different ETL Processes use the same standardization.

### Both
Because both references by key and location are separate files from the business logic defined in the configuration, it is supported (and encouraged) to generate these at run-time from a centralized master data management system and/or data catalog.

## Examples of Variable Injection
### Example: Replacement by Key
For example, take the following action within a workflow:
```yaml
- action: do_something
  $param: keys_to_action
```
If the params file passed during the creation of the ETL Process looks as below:
```yaml
---
keys_to_action:
  some_argument: some value
  some_other_argument:
    - argument_value_0
    - argument_value_1  
```
Then, after the param is replaced, the action will look like this:
```yaml
- action: do_something
  some_argument: some value
  some_other_argument:
    - argument_value_0
    - argument_value_1  
```
### Example: Replacement by Reference
It is also supported to make a `$param` reference the location of another `yaml` document, which will be loaded and injected as the value for the key matching the `$param`.

For example, given the following action:
```yaml
- action: do_something
  $param: keys_to_action
```
And the corresponding params file:
```yaml
---
keys_to_action:
  $ref: "/path/to/referenced/file.yaml"
```
Where the referenced file contains:
```yaml
---
some_argument: some value
  some_other_argument:
    - argument_value_0
    - argument_value_1  
```
The outcome of injection will be the same as before:
```yaml
- action: do_something
  some_argument: some value
  some_other_argument:
    - argument_value_0
    - argument_value_1  
```