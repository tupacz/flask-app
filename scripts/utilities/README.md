# 🔧 Scripts de Utilidades

Scripts para configuración, mantenimiento y administración del sistema.

## 📝 Archivos

### Scripts de Configuración de Bot

#### `setup_bot_correct.py` ⭐ (Recomendado)
**Propósito**: Configuración correcta del bot de Telegram con Mini App
- Versión actualizada y corregida
- Configura el menú del bot con WebApp
- Utiliza las APIs más recientes

**Uso**:
```powershell
python scripts/utilities/setup_bot_correct.py
```

#### `setup_bot.py`
**Propósito**: Versión anterior del setup del bot
- Mantenido para referencia
- Puede tener problemas de compatibilidad

### Scripts de Bot

#### `telegram_bot_correct.py` ⭐ (Recomendado)
**Propósito**: Implementación correcta del bot de Telegram
- Bot completamente funcional
- Maneja comandos y WebApp
- Versión estable y actualizada

**Uso**:
```powershell
python scripts/utilities/telegram_bot_correct.py
```

#### `telegram_bot.py`
**Propósito**: Versión anterior del bot
- Mantenido para referencia
- Puede tener problemas de compatibilidad

### Scripts de Configuración

#### `update_ngrok_url.py`
**Propósito**: Actualizar la URL de ngrok en el archivo .env
- Interfaz interactiva para actualizar URLs
- Valida formato de URL de ngrok
- Actualiza archivo .env automáticamente

**Uso**:
```powershell
python scripts/utilities/update_ngrok_url.py
```

#### `show_data_locations.py`
**Propósito**: Mostrar ubicaciones y estadísticas de datos
- Muestra archivos de datos importantes
- Estadísticas de votos y libros
- Información de configuración
- Útil para debugging y administración

**Uso**:
```powershell
python scripts/utilities/show_data_locations.py
```

## 🔄 Archivos Duplicados

Algunos archivos tienen versiones "correct" que son las versiones mejoradas:
- `setup_bot_correct.py` vs `setup_bot.py`
- `telegram_bot_correct.py` vs `telegram_bot.py`

**Recomendación**: Usar siempre las versiones "correct" que tienen las correcciones más recientes.
