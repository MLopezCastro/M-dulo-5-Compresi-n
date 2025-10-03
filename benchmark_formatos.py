import time
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"

CSV_PLAIN = OUT / "csv" / "ventas_100mb.csv"
CSV_GZIP  = OUT / "csv" / "ventas_100mb.csv.gz"
PARQUET   = OUT / "parquet" / "ventas_100mb.parquet"
PARQ_PART = OUT / "parquet_partitioned"

def size_mb(path: Path) -> float:
    if path.is_file():
        return path.stat().st_size / 1024 / 1024
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / 1024 / 1024

def timed_read(desc, func):
    t0 = time.time()
    df = func()
    t1 = time.time()
    return df, t1 - t0

print("📊 Benchmark formatos\n")

# 1) Tamaños
print("=== Tamaño en disco ===")
for name, path in [
    ("CSV plano", CSV_PLAIN),
    ("CSV gzip", CSV_GZIP),
    ("Parquet", PARQUET),
    ("Parquet particionado", PARQ_PART),
]:
    print(f"{name:22} : {size_mb(path):.2f} MB")
print()

# 2) Tiempo de lectura total (lee todo)
print("=== Tiempo de lectura total ===")
for name, func in [
    ("CSV plano", lambda: pd.read_csv(CSV_PLAIN)),
    ("CSV gzip", lambda: pd.read_csv(CSV_GZIP, compression="gzip")),
    ("Parquet", lambda: pd.read_parquet(PARQUET, engine="pyarrow")),
    ("Parquet particionado", lambda: pd.read_parquet(PARQ_PART, engine="pyarrow")),
]:
    _, secs = timed_read(name, func)
    print(f"{name:22} : {secs:.2f} s")
print()

# 3) Tiempo de lectura con filtro por mes (ejemplo: 2023-07)
MES = "2023-07"
print(f"=== Tiempo de lectura con filtro (mes={MES}) ===")
readers = [
    ("CSV plano", lambda: pd.read_csv(CSV_PLAIN)),
    ("CSV gzip", lambda: pd.read_csv(CSV_GZIP, compression="gzip")),
    ("Parquet", lambda: pd.read_parquet(PARQUET, engine="pyarrow")),
    # En particionado, leo sólo la carpeta del mes:
    ("Parquet particionado", lambda: pd.read_parquet(PARQ_PART / f"mes={MES}", engine="pyarrow")),
]
for name, func in readers:
    df, secs = timed_read(name, func)
    if "mes" in df.columns:
        df = df[df["mes"] == MES]
    print(f"{name:22} : {secs:.2f} s, filas={len(df):,}")
