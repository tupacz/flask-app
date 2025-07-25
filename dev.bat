@echo off
echo 🛠️ Iniciando servidor de desarrollo...
echo.

echo 📊 Verificando configuración...
python scripts/development/check_setup.py

echo.
echo 🚀 Iniciando aplicación Flask...
python scripts/development/dev_run.py
