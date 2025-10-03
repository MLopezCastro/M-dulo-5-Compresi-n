from pyspark.sql import SparkSession
from pathlib import Path

root = Path(__file__).resolve().parent
spark = SparkSession.builder.appName("make-partition").getOrCreate()

# Fuente: si existe outputs/salida.parquet lo uso; si no, pruebo con outputs/csv/ventas_100mb.csv
src_parquet = root / "outputs" / "salida.parquet"
src_csv = root / "outputs" / "csv" / "ventas_100mb.csv"

if src_parquet.exists():
    df = spark.read.parquet(str(src_parquet))
elif src_csv.exists():
    df = (spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(src_csv)))
else:
    raise SystemExit("No encontré ni outputs/salida.parquet ni outputs/csv/ventas_100mb.csv")

# Elegir columna de partición automáticamente (1ª columna si hay)
part_cols = [df.columns[0]] if df.columns else []

dest = root / "outputs" / "salida_particionado"
if part_cols:
    (df.write
        .mode("overwrite")
        .partitionBy(*part_cols)
        .parquet(str(dest)))
    print(f"OK - salida_particionado creada por columna: {part_cols[0]}")
else:
    df.write.mode("overwrite").parquet(str(dest))
    print("OK - salida_particionado creada (sin columnas para particionar)")

spark.stop()
