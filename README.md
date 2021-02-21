# ETL Markup Toolkit
ETL Markup Toolkit (EMT) is spark-native tool for doing ETL in a sustainable, reproducible, and low-code manner. The tool achieves by providing an abstraction of a spark workflow using configuration. Unlike traditional ETL tools, the configuration is done using `yaml`, and so is completely human-readable, compatible with source control, and easy to learn.

Another advantage of the tool over traditional ETL tools, the tool translates configuration directly into `spark`/`pyspark` commands without the use of any UDFs, which can hurt performance. Finally, the tool and configuration is designed to be highly sub-scriptable.

# How to Use
## Requirements
1. Python 3.7 or greater
2. Spark 2.4.4 or greater
3. `pyyaml` 5.3 or greater
## Installation
TBD!!

:warning: If your spark environment is configured with an isolated python environment (eg, Amazon EMR), do not run the default installation, which will overwrite the `spark-submit` executable. It is preferred to execute from source.

## Quickstart
```bash
spark-submit quickstart.py <PATH_TO_CONFIG_FILE> <PATH_TO_PARAMS_FILE>
```

## Programatically
At its core, the ETL Markup Toolkit describes an ETL Process. Appropriately, the container object for an ETL Process is an `ETLProcess`. To instantiate a process, pass it a relative or absolute path to a configuration file and a params file. The params file can be an empty document if no params are needed.

After instantiating the object, call the `execute` method and execution of ETL Process will start.
```python
from etl_markup_toolkit.etl_process import ETLProcess

if __name__ == "__main__":

    cfg_path = "PATH_TO_CONFIG_FILE"
    params_path = "PATH_TO_PARAMS_FILE"

    process = ETLProcess(cfg_path=cfg_path, params_path=params_path)
    process.execute()
```

# Global Configuration Options
A number of features can be controlled by changing the `globals.yml` file within `etl_markup_toolkit`. To learn more about these features, click [here](docs/global_configs.md)

# Configuration Files: Workflows
A EMT configuration file is `yaml` document that describes a series of Workflows. Upon execution of the ETLProcess, workflows are executed in the order in which they are defined within the configuration file.

Each workflow, in addition to the workflow itself, has a shortname, a proper name, and a description. Shortnames are used to refer to the workflow from within other workflows when necessary.

To define a new workflow:

```yaml
---
- shortname: my_workflow
  name: My New Workflow
  desc: A workflow that does things when I tell it to
  workflow:
    - action: nothing
      comment: Look ma, a workflow!
```
# Configuration Files: Actions
Within the `workflow` section of a workflow, the user should define actions. Actions have a name and accept arguments that tell it more about what to do.

## List of Actions
To learn more about the actions that are supported, click [here](docs/actions.md)

## Subscripting/Variable Injection
There are two methods by which an external reference can be made: by directly referencing a parameter in the params file, or by referencing a parameter, which in turn references a location in the filesystem.

To reference a param, set a key called `$param` within the top-level arguments to the action, where the value corresponds to a key in the params file.

The params file should be structured as a set of keys, each of which contains arguments to the action that are inserted directly into the config at the location of the `$param` key.

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
# Errata
[Click here to go to the errata](docs/errata.md)