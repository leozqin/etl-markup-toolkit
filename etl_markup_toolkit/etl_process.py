"""Contains entry point for using ETL Tool."""
from collections import OrderedDict
from yaml import load, FullLoader
from .workflow import Workflow
from os import path

GLOBALS_PATH = path.join(path.dirname(path.abspath(__file__)), "globals.yml")

class ETLProcess:
    """
    An ETL Process is the entry point for doing ETL. An ETL Process consists of one or
    more Workflows, each of which consists of multiple Steps. The ETL process takes one
    configuration file, and one optional file that contains additional parameters, which
    are injected into the rest of the configuration file at runtime.

    Args:
        cfg_path (str): the path to the config file
        params_path (str): optional, the path to the additional params file
    """

    def __init__(self, cfg_path: str, params_path: str = None):

        with open(cfg_path) as fp:
            self.cfg = load(fp, Loader=FullLoader)
        
        with open(GLOBALS_PATH) as fp:
            self.globals = load(fp, Loader=FullLoader)
        
        if params_path:
            with open(params_path) as fp:
                self.params = load(fp, Loader = FullLoader)
                self.params["_params_path"] = params_path
        
        self.unprocessed_workflows = OrderedDict()
        self.workflows = OrderedDict()

        self._parse()
        
    def _parse(self):
        """
        Parse the workflows that are defined in the config file and inject additional configurations
        from the params file into the config file
        """

        for w_flow in self.cfg:
            w_name = w_flow.pop("shortname")
            self.unprocessed_workflows[w_name] = Workflow(w_flow, self.params)
    
    def _process_and_move_workflow(self, wf_name):
        """
        Process a workflow and move it from the list of unprocessed workflows to the list 
        of processed ones.
        """
        
        wf = self.unprocessed_workflows.pop(wf_name)
        wf.execute(self)
        self.workflows[wf_name] = wf

    def _init_workflow(self, wf_name):
        """
        Initialize a workflow by moving it from the list of unprocessed workflows to the list
        of processed ones.
        """

        wf = self.unprocessed_workflows.pop(wf_name)
        self.workflows[wf_name] = wf
    
    def execute(self):
        """
        Executes the workflows defined in the config file after parsing. Workflows are executed
        sequentially in the order in which they are defined.
        """
        
        for wf_name,_ in self.unprocessed_workflows.copy().items():
            if wf_name in self.unprocessed_workflows:
                self._process_and_move_workflow(wf_name)
            else:
                pass
    
    def get_report(self):
        """
        Compiles the report for each processed workflow in the ETL process
        """
        report = dict()

        for wf_name, wf in self.workflows.items():
            report[wf_name] = wf.workflow_report

        return report
