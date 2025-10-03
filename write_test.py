from pyspark.sql import SparkSession
from pathlib import Path

spark = SparkSession.builder.appName("write-test").getOrCreate()

out = Path("outputs") / "_spark_test_write"
out.parent.mkdir(parents=True, exist_ok=True)

spark.range(10).write.mode("overwrite").parquet(str(out))
print("OK - _spark_test_write creado en:", out)

spark.stop()
