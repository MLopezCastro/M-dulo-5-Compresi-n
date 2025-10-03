from pathlib import Path
import csv
import random
from datetime import datetime, timedelta

# === Config ===
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

TARGET_MB = 100              # tamaño objetivo
OUT = DATA / "ventas_100mb.csv"

# Rango de fechas
start = datetime(2023, 1, 1)
end = datetime(2023, 12, 31)
days = (end - start).days + 1

regiones = ["Norte", "Sur", "Este", "Oeste"]

def random_fecha():
    return (start + timedelta(days=random.randint(0, days - 1))).strftime("%Y-%m-%d")

def main():
    # Escribir en streaming hasta alcanzar el tamaño
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["fecha", "región", "id", "monto", "cliente"])

        rows_per_chunk = 100_000
        written = 0
        next_id = 1

        while True:
            for _ in range(rows_per_chunk):
                writer.writerow([
                    random_fecha(),
                    random.choice(regiones),
                    next_id,
                    random.randint(100, 5000),           # monto
                    random.randint(1, 100_000)          # cliente
                ])
                next_id += 1

            f.flush()
            size_mb = OUT.stat().st_size / 1024 / 1024
            if size_mb >= TARGET_MB:
                break
            written += rows_per_chunk

    print(f"✅ CSV listo: {OUT} ({OUT.stat().st_size/1024/1024:.2f} MB)")

if __name__ == "__main__":
    main()
