# Sistema de Votación de Libros - Fl└── votes.json          # Datos de votación
```

## ⚡ Scripts de Conveniencia

Para simplificar el trabajo diario, se han creado scripts de conveniencia:

### `setup.bat` - Configuración Rápida
```powershell
setup.bat
```
- ✅ Configura la URL de ngrok
- ✅ Configura el bot de Telegram
- ✅ Todo en un solo comando

### `dev.bat` - Desarrollo
```powershell
dev.bat
```
- ✅ Verifica la configuración
- ✅ Inicia el servidor de desarrollo
- ✅ Variables de entorno pre-configuradas

### `test.bat` - Testing Completo
```powershell
test.bat
```
- ✅ Ejecuta todos los tests
- ✅ Verifica configuración, navegación y sistema de votación
- ✅ Reporte completo de estado

## 🚀 Inicio RápidoWeb App

Esta aplicación Flask permite votar por libros usando un sistema de voto por ranking (Condorcet) con una interfaz web intuitiva y navegación completa.

## 🌟 Características Principales

### 📊 Sistema de Navegación Completo
- **Pantalla Principal (🗳️ Votar)**: Interfaz para ordenar y votar por libros
- **Pantalla de Ganador (🏆 Ganador)**: Muestra resultados usando el método Condorcet
- **Pantalla de Votos (📊 Ver Votos)**: Vista protegida por contraseña para administrar votos
- **Gestión de Libros (📚 Gestionar Libros)**: Agregar, editar y eliminar libros

### 🔐 Seguridad
- Acceso protegido a la pantalla de votos con contraseña (1234)
- Validación de datos en frontend y backend
- Prevención de votos duplicados

### � Interfaces Múltiples
- **Interfaz Web**: Navegación completa con barra de navegación fija
- **Telegram Mini App**: Interfaz optimizada para Telegram
- **Responsive Design**: Funciona en dispositivos móviles y desktop

## � Estructura del Proyecto

```
flask-app/
├── app/                    # Aplicación principal Flask
├── scripts/               # Scripts de utilidad organizados
│   ├── development/       # Scripts de desarrollo
│   ├── testing/          # Scripts de testing
│   ├── utilities/        # Scripts de configuración y utilidades
│   └── demo/            # Scripts de demostración
├── docs/                 # Documentación técnica
├── run.py               # Punto de entrada principal
├── config.py            # Configuración de la aplicación
├── requirements.txt     # Dependencias Python
└── votes.json          # Datos de votación
```

## �🚀 Inicio Rápido

### Requisitos Previos
- Python 3.10+
- Cuenta de Telegram (para la funcionalidad de Mini App)
- [Cuenta de ngrok](https://ngrok.com) (opcional, para desarrollo local)

### Paso 1: Crear un Bot de Telegram

1. Envía un mensaje a [@BotFather](https://t.me/botfather) en Telegram
2. Usa el comando `/newbot` y sigue las instrucciones
3. Guarda tu token del bot (se ve como `1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Paso 2: Instalar Dependencias

```powershell
# Clonar o descargar el repositorio
cd flask-app

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 3: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Obtén esto de @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Esto se actualizará con la URL de ngrok
WEB_APP_URL=https://your-ngrok-url.ngrok.io/telegram

# Cualquier cadena aleatoria segura
SECRET_KEY=your-super-secret-key-here
```

### Paso 4: Ejecutar la Aplicación

```powershell
# Ejecutar la aplicación Flask
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🧭 Navegación Web

### Pantallas Disponibles

#### 🗳️ Pantalla Principal - Votar
- **URL**: `http://localhost:5000/`
- **Función**: Interfaz principal para ordenar y votar por libros
- **Características**:
  - Lista de libros arrastrables para ordenar por preferencia
  - Campo para ingresar nombre del votante
  - Confirmación antes de enviar el voto
  - Validación de datos en tiempo real

#### 🏆 Pantalla de Ganador
- **URL**: `http://localhost:5000/winner`
- **Función**: Muestra los resultados usando el método de votación Condorcet
- **Características**:
  - Estadísticas detalladas de votación (total, Telegram, Web)
  - Tabla de enfrentamientos directos entre libros
  - Explicación completa del resultado
  - Ganador determinado por el método Condorcet

