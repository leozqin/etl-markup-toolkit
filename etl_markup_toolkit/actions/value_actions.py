"""module for actions that modify values"""

from typing import cast
from .step import Step

class ReplaceValues(Step):

    name = "Replace Values"
    desc = "Replace values in one or more columns with another value"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import regexp_replace, col

        self.old_value = self.action_details.get("replace")
        self.new_value = self.action_details.get("with")

        workflow.df = workflow.df.replace(self.old_value, self.new_value, subset = self.columns)
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "columns": self.columns,
            "old_value": self.old_value,
            "new_value": self.new_value
        }

        self._make_log(workflow, log_stub)

class Convert(Step):

    name = "Convert Values"
    desc = "Convert values from one type to another"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import to_str, to_date, to_timestamp, col
        from pyspark.sql.types import IntegerType, FloatType, DoubleType

        FUNC_TYPE_MAP = {
            "date": to_date,
            "timestamp": to_timestamp
        }

        CAST_TYPE_MAP = {
            "int": IntegerType(),
            "double": DoubleType(),
            "float": FloatType(),
        }

        # types having no arguments required for the conversion call
        NAKED_TYPE_MAP = {
            "str": to_str
        }

        self.cast_to = self.action_details.pop("type")
        f_type = FUNC_TYPE_MAP.get(self.cast_to)
        c_type = CAST_TYPE_MAP.get(self.cast_to)
        n_type = NAKED_TYPE_MAP.get(self.cast_to)

        if f_type:
            format = self.action_details.pop("format", None)
            for column in self.columns:
                workflow.df = workflow.df.withColumn(column, f_type(column, format=format))
        
        elif c_type:
            for column in self.columns:
                workflow.df = workflow.df.withColumn(column, col(column).cast(c_type))
        
        elif n_type:
            for column in self.columns:
                workflow.df = workflow.df.withColumn(n_type(column))
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "columns": self.columns,
            "type": self.cast_to
        }

        self._make_log(workflow, log_stub)

class StandardizeValues(Step):

    name = "Standardize Values"
    desc = "Standardize values from one mapped value to another"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import col, create_map, lit, coalesce, when
        from itertools import chain

        self.mapping = self.action_details.pop("mapping")
        mapping_expr = create_map([lit(x) for x in chain(*self.mapping.items())])
        
        else_value = self.action_details.pop("else")

        for column in self.columns:
            mapfunc = mapping_expr[col(column)]
            keep_nulls = when(col(column).isNull(), lit(None))
            mapper = coalesce(mapfunc, lit(else_value))
            workflow.df = workflow.df \
                .withColumn(column, keep_nulls.otherwise(mapper))
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "columns": self.columns,
            "mapping": self.mapping
        }

        self._make_log(workflow, log_stub)

class Const(Step):

    name = "Add Constant"
    desc = "Add a column with constant value"
    def do(self, workflow, etl_process):
        
        from pyspark.sql.functions import lit
        
        self.const_col = self.action_details.pop("name")
        self.value = self.action_details.pop("value")

        workflow.df = workflow.df \
            .withColumn(self.const_col, lit(self.value))
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "const_col": self.const_col,
            "value": self.value
        }

        self._make_log(workflow, log_stub)

class Concat(Step):

    name = "Concatenate Columns"
    desc = "Concatenate two or more columns, with or without a separator"
    def do(self, workflow, etl_process):
        
        from pyspark.sql.functions import concat, concat_ws
        
        self.concat_col = self.action_details.pop("name")
        self.sep = self.action_details.pop("sep", None)

        if self.sep:
            workflow.df = workflow.df \
                .withColumn(self.concat_col, concat_ws(self.sep, *self.columns))
        else:
            workflow.df = workflow.df \
                .withColumn(self.concat_col, concat(*self.columns))
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "concat_col": self.concat_col,
            "sep": self.sep,
            "columns": self.columns
        }

        self._make_log(workflow, log_stub)

class StringFormat(Step):

    name = "String Format"
    desc = "Apply formatting to a string column"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import upper, lower, initcap, trim, rtrim, ltrim, col, reverse
        
        FORMAT_MAP = {
            "upper": upper,
            "lower": lower,
            "proper": initcap,
            "trim": trim,
            "left_trim": ltrim,
            "right_trim": rtrim,
            "reverse": reverse
        }

        self.format = self.action_details.pop("format")

        format_op = FORMAT_MAP[self.format]

        for column in self.columns:
            workflow.df = workflow.df \
                .withColumn(column, format_op(col(column)))
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "format": self.format,
            "columns": self.columns
        }

        self._make_log(workflow, log_stub)

class StringPad(Step):

    name = "String Padding"
    desc = "Apply padding to a string column"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import lpad, rpad, col
        
        SIDE_MAP = {
            "left": lpad,
            "right": rpad
        }

        self.side = self.action_details.pop("side")
        self.pad_char = self.action_details.pop("with")
        self.length = self.action_details.pop("length")

        pad_op = SIDE_MAP[self.side]

        for column in self.columns:
            workflow.df = workflow.df \
                .withColumn(column, pad_op(col(column), self.length, self.pad_char))
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "side": self.side,
            "with": self.pad_char,
            "length": self.length,
            "columns": self.columns
        }

        self._make_log(workflow, log_stub)
