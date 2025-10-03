
---

# Parte 1 — Dataset sintético (100 MB), exportación y comparación de formatos

Este módulo genera un CSV de ~100 MB con columnas `fecha`, `región`, `id`, `monto`, `cliente`; lo exporta a varios formatos y compara tamaños/tiempos de lectura.

## 📂 Estructura del proyecto

```
Modulo 5 - Compresión/
├─ .venv/
├─ data/
│  └─ ventas_100mb.csv                  # generado en Parte 1
├─ outputs/
│  ├─ csv/
│  │  ├─ ventas_100mb.csv
│  │  └─ ventas_100mb.csv.gz
│  ├─ parquet/
│  │  └─ ventas_100mb.parquet
│  └─ parquet_partitioned/
│     └─ mes=YYYY-MM/part-*.parquet
├─ make_100mb_csv.py
├─ exportar_formatos.py
├─ benchmark_formatos.py
├─ requirements.txt
└─ .gitignore
```

> **Nota GitHub:** `outputs/` y `data/*.csv` están ignorados en `.gitignore` para evitar subir archivos grandes.

## ▶️ Requisitos e instalación

```powershell
# En la carpeta del proyecto
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`requirements.txt`:

```
pandas
numpy
pyarrow
```

## 1) Generar dataset (~100 MB)

Crea un CSV de prueba en `data/ventas_100mb.csv`:

```powershell
python make_100mb_csv.py
```

* Por defecto cubre fechas de 2023 y regiones: Norte/Sur/Este/Oeste.
* Podés ajustar el tamaño editando `TARGET_MB` en el script.

## 2) Exportar a múltiples formatos

Genera:

* CSV sin comprimir
* CSV gzip
* Parquet (único archivo)
* Parquet **particionado por mes** (`mes=YYYY-MM`)

```powershell
python exportar_formatos.py
```

## 3) Benchmark (tamaño y tiempos de lectura)

Mide:

* **Tamaño en disco** (MB)
* **Tiempo de lectura total**
* **Tiempo de lectura filtrado por un mes** (ej. `2023-07`)

```powershell
python benchmark_formatos.py
```

### 👉 Interpretación esperada

* **CSV**: ocupa más y es más lento en lectura total; gz reduce tamaño pero no siempre el tiempo.
* **Parquet**: suele ser más chico y rápido.
* **Parquet particionado**: lectura **con filtro** (p. ej. un mes) debe ser **mucho más rápida** porque lee solo la partición necesaria.

## 🧪 Resultados (completá con tus números)

Reemplazá `—` con los valores que te imprime `benchmark_formatos.py`.

| Formato              | Tamaño (MB) | Tiempo lectura total (s) | Tiempo lectura filtro mes (s) | Filas mes |
| -------------------- | ----------- | ------------------------ | ----------------------------- | --------- |
| CSV plano            | —           | —                        | —                             | —         |
| CSV gzip             | —           | —                        | —                             | —         |
| Parquet              | —           | —                        | —                             | —         |
| Parquet particionado | —           | —                        | —                             | —         |

> Tip: si usás OneDrive, **pausá el sync** durante las escrituras grandes para evitar bloqueos.

## 🔧 Variantes útiles

* **Más años**: en `make_100mb_csv.py`, cambiá `start/end` (ej. 2022–2024).
* **Partición más granular**: en `exportar_formatos.py`, podés usar
  `partition_cols=["anio","mes_num","región"]` tras crear esas columnas.

---

