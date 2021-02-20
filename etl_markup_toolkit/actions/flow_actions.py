"""module for control flow actions"""

from .step import Step

class Select(Step):

    name = "Select fields"
    desc = "Select only certain fields"
    def do(self, workflow, etl_process):

        workflow.df = workflow.df.select(*self.columns)
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "columns": self.columns
        }

        self._make_log(workflow, log_stub)

class Drop(Step):

    name = "Drop fields"
    desc = "Drop certain fields"
    def do(self, workflow, etl_process):
        
        workflow.df = workflow.df.drop(*self.columns)
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "columns": self.columns
        }

        self._make_log(workflow, log_stub)

class Rename(Step):

    name = "Rename fields"
    desc = "Rename certain fields from one name to another"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import col

        copy = self.action_details.pop("copy", False)

        for old, new in self.columns.items():
            if copy:
                workflow.df = workflow.df \
                    .withColumn(new, col(old))
            else:
                workflow.df = workflow.df \
                    .withColumnRenamed(old, new)
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "columns": self.columns
        }

        self._make_log(workflow, log_stub)

class Join(Step):

    name = "Join"
    desc = "Join the workflow to another as the left one"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import broadcast, col
        from functools import reduce
        from operator import iand
        
        self.how = self.action_details.pop("how")
        self.right = self.action_details.pop("right")
        self.broadcast_right = self.action_details.pop("broadcast_right", False)

        if self.right in etl_process.unprocessed_workflows:
            etl_process._process_and_move_workflow(self.right)
        
        right_wf = etl_process.workflows[self.right]

        if self.broadcast_right:
            right_wf.df = broadcast(right_wf.df)
        
        conds = [getattr(workflow.df,k) == getattr(right_wf.df,v) for k,v in self.columns.items()]
        join_conds = reduce(iand, conds)

        workflow.df = workflow.df.join(right_wf.df, how=self.how, on=join_conds)
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "columns": self.columns,
            "how": self.how,
            "right": self.right,
            "broadcast_right": self.broadcast_right
        }

        self._make_log(workflow, log_stub)

class Filter(Step):

    name = "Filter"
    desc = "Filter the rows in the workflow and optionally send them to another workflow"
    def do(self, workflow, etl_process):
        
        from pyspark.sql.functions import col
        
        self.type = self.action_details.pop("type", "out")
        self.field = self.action_details.pop("field")
        self.send_to = self.action_details.pop("send_to", None)
        self.cache_first = self.action_details.pop("cache_first", False)

        filter_map = {
            "out": ~col(self.field),
            "in": col(self.field)
        }
        
        filter_exp = filter_map[self.type]

        if self.cache_first:
            workflow.df = workflow.df.cache()

        if self.send_to:
            etl_process._init_workflow(self.send_to)
            new_workflow = etl_process.workflows[self.send_to]

            new_workflow.df = workflow.df.filter(~filter_exp)
            new_workflow.execute(etl_process)
        
        workflow.df = workflow.df.filter(filter_exp)

    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "field": self.field,
            "type": self.type,
            "send_to": self.send_to,
            "cache_first": self.cache_first
        }

        self._make_log(workflow, log_stub)
        
class Nothing(Step):

    name = "Do Nothing"
    desc = "Does nothing"

    def do(self, workflow, etl_process):
        pass
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc
        }

        self._make_log(workflow, log_stub)