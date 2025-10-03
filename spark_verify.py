# spark_verify.py
from pathlib import Path
from pyspark.sql import SparkSession

# 1) Ruta ABSOLUTA al parquet particionado (tomamos la carpeta local del repo)
root = Path(__file__).resolve().parent
p_rel = root / "outputs" / "salida_particionado"
p_abs = p_rel.resolve()            # p.ej. C:\Users\...\Modulo5Compresion\outputs\salida_particionado
p_posix = p_abs.as_posix()         # usa / para Hadoop (mejor en Windows)

print("\n=== Path detectado ===")
print("Relativo:", p_rel)
print("Absoluto:", p_abs)
print("POSIX   :", p_posix)

# 2) SparkSession con ajustes para Windows (evita NativeIO)
spark = (
    SparkSession.builder
    .config("spark.hadoop.io.native.lib.available", "false")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    .getOrCreate()
)
sc = spark.sparkContext
print("\n=== Contexto Spark ===")
print("Master:", sc.master)
print("Cores :", sc.defaultParallelism)

# 3) Intentar leer el parquet
try:
    df = spark.read.parquet(p_posix)
    print("\n=== Schema ===")
    df.printSchema()
    df.show(5, truncate=False)

    print("\n=== EXPLAIN groupBy('mes').count() ===")
    df.groupBy("mes").count().explain(True)

    print("\nOK: lectura y explain realizados. Abrí http://localhost:4040 para ver Jobs/Stages/Tasks.")
except Exception as e:
    print("\n*** ERROR leyendo Parquet ***")
    print(type(e).__name__, "->", e)
    print("\nSugerencias:")
    print("  1) Pausá OneDrive unos minutos (si está sincronizando esa carpeta).")
    print("  2) Probá mover el dataset a un path simple sin OneDrive (C:/data/salida_particionado) y cambiá p_posix.")
    print("  3) Volvé a correr este script.")
