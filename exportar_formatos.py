from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CSV_IN = DATA / "ventas_100mb.csv"

OUT = ROOT / "outputs"
OUT_CSV = OUT / "csv"
OUT_PARQUET = OUT / "parquet"
OUT_PARQUET_PART = OUT / "parquet_partitioned"

for d in (OUT, OUT_CSV, OUT_PARQUET, OUT_PARQUET_PART):
    d.mkdir(parents=True, exist_ok=True)

def size_mb(p: Path) -> str:
    return f"{p.stat().st_size/1024/1024:.2f} MB"

# 0) Verificaciones previas
if not CSV_IN.exists():
    raise FileNotFoundError(f"No encuentro {CSV_IN}. Creálo con make_100mb_csv.py o poné tu CSV ahí.")

print(f"📥 CSV detectado: {CSV_IN} ({size_mb(CSV_IN)})")

# 1) Cargar
df = pd.read_csv(CSV_IN, low_memory=False, dtype={"región": "string"})
print(f"✅ Cargado: {len(df):,} filas, columnas = {list(df.columns)}")

# 2) Preparar fecha/mes
df["fecha"] = pd.to_datetime(df["fecha"], errors="raise")
df["mes"] = df["fecha"].dt.to_period("M").astype(str)

# 3) CSV plano
csv_plain = OUT_CSV / "ventas_100mb.csv"
df.to_csv(csv_plain, index=False)
print(f"💾 CSV plano: {csv_plain} ({size_mb(csv_plain)})")

# 4) CSV gzip
csv_gzip = OUT_CSV / "ventas_100mb.csv.gz"
df.to_csv(csv_gzip, index=False, compression="gzip")
print(f"💾 CSV gzip : {csv_gzip} ({size_mb(csv_gzip)})")

# 5) Parquet sin particionar
parquet_file = OUT_PARQUET / "ventas_100mb.parquet"
df.to_parquet(parquet_file, index=False, engine="pyarrow", compression="snappy")
print(f"💾 Parquet  : {parquet_file} ({size_mb(parquet_file)})")

# 6) Parquet particionado por mes
df.to_parquet(
    OUT_PARQUET_PART,
    index=False,
    engine="pyarrow",
    compression="snappy",
    partition_cols=["mes"]
)
parts = list(OUT_PARQUET_PART.rglob("*.parquet"))
print(f"💾 Parquet particionado en: {OUT_PARQUET_PART} (archivos: {len(parts)})")

print("🎉 Listo.")
