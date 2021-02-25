# ETL Markup Toolkit
ETL Markup Toolkit (EMT) is spark-native tool for doing ETL in a sustainable, reproducible, and low-code manner. The tool achieves by providing an abstraction of a spark workflow using configuration. Unlike traditional ETL tools, the configuration is done using `yaml`, and so is completely human-readable, compatible with source control, and easy to learn.

Another advantage of the tool over traditional ETL tools, the tool translates configuration directly into `spark`/`pyspark` commands without the use of any UDFs or custom serialization, which can hurt performance, and natively integrates with the `DataFrame` API. Finally, the tool and configuration is designed to be highly sub-scriptable.

# How to Use
## Requirements
1. Python 3.7 or greater
2. Spark 2.4.4 or greater
3. `pyyaml` 5.3 or greater
## Installation
Right now, EMT is not published on pypi, so the fastest way to install is to clone the repo and do a local install in a clean virtualenv. You can achieve this like so (some commands may differ depending on how your environment is configured)

```bash
git clone https://github.com/leozqin/etl-markup-toolkit.git
python3 -m venv emt_env
source emt_env/bin/activate
cd etl-markup-toolkit
make install
```

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

For some examples of how this works, [see errata](docs/errata.md#examples-of-variable-injection)

For some suggestions of how variable injection can be used to improve the quality of ETL processes, [see errata](docs/errata.md#use-cases-for-references)

# Logging
ETL Processes have a `get_report` method that compiles a simple report for an ETL Process in the form of a Python dictionary, where the key is the workflow shortname and the value is the corresponding report for the workflow.

Because this report is a Python object, the report is trivially serialized to whatever format is required. This is left to the user.

Example:
```python
from json import dumps

report = process.get_report()
print(dumps(report))
```

For some ideas on how to use logging to improve data quality, [see errata](docs/errata.md#logging)

# Contributions
I welcome contributions - please do so by forking this repository and then sending a pull request.

If you'd like to contribute but don't know where to start, I have compiled a [wishlist in the errata](docs/errata.md#contribution-wishlist)

# Errata
[Click here to go to the errata](docs/errata.md)