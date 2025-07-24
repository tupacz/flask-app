# Telegram Mini App - Book Voting System

This Flask application has been converted to work as a Telegram Mini App for voting on books using ranked choice voting.

## 🚀 Quick Start with ngrok (Local Development)

### Prerequisites
- Python 3.10+
- Telegram account
- [ngrok account](https://ngrok.com) (free tier works)

### Step 1: Create a Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command and follow the instructions
3. Save your bot token (looks like `1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Step 2: Install Dependencies

```powershell
# Clone or download the repository
cd flask-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install and Setup ngrok

1. **Download ngrok**:
   - Go to [ngrok.com](https://ngrok.com)
   - Sign up for free account
   - Download ngrok for Windows
   - Extract `ngrok.exe` to your project folder

2. **Authenticate ngrok**:
   ```powershell
   .\ngrok.exe authtoken YOUR_NGROK_AUTHTOKEN
   ```

### Step 4: Configure Environment Variables

Create a `.env` file in your project root:

```env
# Get this from @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here

# This will be updated with ngrok URL
WEB_APP_URL=https://your-ngrok-url.ngrok.io/telegram

# Any secure random string
SECRET_KEY=your-super-secret-key-here
```

### Step 5: Start the Application

**You need 4 terminal windows/tabs:**

#### Terminal 1: Start ngrok
```powershell
# Expose local Flask app (port 5000)
.\ngrok.exe http 5000
```
Copy the HTTPS URL (like `https://abc123.ngrok.io`)

#### Terminal 2: Update ngrok URL
```powershell
# Update the .env file with your ngrok URL
python update_ngrok_url.py
```
Paste your ngrok URL when prompted (it will automatically add `/telegram`)

#### Terminal 3: Configure Telegram Bot
```powershell
# Configure the Web App in your Telegram bot
python setup_bot_correct.py
```

#### Terminal 4: Start Flask App
```powershell
# Start the Flask application
python run.py
```

#### Terminal 5: Start Telegram Bot (Optional)
```powershell
# Start the bot to handle /start commands
python telegram_bot_correct.py
```

### Step 6: Test Your Mini App

1. Open Telegram
2. Search for your bot (e.g., `@YourBotName`)
3. Send `/start`
4. Click the "📚 Votar Libros" button
5. The Mini App should open inside Telegram!

## 🔧 Development Workflow

### Daily Development Routine

1. **Start ngrok** (Terminal 1):
   ```powershell
   .\ngrok.exe http 5000
   ```

2. **Update URL if ngrok URL changed** (Terminal 2):
   ```powershell
   python update_ngrok_url.py
   python setup_bot_correct.py
   ```

3. **Start Flask** (Terminal 3):
   ```powershell
   python run.py
   ```

4. **Test in Telegram**: Send `/start` to your bot

### Automatic Setup (Alternative)

Create a `start_dev.py` script:

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
    print("2. Run: python update_ngrok_url.py")
    print("3. Run: python setup_bot_correct.py")
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

Then just run: `python start_dev.py`

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
   - ✅ Run `python telegram_bot_correct.py`
   - ✅ Check bot token is valid

4. **"This site can't be reached"**
   - ✅ Restart ngrok: `.\ngrok.exe http 5000`
   - ✅ Update URL: `python update_ngrok_url.py`
   - ✅ Reconfigure bot: `python setup_bot_correct.py`

### Verification Scripts

Test your setup:

```powershell
# Check if all packages are installed
python check_telegram_version.py

# Test web app accessibility
python test_webapp.py

# Verify votes are being saved
python show_data_locations.py
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
python show_data_locations.py
```

**Test System:**
```powershell
python test_voting_system.py
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
4. Run `python setup_bot_correct.py` with production URL
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
2. Run the bot script: `python telegram_bot.py`
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
