Aquí va tu **README 2** —explicación detallada y pasos— listo para pegar como `README_PART2_SPARK.md` 

---

# Parte 2 — De compresión a **Parquet particionado con Spark**

Este módulo extiende la etapa de **compresión** (CSV → `.csv.gz`) y agrega una etapa de **ingeniería de datos con PySpark**: conversión a **Parquet** y **particionado por `mes`** para mejorar performance de lectura y analítica.

## 🎯 Objetivo

* Pasar de **un archivo comprimido** a un **dataset columnar optimizado**.
* Escribir los datos en **Parquet** (con compresión interna) y **particionar por `mes`** → lectura selectiva por partición y mejor I/O.

---

## 🧱 Estructura actual del proyecto (relevante)

```
MODULO5COMPRESION/
├─ .venv/
├─ data/
├─ outputs/
│  ├─ csv/
│  │  ├─ ventas_100mb.csv
│  │  └─ ventas_100mb.csv.gz
│  ├─ parquet/                 (parquet "no particionado", opcional)
│  ├─ salida_particionado/     (parquet particionado por mes)  ✅
│  │  ├─ mes=2023-01/
│  │  │  ├─ 9077e3bd...-0.parquet
│  │  │  └─ a10ff3ff...-0.parquet
│  │  ├─ mes=2023-02/
│  │  └─ ...
│  └─ _spark_test_write/       (carpeta de test creada por Spark, opcional)
├─ .gitignore
├─ benchmark_formatos.py
├─ exportar_formatos.py
├─ make_100mb_csv.py
├─ make_partition.py           ✅ script principal de esta parte
├─ spark_demo.py
├─ write_test.py
└─ requirements.txt
```

---

## 🧪 Qué hiciste en la **Parte 1 (Compresión)**

1. Generaste un CSV grande (`ventas_100mb.csv`).
2. Lo **comprimiste** a `ventas_100mb.csv.gz`.

   * Ventaja: ocupa menos espacio.
   * Límite: **sigue siendo fila a fila**; no es formato columnar y no está particionado.

---

## ⚙️ Qué hiciste ahora en la **Parte 2 (Spark)**

Con el script `make_partition.py`:

1. **Leíste** el CSV fuente (desde `outputs/csv/ventas_100mb.csv` o el `.gz`).
2. **(Opcional)** Normalizaste tipos / columnas (por ejemplo, asegurar que `mes` esté en formato `YYYY-MM`.

   * Si el CSV **ya trae** `mes`, Spark lo usa directo.
   * Si no, el script puede derivarlo desde una columna fecha (p. ej. `to_date` → `date_format(..., 'yyyy-MM')`).
3. **Escribiste en Parquet** con compresión interna (columnar).
4. **Particionaste por `mes`** con `partitionBy("mes")`.
5. Resultado: `outputs/salida_particionado/mes=YYYY-MM/*.parquet`.

> **Nota de naming**: tus archivos aparecen como `9077e3bd....parquet` (hash/UUID). Es normal. En algunas configuraciones Spark usa `part-*.parquet`. **No es un error**.

---

## 🧠 ¿Por qué Parquet + particiones?

* **Parquet**: formato columnar → lecturas más rápidas, compresión por columna, mejor para analytics.
* **Particiones por `mes`**: cuando filtrás por `mes`, el motor **lee solo esas carpetas** → menos I/O, más velocidad.
* **Compresión interna**: Parquet ya aplica compresión (snappy por defecto), sin perder la capacidad de consulta eficiente.

---

## ▶️ Cómo reproducir (paso a paso)

### 0) Activar entorno e instalar dependencias

```powershell
# En PowerShell
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

### 1) (Opcional) Generar el CSV de prueba

```powershell
python .\make_100mb_csv.py
```

### 2) Ejecutar el particionado con Spark

```powershell
python .\make_partition.py
```

### 3) Verificar la salida en disco

```powershell
# Ver carpetas de partición
Get-ChildItem .\outputs\salida_particionado

# Contar archivos por partición
Get-ChildItem .\outputs\salida_particionado -Recurse -File -Filter *.parquet |
  Group-Object { $_.Directory.Name } | Select-Object Name, Count
```

---

## 🔎 Validaciones rápidas

### A) Chequear versión de PySpark y Spark

> En PowerShell **no** escribas `import` directo. Usá el REPL de Python o `-c`.

**REPL:**

```powershell
python
```

Dentro de Python:

```python
import pyspark
from pyspark.sql import SparkSession
print("PySpark:", pyspark.__version__)
print("Spark  :", SparkSession.builder.getOrCreate().version)
```

Salir: `exit()`.

**One-liner:**

```powershell
python -c "import pyspark; from pyspark.sql import SparkSession; \
print('PySpark:', pyspark.__version__); \
print('Spark  :', SparkSession.builder.getOrCreate().version)"
```

### B) Leer un Parquet (Pandas)

```powershell
python -c "import pandas as pd, glob; \
paths = glob.glob(r'.\outputs\salida_particionado\mes=2023-01\*.parquet'); \
df = pd.read_parquet(paths[0]); \
print(df.head()); print('Filas en primer archivo:', len(df))"
```

### C) Leer todo con Spark y contar

*(En PowerShell usá REPL o `-c`; heredoc tipo `<<PY` es de bash.)*

```powershell
python -c "from pyspark.sql import SparkSession; \
spark = SparkSession.builder.getOrCreate(); \
df = spark.read.parquet(r'.\outputs\salida_particionado'); \
print('Total filas:', df.count()); \
df.show(5, truncate=False)"
```

---

## 📈 Rendimiento (idea)

* **CSV (.gz)**: bueno para storage, **malo para análisis** (escaneo total, sin pushdown de columnas).
* **Parquet particionado**: excelente en lectura filtrada y selección de columnas; **menos CPU y disco**.

Podés comparar con `benchmark_formatos.py` (si lo tenés implementado) midiendo tiempos de:

* Leer CSV vs Parquet.
* `count()` del total.
* Filtro por `mes`.

---

## 🧯 Troubleshooting rápido

* **“`import` no reconocido”**: estás escribiendo Python en PowerShell. Entrá al REPL (`python`) o usá `python -c "..."`
* **No aparecen `part-*.parquet`**: no pasa nada; Spark puede nombrar con UUIDs. La estructura de **carpetas `mes=YYYY-MM`** es lo importante.
* **No se crea `salida_particionado`**: revisá rutas de entrada/salida en `make_partition.py` y permisos de escritura.
* **Pandas no abre Parquet**: asegurate de tener `pyarrow` en `requirements.txt`.

---

## 🧩 Qué archivos de código usaste acá

* `make_partition.py` → **Script principal**: lee CSV/CSV.GZ, crea/ajusta `mes` si hace falta, y escribe Parquet **particionado**.
* `spark_demo.py` / `write_test.py` → utilitarios opcionales de prueba de escritura Spark.
* `requirements.txt` → incluye `pyspark`, `pandas`, `pyarrow`, etc.

---

## ✅ Resumen ejecutivo

* **Antes:** CSV → `.csv.gz` (**compresión lineal** de un único archivo).
* **Ahora:** CSV/CSV.GZ → **Parquet particionado por `mes` con Spark** (columnar + compresión interna + lectura selectiva).
* **Resultado:** dataset analítico **mucho más eficiente** para consultas y pipelines.

---


