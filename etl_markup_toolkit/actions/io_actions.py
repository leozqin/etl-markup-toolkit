"""module for IO actions"""


from .step import Step

class SparkSessionCreator:

    def create(cls):
        from pyspark.sql import SparkSession

        cls.spark = SparkSession.builder.appName("ETL Process").getOrCreate()

class Read(Step, SparkSessionCreator):
    
    name = "Read data"
    desc = "Read data from a filesystem"
    def do(self, workflow, etl_process):
        
        from pyspark.sql.types import StructType, StructField, StringType
        from json import load

        self.create()
        self.location = self.action_details.pop("location")
        self.format = self.action_details.pop("format")
        self.schema = self.action_details.pop("schema", None)

        # self.schema should be a relative filepath to a spark-compliant schema
        if self.schema:
            with open(self.schema) as fp:
                schema = StructType.fromJson(load(fp))
        
        # if there is no spark-compliant schema, attempt to use the columns and set all
        # fields to string
        elif self.columns:
            schema = StructType([StructField(i, StringType()) for i in self.columns])
        
        # if there are no columns, then allow the schema to be inferred using the inference
        # rules native to the format
        else:
            schema = None
        
        schema_types = {
            "csv": self.spark.read.csv,
            "json": self.spark.read.json
        }

        schemaless_types = {
            "parquet": self.spark.read.parquet,
            "orc": self.spark.read.orc,
        }

        
        if self.format in schema_types:
            reader = schema_types[self.format]
            workflow.df = reader(self.location, schema=schema, **self.action_details)
        else:
            reader = schemaless_types[self.format]
            workflow.df = reader(self.location, **self.action_details)
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "format": self.format,
            "location": self.location,
            "additional_arguments": self.action_details
        }

        if self.columns:
            log_stub["columns"] = self.columns
        
        if self.schema:
            log_stub["schema"] = self.schema

        self._make_log(workflow, log_stub)

class Write(Step):

    name = "Write data"
    desc = "Write data using to a filesystem"
    def do(self, workflow, etl_process):

        self.location = self.action_details.pop("location")
        self.format = self.action_details.pop("format")

        FORMAT_MAP = {
            "csv": workflow.df.write.csv,
            "parquet": workflow.df.write.parquet,
            "json": workflow.df.write.json,
            "orc": workflow.df.write.orc
        }

        writer = FORMAT_MAP.get(self.format)

        writer(self.location, **self.action_details)
    
    def log(self, workflow):

        log_stub = {
            "name": self.name,
            "desc": self.desc,
            "location": self.location,
            "format": self.format,
            "additional_arguments": self.action_details
        }

        self._make_log(workflow, log_stub)
