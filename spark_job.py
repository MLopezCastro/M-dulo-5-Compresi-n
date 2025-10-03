from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, substring, col, lit
from time import perf_counter

spark = (SparkSession.builder
    .config("spark.hadoop.io.native.lib.available", "false")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    .getOrCreate())

print("Spark UI -> http://localhost:4040 (dejá este proceso abierto)")
df = spark.read.parquet("C:/data/salida_particionado")

# 1) Shuffle sobre TU data
print("\n=== EXPLAIN groupBy('mes').count() ===")
df.groupBy("mes").count().explain(True)

# 2) Medir sin/CON repartition
def timeit(msg, fn):
    t0 = perf_counter(); r = fn(); t1 = perf_counter()
    print(f"{msg}: {t1 - t0:.3f}s")
    return r

timeit("groupBy('mes').count() (sin repartition)",
       lambda: df.groupBy("mes").count().count())

df_rep = df.repartition(24, "mes")
timeit("groupBy('mes').count() (CON repartition('mes'))",
       lambda: df_rep.groupBy("mes").count().count())

# 3) Join sin/CON broadcast (dim de meses 1..12)
df2 = df.withColumn("mm", substring(col("mes"), 6, 2).cast("int"))
months = spark.createDataFrame([(i,) for i in range(1,13)], ["mm"]).withColumn("label", lit("m"))

print("\n=== EXPLAIN join SIN broadcast ===")
df2.join(months, "mm").explain(True)
print("\n=== EXPLAIN join CON broadcast ===")
df2.join(broadcast(months), "mm").explain(True)

timeit("join SIN broadcast → count", lambda: df2.join(months, "mm").count())
timeit("join CON broadcast → count", lambda: df2.join(broadcast(months), "mm").count())

input("\nDejé Spark vivo para que veas la UI. Abrí http://localhost:4040 y cuando termines, presioná Enter para salir...")
