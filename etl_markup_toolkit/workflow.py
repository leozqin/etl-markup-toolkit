"""Workflows module"""
from typing import Dict
from .actions.io_actions import Read, Write
from .actions.flow_actions import Select, Drop, Rename, Join, Nothing, Filter, Union, Copy
from .actions.value_actions import ReplaceValues, StandardizeValues, Convert, Concat, Const, StringFormat, StringPad, ParseDate
from .actions.calc_actions import Comparison, Aggregation, Checksum, Math, Scalar
from os import path
from yaml import load, FullLoader

GLOBALS_PATH = path.join(path.dirname(path.abspath(__file__)), "globals.yml")

class Workflow:

    ACTION_MAP = {
        "read": Read,
        "write": Write,
        "select": Select, 
        "drop": Drop,
        "rename": Rename,
        "replace_values": ReplaceValues,
        "standardize_values": StandardizeValues,
        "convert": Convert,
        "comparison": Comparison,
        "join": Join,
        "const": Const,
        "concat": Concat,
        "math": Math,
        "str_format": StringFormat,
        "str_pad": StringPad,
        "aggregate": Aggregation,
        "checksum": Checksum,
        "scalar": Scalar,
        "do_nothing": Nothing,
        "filter": Filter,
        "parse_date": ParseDate,
        "union": Union,
        "copy_workflow": Copy
    }

    def __init__(self, cfg: Dict, params: Dict = None) -> None:
        """
        A Workflow represents an individual instance of data that can be transformed by the functions
        defined in the configuration. Additional configurations are injected from the params file

        Args:
            cfg (Dict): The configuration file, after deserializing into a Dictionary
            params (Dict): The params file, after deserializing into a Dictionary
        """
        
        with open(GLOBALS_PATH) as fp:
            self.globals = load(fp, Loader=FullLoader)

        self.name = cfg.get("name")
        self.desc = cfg.get("desc")
        self.steps = []

        steps = cfg.get("workflow")
        for step in steps:
            action_name = step["action"]
            step_obj = self.ACTION_MAP.get(action_name)(step, params)
            self.steps.append(step_obj)
        
        self.workflow_report = {
            "name": self.name,
            "desc": self.desc,
            "steps": list()
        }
    
    def execute(self, etl_process):
        """
        Executing the workflow triggers Spark to carry out the transformations that are defined in the
        parsed config file. In the process of doing the transformation, a log file is also generated and
        added to the workflow report.
        """

        for step in self.steps:
            step.do(self, etl_process)
            step.log(self)