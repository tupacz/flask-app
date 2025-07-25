"""
Test script to verify the Telegram Mini App setup
"""

import os
import sys

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import flask
        print("✅ Flask imported successfully")
        
        import telegram
        print("✅ python-telegram-bot imported successfully")
        
        import cryptography
        print("✅ cryptography imported successfully")
        
        import requests
        print("✅ requests imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_structure():
    """Test if the app structure is correct"""
    required_files = [
        'run.py',
        'config.py',
        'app/__init__.py',
        'app/routes.py',
        'app/telegram_auth.py',
        'app/templates/telegram_index.html',
        'app/static/telegram_styles.css'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_configuration():
    """Test configuration"""
    try:
        from config import Config
        print("✅ Configuration imported successfully")
        
        # Check if important config values are set
        if hasattr(Config, 'TELEGRAM_BOT_TOKEN'):
            if Config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
                print("⚠️  TELEGRAM_BOT_TOKEN needs to be set")
            else:
                print("✅ TELEGRAM_BOT_TOKEN is configured")
        
        if hasattr(Config, 'WEB_APP_URL'):
            if 'your-domain.com' in Config.WEB_APP_URL:
                print("⚠️  WEB_APP_URL needs to be updated with your domain")
            else:
                print("✅ WEB_APP_URL is configured")
                
        return True
    except ImportError as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_telegram_auth():
    """Test Telegram authentication module"""
    try:
        from app.telegram_auth import validate_telegram_data, get_user_name
        print("✅ Telegram authentication module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Telegram auth error: {e}")
        return False

def main():
    print("🔍 Testing Telegram Mini App Setup...")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("App Structure", test_app_structure),
        ("Configuration", test_configuration),
        ("Telegram Auth", test_telegram_auth)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your Telegram Mini App is ready!")
        print("\n📝 Next steps:")
        print("1. Set your TELEGRAM_BOT_TOKEN in config.py or environment variable")
        print("2. Deploy your Flask app to a hosting service (with HTTPS)")
        print("3. Update WEB_APP_URL with your deployment URL")
        print("4. Set up your bot with @BotFather")
        print("5. Run: python telegram_bot.py")
        print("6. Test your bot!")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