#### 📊 Pantalla de Votos (Protegida)
- **URL**: `http://localhost:5000/votes`
- **Función**: Vista administrativa para gestionar votos
- **Seguridad**: Requiere contraseña `1234`
- **Características**:
  - Resumen completo de todos los votos
  - Detalles de cada voto (timestamp, usuario, ranking, fuente)
  - Exportación a JSON
  - Capacidad de editar datos de votación
  - Botones para actualizar y exportar datos

#### 📚 Gestión de Libros
- **URL**: `http://localhost:5000/books-manager`
- **Función**: Administrar la lista de libros disponibles para votación
- **Características**:
  - Agregar nuevos libros con título, autor y descripción
  - Editar libros existentes
  - Eliminar libros (con confirmación)
  - Validación de campos obligatorios
  - Retroalimentación visual al guardar

### Navegación por Botones

La aplicación incluye una **barra de navegación fija** en la parte superior con botones para acceder a cada pantalla:

- **🗳️ Votar**: Ir a la pantalla principal de votación
- **🏆 Ganador**: Ver resultados de la votación
- **📊 Ver Votos**: Acceder a la vista de administración (solicita contraseña)
- **📚 Gestionar Libros**: Administrar la lista de libros

### Funciones Especiales

#### Protección por Contraseña
- La pantalla de votos está protegida con contraseña (`1234`)
- Se solicita la contraseña tanto al hacer clic en el botón como al acceder directamente a la URL
- Redirección automática a la página principal si la contraseña es incorrecta

#### Diseño Responsive
- La navegación se adapta automáticamente a dispositivos móviles
- Los botones se reorganizan en columna en pantallas pequeñas
- Espaciado ajustado para touch interfaces

## 🔧 Configuración Avanzada con ngrok (Para Telegram Mini App)

### Paso 1: Instalar y Configurar ngrok

