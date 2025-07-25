# 🛠️ Scripts de Desarrollo

Scripts para facilitar el desarrollo y verificación del entorno.

## 📝 Archivos

### `dev_run.py`
**Propósito**: Servidor de desarrollo con configuración automática
- Configura variables de entorno predeterminadas
- Inicia el servidor Flask en modo desarrollo
- Útil para desarrollo local sin configurar manualmente las variables

**Uso**:
```powershell
python scripts/development/dev_run.py
```

### `check_setup.py`
**Propósito**: Verificar la configuración del bot de Telegram
- Verifica que `TELEGRAM_BOT_TOKEN` esté configurado
- Verifica que `WEB_APP_URL` esté configurado
- Valida que el token del bot sea válido

**Uso**:
```powershell
python scripts/development/check_setup.py
```

### `check_telegram_version.py`
**Propósito**: Verificar la versión de python-telegram-bot
- Muestra la versión instalada
- Verifica disponibilidad de WebApp
- Verifica compatibilidad con características modernas

**Uso**:
```powershell
python scripts/development/check_telegram_version.py
```

### `explore_telegram.py`
**Propósito**: Explorar características de la librería telegram
- Explora módulos disponibles
- Busca características relacionadas con WebApp
- Útil para debugging y desarrollo

**Uso**:
```powershell
python scripts/development/explore_telegram.py
```
