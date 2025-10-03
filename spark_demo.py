from pyspark.sql import SparkSession, functions as F
from pathlib import Path

# === SparkSession ===
spark = SparkSession.builder \
    .appName("MiPrimerJob-IAE") \
    .master("local[*]") \
    .getOrCreate()

root = Path(__file__).resolve().parent
csv_in = root / "data" / "ventas_100mb.csv"      # tu CSV real
out_parquet = root / "outputs" / "salida.parquet" # 3.7 (parquet "plano")
out_part = root / "outputs" / "salida_particionado"  # 3.7 particionado

# === 3.6 Leer un CSV y transformarlo ===
# OJO: tu columna se llama 'región' (con tilde). La renombro a 'region' para evitar problemas.
df = (spark.read
      .option("header", True)
      .option("inferSchema", True)
      .csv(str(csv_in)))

df = df.withColumnRenamed("región", "region")

# Ver columnas y primeras filas
print("📄 Esquema:")
df.printSchema()
print("👀 Primeras filas:")
df.show(5, truncate=False)

# Filtro y selección
df_filtered = df.filter(F.col("monto") > 100).select("cliente", "monto")

# Agregación (promedio de monto por región)
df_grouped = df.groupBy("region").agg(F.avg("monto").alias("avg_monto"))

print("📊 Agregación por región:")
df_grouped.show()

# === 3.8 Protip: visualizar el plan de ejecución ===
print("🧠 Plan de df_filtered:")
df_filtered.explain()

# === 3.7 Guardar en Parquet ===
# Parquet "plano" (archivo/directorio único)
df.write.mode("overwrite").parquet(str(out_parquet))

# Parquet particionado por región
df.write.mode("overwrite").partitionBy("region").parquet(str(out_part))

print(f"✅ Parquet escrito en: {out_parquet}")
print(f"✅ Parquet particionado en: {out_part}")

spark.stop()
