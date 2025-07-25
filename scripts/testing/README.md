# 🧪 Scripts de Testing

Scripts para probar y validar el funcionamiento del sistema.

## 📝 Archivos

### `test_navigation.py`
**Propósito**: Prueba todas las rutas de navegación de la aplicación
- Verifica que todas las rutas respondan correctamente
- Prueba códigos de estado HTTP
- Valida la navegación completa del sistema

**Uso**:
```powershell
# Asegúrate de que el servidor esté corriendo en http://localhost:5000
python scripts/testing/test_navigation.py
```

### `test_setup.py`
**Propósito**: Verificación completa de la configuración del sistema
- Prueba importación de todas las librerías requeridas
- Verifica variables de entorno
- Valida configuración de Telegram
- Prueba conectividad

**Uso**:
```powershell
python scripts/testing/test_setup.py
```

### `test_voting_system.py`
**Propósito**: Prueba el sistema de votaciones
- Crea datos de prueba
- Prueba el algoritmo de votación Condorcet
- Valida almacenamiento de votos
- Verifica prevención de votos duplicados

**Uso**:
```powershell
python scripts/testing/test_voting_system.py
```

## ⚠️ Nota Importante

Estos scripts de testing están diseñados para:
- Ejecutarse en un entorno de desarrollo
- Validar que todo funciona correctamente antes de producción
- Debugging de problemas específicos

**Antes de ejecutar**:
1. Asegúrate de tener todas las dependencias instaladas
2. Configura las variables de entorno necesarias
3. Para `test_navigation.py`, el servidor debe estar corriendo
