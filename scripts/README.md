# 📁 Scripts

Esta carpeta contiene scripts de utilidad organizados por categoría.

## 📂 Estructura

### 🛠️ `/development`
Scripts para desarrollo y verificación del entorno:
- `dev_run.py` - Servidor de desarrollo con variables de entorno predefinidas
- `check_setup.py` - Verifica la configuración del bot de Telegram
- `check_telegram_version.py` - Verifica la versión de python-telegram-bot
- `explore_telegram.py` - Explora las características disponibles de la librería

### 🧪 `/testing`
Scripts para testing y validación:
- `test_navigation.py` - Prueba todas las rutas de navegación
- `test_setup.py` - Verifica la configuración completa del sistema
- `test_voting_system.py` - Prueba el sistema de votaciones

### 🔧 `/utilities`
Scripts de utilidades para configuración y mantenimiento:
- `setup_bot.py` - Configuración inicial del bot de Telegram
- `setup_bot_correct.py` - Versión corregida del setup del bot
- `telegram_bot.py` - Bot de Telegram principal
- `telegram_bot_correct.py` - Versión corregida del bot
- `update_ngrok_url.py` - Actualiza la URL de ngrok en .env
- `show_data_locations.py` - Muestra ubicaciones y estadísticas de datos

### 🎭 `/demo`
Scripts de demostración:
- `demo_navigation.py` - Demostración de funcionalidades de navegación
- `summary_implementation.py` - Resumen de las características implementadas

## 🚀 Uso

Para ejecutar cualquier script, desde la raíz del proyecto:

```powershell
# Ejemplo: ejecutar script de desarrollo
python scripts/development/dev_run.py

# Ejemplo: ejecutar test de navegación
python scripts/testing/test_navigation.py

# Ejemplo: configurar bot
python scripts/utilities/setup_bot_correct.py
```
