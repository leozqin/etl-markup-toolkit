"""module for Steps"""

from typing import Dict
from os import path
from yaml import load, FullLoader
from json import dumps

GLOBALS_PATH = path.join(path.dirname(path.abspath(__file__)), "../globals.yml")

class Step:

    def __init__(self, cfg: Dict, params: Dict) -> None:
        """
        Base class for steps. The base class handles parsing of the config into a function-specific
        step. Common conventions for defining steps should also be defined here. 
        
        Finally, the base class handles injection of params (noted in the config file as $param,
        and a key corresponding to the value in the params file) into the data structure of the Step.
        The key can also be a $ref, referring to another file relative to the path of the params
        file, which will be loaded and injected to the params file before it is itself injected
        into the step.

        Therefore, every step can have one $param, which can support an arbitrary number of keys
        and a single $ref, which can itself support an arbitrary number of keys.

        Args:
            cfg (Dict): The contents of the config Dictionary for the individual step
            params (Dict): The params file, after deserializing into a Dictionary
        """
        with open(GLOBALS_PATH) as fp:
            self.globals = load(fp, Loader=FullLoader)

        self.action = cfg.pop("action")
        self.action_details = cfg

        global_diagnostic_mode = self.globals.get("diagnostic_mode")
        step_level_diagnostic_mode = cfg.pop("diagnostic_mode", False)
        
        self.is_diagnostic_mode = global_diagnostic_mode or step_level_diagnostic_mode

        self.param = cfg.pop("$param", None)

        if self.param:
            injected_param = params.get(self.param)
            _param_path = params.get("_params_path")

            if "$ref" in injected_param:

                param_dir = path.dirname(path.abspath(_param_path))
                ref_path = injected_param['$ref']

                with open(path.join(param_dir, ref_path)) as fp:
                    ref_data = load(fp, Loader=FullLoader)
                    injected_param = {**injected_param, **ref_data}

            self.action_details = {**self.action_details, **injected_param}
        
        self.columns = self.action_details.pop("columns", None)
        self.comment = self.action_details.pop("comment", None)
    
    def _make_log(self, workflow, log_stub):

        if self.is_diagnostic_mode:

            if self.globals.get("diagnostic_mode_show_count", False):
                log_stub["row_count"] = workflow.df.count()
            
            if self.globals.get("diagnostic_mode_show_columns", False):
                log_stub["observed_columns"] = workflow.df.columns
            
            if self.globals.get("diagnostic_mode_show_column_diff", False):
                old_columns = set(getattr(workflow, "_columns", set()))
                new_columns = set(workflow.df.columns)

                columns_removed = old_columns - new_columns
                columns_added = new_columns - old_columns

                log_stub["columns_added"] = list(columns_added)
                log_stub["columns_removed"] = list(columns_removed)

            if self.globals.get("diagnostic_mode_show_preview", False):
                print("showing preview for step:")
                print(dumps(log_stub, indent=4))

                preview_rows = self.globals.get("diagnostic_mode_show_preview_rows_count", 20)
                workflow.df.show(preview_rows, False)
        
        if self.comment:
            log_stub["comment"] = self.comment

        workflow._columns = workflow.df.columns        
        workflow.workflow_report["steps"].append(log_stub)