@echo off
echo 🚀 Setup rápido para el sistema de votación de libros
echo.

echo 📝 1. Configurando variables de entorno...
python scripts/utilities/update_ngrok_url.py

echo.
echo 🤖 2. Configurando bot de Telegram...
python scripts/utilities/setup_bot_correct.py

echo.
echo ✅ Setup completado!
echo 📌 Próximos pasos:
echo    1. Ejecutar: python run.py
echo    2. Probar en Telegram enviando /start a tu bot
echo.
pause
