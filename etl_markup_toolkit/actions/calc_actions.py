"""module for actions that calculate a field using other fields"""

import operator
from .step import Step

class Comparison(Step):

    name = "Comparison"
    desc = "Compare one or more fields and return a boolean outcome"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import when, lit, col
        from operator import iand, ior,  lt, le, eq, ne, gt, ge
        from functools import reduce

        self.bool_col = self.action_details.pop("name")
        self.else_val = self.action_details.pop("else", False)
        self.type = self.action_details.pop("type", "and")

        self.comparisons = self.action_details.pop("comparisons")

        operator_map = {
            "=" : eq,
            "!=" : ne,
            ">" : gt,
            ">=" : ge,
            "<": lt,
            "<=": le
        }

        cond_map = {
            "or": ior,
            "and": iand
        }

        cond_func = cond_map[self.type]
        conds = list()

        for comp in self.comparisons:
            op = operator_map[comp["type"]]
            cols = comp.get("columns")

            if cols:
                left_term = cols[0]
                right_term = cols[1]
                conds.append(op(col(left_term), right_term))

            else:
                left_term = comp["column"]
                right_term = comp["value"]
                conds.append(op(col(left_term), right_term))

        conds_list = reduce(cond_func, conds)

        workflow.df = workflow.df \
            .withColumn(self.bool_col, when(conds_list,lit(True)).otherwise(self.else_val))
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "type": self.type,
            "bool_col": self.bool_col,
            "else": self.else_val,
            "comparisons": self.comparisons
        }

        self._make_log(workflow, log_stub)

class Aggregation(Step):

    name = "Aggregation"
    desc = "Group by one or more fields and take aggregations"
    def do(self, workflow, etl_process):
        
        from pyspark.sql.functions import (count, countDistinct, collect_list
            , collect_set, avg, sum, first, min, max, lit)
        
        AGG_MAP = {
            "count": lambda x: count(lit(1)),
            "count_distinct": countDistinct,
            "collect_list": collect_list,
            "collect_set": collect_set,
            "average": avg,
            "sum": sum,
            "first": first,
            "min": min,
            "max": max
        }

        self.aggs = self.action_details.pop("aggregations")

        agg_exps = []

        for agg in self.aggs:
            aggfunc = AGG_MAP[agg["type"]]
            new_col = agg["name"]
            target = agg.get("target")
            agg_exps.append(aggfunc(target).alias(new_col))
        
        workflow.df = workflow.df \
            .groupby(*self.columns) \
            .agg(*agg_exps)
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "columns": self.columns,
            "aggregations": self.aggs
        }

        self._make_log(workflow, log_stub)

class Checksum(Step):

    name = "Add a checksum"
    desc = "Calculate the checksum value for a field"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import md5, crc32, xxhash64, sha1, sha2, hash, col, to_str

        func_map = {
            "md5": md5,
            "crc32": crc32,
            "xxhash64": xxhash64,
            "hash": hash,
            "sha1": sha1,
            "sha224": lambda x: sha2(x, 224),
            "sha256": lambda x: sha2(x, 256),
            "sha384": lambda x: sha2(x, 384),
            "sha512": lambda x: sha2(x, 512)
        }

        self.type = self.action_details.pop("type")
        hashfunc = func_map[self.type]

        for column in self.columns:
            workflow.df = workflow.df \
                .withColumn(column, hashfunc(col(column).astype("string")))
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "columns": self.columns,
            "type": self.type
        }

        self._make_log(workflow, log_stub)

class Scalar(Step):

    name = "Scalar Function"
    desc = "Apply a scalar function to one or more columns"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import (abs, acos, asin, atan, ceil, col, cos, cosh, 
            degrees, exp, expm1, factorial, floor, length, log10, log1p, log2, radians,
            sin, sinh, sqrt, tan, tanh)

        FUNC_MAP = {
            "abs": abs,
            "acos": acos,
            "asin": asin,
            "atan": atan,
            "ceiling": ceil,
            "cos": cos,
            "cosh": cosh,
            "degrees": degrees,
            "exp": exp,
            "exp_minus_one": expm1,
            "factorial": factorial,
            "floor": floor,
            "length": length,
            "log10": log10,
            "log_plus_one": log1p,
            "log2": log2,
            "radians": radians,
            "sin": sin,
            "sinh": sinh,
            "sqrt": sqrt,
            "tan": tan,
            "tanh": tanh
        }

        self.type = self.action_details.pop("type")

        col_func = FUNC_MAP[self.type]

        for column in self.columns:
            workflow.df = workflow.df \
                .withColumn(column, col_func(col(column)))
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "type": self.type,
            "columns": self.columns
        }

        self._make_log(workflow, log_stub)

class Math(Step):

    name = "Mathematical Operation"
    desc = "Do a mathematical operation on one or more operands"
    def do(self, workflow, etl_process):

        from operator import add, sub, mul, truediv, pow, mod
        from functools import reduce
        from pyspark.sql.functions import col

        OPERATOR_MAP = {
            "add": add,
            "subtract": sub,
            "multiply": mul,
            "divide": truediv,
            "exponent": pow,
            "modulo": mod
        }

        self.math_col = self.action_details.pop("name")
        self.operator = self.action_details.pop("operator")

        math_op = reduce(OPERATOR_MAP[self.operator], [col(i) for i in self.columns])

        workflow.df = workflow.df \
            .withColumn(self.math_col, math_op)
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "math_col": self.math_col,
            "operator": self.operator,
            "columns": self.columns
        }

        self._make_log(workflow, log_stub)

class Window(Step):

    name = "Window Function"
    desc = "Calculate a window function over a specified window"
    def do(self, workflow, etl_process):

        from pyspark.sql.functions import sum, row_number, rank, dense_rank, cume_dist, percent_rank, col
        from pyspark.sql import Window

        self.window_column = self.action_details.pop("name")
        self.type = self.action_details.pop("type")
        self.partition_by = self.action_details.pop("partition_by", list())
        self.order_by = self.action_details.pop("order_by", list())
        self.target = self.action_details.pop("target", None)

        type_map = {
            "sum": lambda x: sum(x),
            "row_num": lambda x: row_number(),
            "rank": lambda x: rank(),
            "dense_rank": lambda x: dense_rank(),
            "cume_dist": lambda x: cume_dist(),
            "percent_rank": lambda x: percent_rank()
        }



        order_map = {
            "asc": lambda x: col(x).asc(),
            "desc": lambda x: col(x).desc()
        }

        order_expr = list()
        for order in self.order_by:
            for k,v in order.items():
                expr = order_map[v](k)
                order_expr.append(expr)

        w = Window().partitionBy(*self.partition_by).orderBy(*order_expr)
        w_func = type_map[self.type](self.target).over(w)

        workflow.df = workflow.df \
            .withColumn(self.window_column, w_func)

    def log(self, workflow):
        
        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "window_column": self.window_column,
            "type": self.type,
            "partition_by": self.partition_by,
            "order_by": self.order_by
        }

        self._make_log(workflow, log_stub)