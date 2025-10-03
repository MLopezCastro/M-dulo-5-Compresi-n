# Módulo 5 – Compresión y particionado
Genera (o lee) un dataset ~100 MB, particiona por `fecha` y `region`, y comprime a ZIP.

## Cómo correr
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python generar_particiones.py
