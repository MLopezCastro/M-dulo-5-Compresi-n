¡Perfecto, Marcelo! 🚀 Te actualizo el **README – Parte 1** con tus resultados reales de tamaños y tiempos. Así queda documentado el benchmark 👇

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

### ✅ Resultados obtenidos

**Tamaño en disco:**

* CSV plano              : 124.70 MB
* CSV gzip               : 33.75 MB
* Parquet                : 29.74 MB
* Parquet particionado   : 49.94 MB

**Tiempo de lectura total:**

* CSV plano              : 1.27 s
* CSV gzip               : 1.58 s
* Parquet                : 0.40 s
* Parquet particionado   : 0.39 s

**Tiempo de lectura con filtro (mes=2023-07):**

* CSV plano              : 1.29 s, filas=254,540
* CSV gzip               : 1.60 s, filas=254,540
* Parquet                : 0.40 s, filas=254,540
* Parquet particionado   : 0.04 s, filas=254,540

### 📊 Comparación en tabla

| Formato              | Tamaño (MB) | Lectura total (s) | Lectura filtro mes (s) | Filas mes |
| -------------------- | ----------- | ----------------- | ---------------------- | --------- |
| CSV plano            | 124.70      | 1.27              | 1.29                   | 254,540   |
| CSV gzip             | 33.75       | 1.58              | 1.60                   | 254,540   |
| Parquet              | 29.74       | 0.40              | 0.40                   | 254,540   |
| Parquet particionado | 49.94       | 0.39              | **0.04**               | 254,540   |

---

## 🧪 Conclusiones rápidas

* **Parquet** es más compacto y veloz que CSV.
* **CSV gzip** reduce mucho tamaño, pero penaliza un poco la velocidad de lectura.
* **Parquet particionado** sobresale al filtrar: carga solo la carpeta del mes y es **~10× más rápido** que leer todo.

---



