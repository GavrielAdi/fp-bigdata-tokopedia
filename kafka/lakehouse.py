from pyspark.sql import SparkSession
from delta.tables import DeltaTable
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("LakehouseWriter") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.1.0") \
    .getOrCreate()

# Path to Delta Lake storage
DELTA_PATH = "./lakehouse/delta-lake"

def write_to_delta(record):
    """Write a single record to Delta Lake."""
    # Define schema
    schema = StructType([
        StructField("rating", IntegerType(), True),
        StructField("category", StringType(), True),
        StructField("product_name", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("sold", IntegerType(), True),
        StructField("shop_id", StringType(), True),
        StructField("product_url", StringType(), True),
    ])
    
    # Create a DataFrame from the record
    df = spark.createDataFrame([record], schema=schema)
    
    # Append to Delta Lake
    df.write.format("delta").mode("append").save(DELTA_PATH)
    print(f"Data written to Delta Lake: {record}")
