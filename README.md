# ETL Markup Toolkit
ETL Markup Toolkit (EMT) is spark-native tool for doing ETL transformations (the "T" in ETL) in a sustainable, reproducible, and low-code manner. The tool achieves by providing an abstraction of a spark workflow using configuration. Unlike traditional ETL tools, the configuration is done using `yaml`, and so is completely human-readable, compatible with source control, and easy to learn.

Another advantage of the tool over traditional ETL tools, the tool translates configuration directly into `spark`/`pyspark` commands without the use of any UDFs or custom serialization, which can hurt performance, and natively integrates with the `DataFrame` API. Finally, the tool and configuration is designed to be highly sub-scriptable.

To learn a little more about the philosophy behind EMT and use cases where it can excel, [please check out my blog.](https://www.leozqin.me/introducing-etl-markup-toolkit-emt/)

# Terminology and Taxonomy

The following is a glossary of terminology that is used within EMT. Hopefully, this section can serve as a reference for the rest of the documentation.

1. ETL Process - an ETL Process is the container for all activities that are orchestrated by EMT. An ETL Process is described by a configuration file and (optionally) a param file.
2. Configuration - a configuration describes the activities that the ETL Process should conduct. A configuration is composed of one or more workflows.
3. Params - a supplement to the configuration that contains additional information. Individual actions within a workflow can be modified by the params file. 
4. Workflow - a container for a view of data that is being processed by the ETL Process. A workflow is composed of one or more actions. Each workflow corresponds to a pyspark DataFrame and it is modified mutably by the actions contained within it.
5. Action - an individual transformation that is applied to a Workflow by the ETL Process. Actions are referenced by their name and accepts arguments, which vary depending on the action that is being used. Actions are applied to the workflow in the order that they are defined within the workflow. There are over 30 actions supported by EMT.

To use an object-oriented programming metaphor:
1. You can think of the Configuration as the class that contains the business logic for the transformation. 
2. The ETL Process executes an instance of the Configuration.
3. The params are instance variables which can vary across different instances of the same Configuration.
4. Workflows within a Configuration are methods of a class.
5. Actions are function calls within a method.

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
At its core, the ETL Markup Toolkit describes an ETL Process. Appropriately, the container object for an ETL Process is an `ETLProcess`. To instantiate a process, pass it a relative or absolute path to a configuration file and a params file. The params file is an optional argument and does not need to be passed if no params are needed.

After instantiating the object, call the `execute` method and execution of ETL Process will start.
```python
from etl_markup_toolkit.etl_process import ETLProcess

if __name__ == "__main__":

    cfg_path = "PATH_TO_CONFIG_FILE"
    params_path = "PATH_TO_PARAMS_FILE"

    process = ETLProcess(cfg_path=cfg_path, params_path=params_path)
    process.execute()
```

# Configurations
## Global
A number of features can be controlled by changing the `globals.yml` file within `etl_markup_toolkit`. To learn more about these features, click [here](docs/global_configs.md)

## Workflows
A EMT configuration file is `yaml` document that describes a series of Workflows. Upon execution of the ETLProcess, workflows are executed in the order in which they are defined within the configuration file.

Each workflow, in addition to the workflow itself, has a shortname, a proper name, and a description. Shortnames are used to refer to the workflow from within other workflows when necessary. Workflows are in turn comprised of actions, which describe transformations that should be applied to the data.

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


## List of Actions
To learn more about the actions that are supported, click [here](docs/actions.md)

# Variable Injection / Using References
There are two methods by which an external reference can be made: by directly referencing a parameter in the params file, or by referencing a parameter, which in turn references a location in the filesystem.

## How to define references
To reference a param, set a key called `$param` within the top-level arguments to the action, where the value corresponds to a key in the params file. The params file should be structured as a set of keys, each of which contains arguments to the action that are inserted directly into the config at the location of the `$param` key.

To make a reference by location, do the same as above (creating a key called `$param`), but then set as the value of the key in turn a key called `$ref`, which references as its value the path to another `yml` file, which will be substituted in the place of that reference. The path can be absolute, or relative. If a relative path is used, it should be relative to the path of the params file.

For some examples of how this works, [see errata](docs/errata.md#examples-of-variable-injection)

For some suggestions of how variable injection can be used to improve the quality of ETL processes, [see errata](docs/errata.md#use-cases-for-references)

## Use cases for references
There are two kinds of references - references by key and references by location. Some use cases for both:

References by key:
- Changing the location from which data is read (for example, if a vendor gives you data on a monthly basis)
- Changing the location where the data is written (for example, to write data to different locations between production and dev environments)
- Changing fields that are written to the filesystem (for example, to write only ceratin fields and drop all others)

References by location:
- Storing the value mapping for standardizing a field  (for example, from vendor-provided values to standardized values)
- Storing the schema required for reading a file (for example, to resude)

It is encouraged to try generating parameter files programmatically! This might help you keep track of how business logic is applied during transformations. YAML is trivially serialized.

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
