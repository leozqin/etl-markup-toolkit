# Errata
Here are a few other considerations that have no better place to put them.

[Click here to return to the README](../README.md)

## Contribution Wishlist
I encourage contributions and am happy to accept PRs. Here are some things that would be valuable contributions (if I don't get to them first):

In no particular order:
1. A unit test suite, especially one with minimal dependency on spark itself (also, I am not that familiar with test automation)
2. A separate project to wrap a GUI around EMT. A lot of the benefit of legacy enterprise ETL Tools is their GUI, a fairly lightweight wrapper around a process to generate YAML files would suffice.
3. Improvements to argument naming consistency - I notice that sometimes arguments are fall into a structure (eg, `type`) where as other times they take a more human readable approach (eg, `else`)
4. Support for complex types other than arrays - I believe that 95% of ETL processes can be satisfied without using complex types, but if anyone can come up with a sane API for describing them, I will entertain that.
5. A way to avoid clobbering isolated python environments (a la Amazon EMR) on package install. In the past I have looked for things like the cluster name in `/mnt/var/lib/info/job-flow.json` to determine if Spark is running on EMR, but I wonder if there is a way to do this in a programmatic, non-EMR specific way.
6. A way to programmatically submit applications to the aforementioned environment from a non-Spark application context. This seems possible, but I haven't figured it out yet.

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

## Logging
In my experience, one of the hardest things about ETL is identifying the root cause of data quality issues. It never ceases to amaze how difficult it can be to answer the question simply of "what data was processed, and where did it come from?"

To that end, EMT is designed to emit precise and parseable logging, with additional diagnostic options to increase verbosity, albeit sometimes with a penalty to performance. Indeed, diagnostic mode, while useful during the development process, can also be used as a feature for logging.

In my head, a sensible architecture for logging would look something like this:
1. Define global configurations for your production environment. To minimize performance penalty, using `columns` and `column_diff` option are free, and using the `row_count` option may be a justifiable expense.
2. Enable diagnostic mode on critical actions, such as reading and writing.
3. Emit the log in `json` format and transmit to an ELK-style analytics cluster or ingest the log lines into a relational-style database (a good candidate is one with json-type support - even rudimentary support would be ok, given that the complexity of the logging is not high).