1. **Descargar ngrok**:
   - Ve a [ngrok.com](https://ngrok.com)
   - Regístrate para una cuenta gratuita
   - Descarga ngrok para Windows
   - Extrae `ngrok.exe` a la carpeta de tu proyecto

2. **Autenticar ngrok**:
   ```powershell
   .\ngrok.exe authtoken YOUR_NGROK_AUTHTOKEN
   ```

### Paso 2: Configurar Variables de Entorno para Telegram

Actualiza tu archivo `.env`:

```env
# Obtén esto de @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Esto se actualizará con la URL de ngrok
WEB_APP_URL=https://your-ngrok-url.ngrok.io/telegram

# Cualquier cadena aleatoria segura
SECRET_KEY=your-super-secret-key-here
```

### Paso 3: Ejecutar la Aplicación con Telegram (Requiere 4 terminales)

#### Terminal 1: Iniciar ngrok
```powershell
# Exponer la aplicación Flask local (puerto 5000)
.\ngrok.exe http 5000
```
Copia la URL HTTPS (como `https://abc123.ngrok.io`)

#### Terminal 2: Actualizar URL de ngrok
```powershell
# Actualizar el archivo .env con tu URL de ngrok
python scripts/utilities/update_ngrok_url.py
```
Pega tu URL de ngrok cuando se solicite (automáticamente agregará `/telegram`)

#### Terminal 3: Configurar Bot de Telegram
```powershell
# Configurar la Web App en tu bot de Telegram
python scripts/utilities/setup_bot_correct.py
```

#### Terminal 4: Iniciar Aplicación Flask
```powershell
# Iniciar la aplicación Flask
python run.py
```

#### Terminal 5: Iniciar Bot de Telegram (Opcional)
```powershell
# Iniciar el bot para manejar comandos /start
python scripts/utilities/telegram_bot_correct.py
```

### Paso 4: Probar tu Mini App

1. Abrir Telegram
2. Buscar tu bot (ej. `@YourBotName`)
3. Enviar `/start`
4. Hacer clic en el botón "📚 Votar Libros"
5. ¡La Mini App debería abrirse dentro de Telegram!

## 🔧 Flujo de Trabajo de Desarrollo

### Rutina de Desarrollo Diaria

1. **Iniciar ngrok** (Terminal 1):
   ```powershell
   .\ngrok.exe http 5000
   ```

2. **Actualizar URL si cambió la URL de ngrok** (Terminal 2):
   ```powershell
   python scripts/utilities/update_ngrok_url.py
   python scripts/utilities/setup_bot_correct.py
   ```

3. **Iniciar Flask** (Terminal 3):
   ```powershell
   python run.py
   ```

4. **Probar en Telegram**: Enviar `/start` a tu bot

### Configuración Automática (Alternativa)

Crear un script `start_dev.py`:

```python
from dotenv import load_dotenv
load_dotenv()

import subprocess
import sys
import time

def start_development():
    print("🚀 Starting development environment...")
    
    # Start Flask app
    print("📱 Starting Flask app...")
    flask_process = subprocess.Popen([sys.executable, 'run.py'])
    
    # Start Telegram bot
    print("🤖 Starting Telegram bot...")
    bot_process = subprocess.Popen([sys.executable, 'telegram_bot_correct.py'])
    
    print("✅ Services started!")
    print("📝 Manual steps needed:")
    print("1. Run: ngrok http 5000")
    print("2. Run: python scripts/utilities/update_ngrok_url.py")
    print("3. Run: python scripts/utilities/setup_bot_correct.py")
    print("4. Test your bot in Telegram!")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        flask_process.terminate()
        bot_process.terminate()

if __name__ == '__main__':
    start_development()
```

Then just run: `python scripts/development/dev_run.py` (o crear un script start_dev.py consolidado)

## 🔍 Troubleshooting

### Common Issues

1. **"Invalid Telegram data"**
   - ✅ Check your bot token is correct in `.env`
   - ✅ Ensure ngrok URL ends with `/telegram`

2. **Mini App doesn't load**
   - ✅ Verify ngrok is running: `.\ngrok.exe http 5000`
   - ✅ Check Flask is running: visit `http://localhost:5000/telegram`
   - ✅ Ensure URL is HTTPS (ngrok provides this)

3. **Bot doesn't respond to /start**
   - ✅ Run `python scripts/utilities/telegram_bot_correct.py`
   - ✅ Check bot token is valid

4. **"This site can't be reached"**
   - ✅ Restart ngrok: `.\ngrok.exe http 5000`
   - ✅ Update URL: `python scripts/utilities/update_ngrok_url.py`
   - ✅ Reconfigure bot: `python scripts/utilities/setup_bot_correct.py`

### Verification Scripts

Test your setup:

```powershell
# Check if all packages are installed
python scripts/development/check_telegram_version.py

# Test web app accessibility (si existe)
python scripts/testing/test_webapp.py

# Verify votes are being saved
python scripts/utilities/show_data_locations.py
```

## 📂 Data Storage

Votes are stored in a **JSON file** with the following structure:

### Vote Storage Location
- **File**: `votes.json` in your project root
- **Format**: JSON with detailed vote information
- **Backup**: Automatic UUIDs prevent data corruption

### Vote Structure
Each vote contains:
```json
{
  "vote_id": "unique-uuid-here",
  "timestamp": "2025-07-24T01:04:35.112921",
  "ranking": ["Book1", "Book2", "Book3"],
  "vote_source": "telegram" | "web",
  "telegram_user_id": "123456789",
  "telegram_user_data": {
    "first_name": "Name",
    "last_name": "Surname", 
    "username": "username"
  },
  "display_name": "Display Name"
}
```

### Managing Vote Data

**View Statistics:**
```powershell
python scripts/utilities/show_data_locations.py
```

**Test System:**
```powershell
python scripts/testing/test_voting_system.py
```

**API Endpoints:**
- `GET /votes-json` - Export votes as JSON
- `GET /vote-stats` - Get voting statistics
- `GET /winner` - See Condorcet results with stats

### Features
- ✅ **Duplicate Prevention**: Users can only vote once
- ✅ **Source Tracking**: Telegram vs Web votes
- ✅ **User Identification**: Telegram ID + username for web
- ✅ **Timestamp Tracking**: ISO format timestamps
- ✅ **Data Integrity**: UUID-based vote IDs
- ✅ **Export Ready**: JSON format for analysis

## 🌐 Production Deployment

For production, replace ngrok with:

- **Render**: Connect your GitHub repo
- **Railway**: Easy deployment with Git integration
- **Heroku**: Classic PaaS option
- **Vercel**: For serverless deployment
- **Your own server**: With SSL certificate

### Production Setup

1. Deploy your app to a hosting service
2. Update `WEB_APP_URL` with your production domain
3. Set environment variables on your hosting platform
4. Run `python scripts/utilities/setup_bot_correct.py` with production URL
5. Your bot will work with the production URL

## Features

- **Telegram Authentication**: Users are automatically authenticated via Telegram
- **Drag & Drop Voting**: Users can rank books by dragging them
- **Responsive Design**: Works great on mobile devices
- **Haptic Feedback**: Uses Telegram's haptic feedback for better UX
- **Theme Integration**: Adapts to user's Telegram theme
- **Duplicate Prevention**: Users can only vote once (tracked by Telegram ID)

## File Structure

- `app/telegram_auth.py` - Telegram Web App authentication
- `app/templates/telegram_index.html` - Mini App interface
- `app/static/telegram_styles.css` - Mini App styles
- `telegram_bot_correct.py` - Bot setup script
- `setup_bot_correct.py` - Bot configuration script
- `config.py` - Configuration settings
- `votes.json` - Vote storage (created automatically)

## API Endpoints

- `GET /telegram` - Mini App main page
- `POST /telegram-auth` - Validate Telegram user data
- `POST /submit` - Submit vote (handles both web and Telegram)
- `GET /` - Regular web interface
- `GET /winner` - Show voting results

## Security

- All Telegram data is validated using HMAC-SHA256
- Bot token is used to verify request authenticity
- Users are identified by Telegram ID to prevent duplicate votes
- HTTPS is required for Mini Apps

## Support

For issues with:
- Telegram Bot API: Check [Telegram Bot API docs](https://core.telegram.org/bots/api)
- Mini Apps: Check [Telegram Mini Apps docs](https://core.telegram.org/bots/webapps)
- Flask: Check [Flask documentation](https://flask.palletsprojects.com/)
- ngrok: Check [ngrok documentation](https://ngrok.com/docs)
- **Heroku**: Classic PaaS option
- **Vercel**: For serverless deployment
- **Your own server**: With SSL certificate

### 5. Update Web App URL

After deployment, update the `WEB_APP_URL` in your bot configuration:

1. Message [@BotFather](https://t.me/botfather)
2. Use `/mybots` command
3. Select your bot
4. Choose "Bot Settings" → "Menu Button"
5. Enter your Mini App URL: `https://your-domain.com/telegram`

### 6. Test Your Bot

1. Run the Flask app: `python run.py`
2. Run the bot script: `python scripts/utilities/telegram_bot.py`
3. Message your bot on Telegram
4. Use `/start` or the menu button to access the Mini App

## Features

- **Telegram Authentication**: Users are automatically authenticated via Telegram
- **Drag & Drop Voting**: Users can rank books by dragging them
- **Responsive Design**: Works great on mobile devices
- **Haptic Feedback**: Uses Telegram's haptic feedback for better UX
- **Theme Integration**: Adapts to user's Telegram theme
- **Duplicate Prevention**: Users can only vote once (tracked by Telegram ID)

## Development

### Local Testing

For local development, you can use tools like `ngrok` to expose your local server:

```bash
# Install ngrok
# Run your Flask app
python run.py

# In another terminal, expose your local server
ngrok http 5000
```

Then use the ngrok HTTPS URL as your `WEB_APP_URL`.

### File Structure

- `app/telegram_auth.py` - Telegram Web App authentication
- `app/templates/telegram_index.html` - Mini App interface
- `app/static/telegram_styles.css` - Mini App styles
- `telegram_bot.py` - Bot setup script
- `config.py` - Configuration settings

### API Endpoints

- `GET /telegram` - Mini App main page
- `POST /telegram-auth` - Validate Telegram user data
- `POST /submit` - Submit vote (handles both web and Telegram)

## Deployment Examples

### Render (Recommended)

1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Set environment variables in Render dashboard
5. Deploy

### Railway

1. Create account at [railway.app](https://railway.app)
2. Connect GitHub repository
3. Set environment variables
4. Deploy automatically

## Security

- All Telegram data is validated using HMAC-SHA256
- Bot token is used to verify request authenticity
- Users are identified by Telegram ID to prevent duplicate votes
- HTTPS is required for Mini Apps

## Troubleshooting

### Common Issues

1. **"Invalid Telegram data"**: Check your bot token is correct
2. **Mini App doesn't load**: Ensure URL is HTTPS
3. **Authentication fails**: Verify environment variables are set
4. **Bot doesn't respond**: Check bot token and run `telegram_bot.py`

### Debug Mode

Set `DEBUG=True` in `config.py` for detailed error messages.

## Support

For issues with:
- Telegram Bot API: Check [Telegram Bot API docs](https://core.telegram.org/bots/api)
- Mini Apps: Check [Telegram Mini Apps docs](https://core.telegram.org/bots/webapps)
- Flask: Check [Flask documentation](https://flask.palletsprojects.com/)
