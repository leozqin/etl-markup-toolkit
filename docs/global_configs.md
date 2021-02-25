# Global Configurations

Global configurations are stored in `etl_markup_toolkit/globals.yml` and control certain functionality that applies across all ETL Processes.

## Diagnostic Mode
A number of global configurations have to do with diagnostic mode. Diagnostic mode can be activated both globally and for an individual step. To learn how to activate diagnostic mode for an individual step, [click here](actions.md#universal-arguments)

The following global configurations affect the behavior of diagnostic mode:

1. `diagnostic_mode`: if `true` then diagnostic mode will be run on every action. This can significantly affect performance, so only turn it on if you really need to know what is happening step by step. If this is `false` or not present in the global config, you can still turn on diagnostic mode for individual steps.
2. `diagnostic_mode_show_count`: if `true` then diagnostic mode will include logging of record counts at each step. This may affect performance.
3. `diagnostic_mode_show_columns`: if `true` then diagnostic mode will include logging of the columns observed after applying the action to the workflow. There is no performance penalty for activating this option, although it will make logs more verbose.
4. `diagnostic_mode_show_column_diff`: if `true` then diagnostic mode will include logging of the difference in columns added and removed after applying the action to the workflow. There is no performance penalty for activating this option, although it will make logs more verbose.
5. `diagnostic_mode_show_preview`: if `true` then diagnostic mode will print a preview of the rows in the workflow after applying the action. This may affect performance.
6. `diagnostic_mode_show_preview_rows_count`: this is an integer value that controls how many rows are shown in the preview. The default value is `20`, which will be used when this global config is not set. This config has no effect if `diagnostic_mode_show_preview` is not `true`

## Spark Behavior
A number of global configurations control the default spark behavior.

1. `cache_workflow_default_storage_level`: this controls the storage level that is used when no storage level argument is passed for the `cache` action. The storage level can be any level that is supported for pyspark