@echo off
echo 🧪 Ejecutando tests del sistema...
echo.

echo 🔍 1. Testeando configuración...
python scripts/testing/test_setup.py

echo.
echo 🌐 2. Testeando navegación...
python scripts/testing/test_navigation.py

echo.
echo 🗳️ 3. Testeando sistema de votación...
python scripts/testing/test_voting_system.py

echo.
echo ✅ Tests completados!
pause
