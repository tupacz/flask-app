# 🗑️ Archivos que Se Pueden Eliminar

Después de la reorganización, algunos archivos duplicados o obsoletos pueden eliminarse de forma segura.

## ✅ Archivos Movidos Exitosamente

Estos archivos han sido movidos a `scripts/` y YA NO están en la raíz:

### Scripts de Desarrollo
- ✅ `dev_run.py` → `scripts/development/dev_run.py`
- ✅ `check_setup.py` → `scripts/development/check_setup.py`
- ✅ `check_telegram_version.py` → `scripts/development/check_telegram_version.py`
- ✅ `explore_telegram.py` → `scripts/development/explore_telegram.py`

### Scripts de Testing
- ✅ `test_navigation.py` → `scripts/testing/test_navigation.py`
- ✅ `test_setup.py` → `scripts/testing/test_setup.py`
- ✅ `test_voting_system.py` → `scripts/testing/test_voting_system.py`

### Scripts de Utilidades
- ✅ `setup_bot.py` → `scripts/utilities/setup_bot.py`
- ✅ `setup_bot_correct.py` → `scripts/utilities/setup_bot_correct.py`
- ✅ `telegram_bot.py` → `scripts/utilities/telegram_bot.py`
- ✅ `telegram_bot_correct.py` → `scripts/utilities/telegram_bot_correct.py`
- ✅ `update_ngrok_url.py` → `scripts/utilities/update_ngrok_url.py`
- ✅ `show_data_locations.py` → `scripts/utilities/show_data_locations.py`

### Scripts de Demo
- ✅ `demo_navigation.py` → `scripts/demo/demo_navigation.py`
- ✅ `summary_implementation.py` → `scripts/demo/summary_implementation.py`

### Documentación
- ✅ `IMPLEMENTACION_COMPLETADA.md` → `docs/IMPLEMENTACION_COMPLETADA.md`

## 🔄 Archivos Duplicados - Evaluar para Eliminación

### Versiones Obsoletas (Candidatos para eliminar)
Estos archivos tienen versiones "correctas" mejoradas:

- `scripts/utilities/setup_bot.py` - **Candidato para eliminar**
  - Razón: Existe `setup_bot_correct.py` que es la versión mejorada
  - Acción recomendada: Eliminar después de verificar que setup_bot_correct.py funciona

- `scripts/utilities/telegram_bot.py` - **Candidato para eliminar**
  - Razón: Existe `telegram_bot_correct.py` que es la versión mejorada
  - Acción recomendada: Eliminar después de verificar que telegram_bot_correct.py funciona

## 🧪 Scripts de Testing - Evaluar Utilidad

Algunos scripts de testing podrían no ser necesarios para el funcionamiento diario:

- `scripts/testing/test_setup.py` - **Mantener**
  - Útil para verificar instalación completa
  
- `scripts/testing/test_navigation.py` - **Mantener**
  - Útil para verificar que todas las rutas funcionen
  
- `scripts/testing/test_voting_system.py` - **Mantener**
  - Útil para verificar el algoritmo de votación

## 🎭 Scripts de Demo - Evaluar Necesidad

- `scripts/demo/demo_navigation.py` - **Mantener**
  - Útil para demostraciones a stakeholders
  
- `scripts/demo/summary_implementation.py` - **Mantener**
  - Útil para generar reportes de funcionalidades

## 🚨 NO ELIMINAR

Estos archivos son esenciales para el funcionamiento:

### Archivos de Producción (en raíz)
- ✅ `run.py` - Punto de entrada principal
- ✅ `config.py` - Configuración
- ✅ `requirements.txt` - Dependencias
- ✅ `Procfile` - Para Heroku
- ✅ `runtime.txt` - Versión de Python
- ✅ `README.md` - Documentación
- ✅ `votes.json` - Datos de votación
- ✅ `app/` - Toda la carpeta de la aplicación

### Nuevas Carpetas y Documentación
- ✅ `scripts/` - Todo el contenido
- ✅ `docs/` - Todo el contenido

## 📋 Acciones Recomendadas

1. **Inmediato**: Verificar que los scripts movidos funcionen correctamente
2. **Después de pruebas**: Eliminar versiones obsoletas (`setup_bot.py` y `telegram_bot.py`)
3. **Opcional**: Crear aliases o scripts de conveniencia en la raíz que apunten a scripts/

## 🔧 Scripts de Conveniencia (Opcional)

Podrías crear scripts simples en la raíz que deleguen a los scripts organizados:

```powershell
# setup.ps1
python scripts/utilities/setup_bot_correct.py

# test.ps1  
python scripts/testing/test_navigation.py

# dev.ps1
python scripts/development/dev_run.py
```
