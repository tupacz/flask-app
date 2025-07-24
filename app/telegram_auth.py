import hashlib
import hmac
import json
from urllib.parse import unquote
from datetime import datetime, timedelta

def validate_telegram_data(init_data, bot_token):
    """
    Validate Telegram Web App init data
    """
    try:
        # Parse the init data
        parsed_data = {}
        for item in init_data.split('&'):
            if '=' in item:
                key, value = item.split('=', 1)
                parsed_data[unquote(key)] = unquote(value)
        
        if 'hash' not in parsed_data:
            return False, None
        
        # Extract the hash
        received_hash = parsed_data.pop('hash')
        
        # Create data check string
        data_check_arr = []
        for key, value in sorted(parsed_data.items()):
            data_check_arr.append(f"{key}={value}")
        data_check_string = '\n'.join(data_check_arr)
        
        # Create secret key
        secret_key = hmac.new(
            b"WebAppData", 
            bot_token.encode(), 
            hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            secret_key, 
            data_check_string.encode(), 
            hashlib.sha256
        ).hexdigest()
        
        # Verify hash
        if calculated_hash != received_hash:
            return False, None
        
        # Check auth date (data should be no older than 24 hours)
        if 'auth_date' in parsed_data:
            auth_date = datetime.fromtimestamp(int(parsed_data['auth_date']))
            if datetime.now() - auth_date > timedelta(hours=24):
                return False, None
        
        # Parse user data
        user_data = None
        if 'user' in parsed_data:
            user_data = json.loads(parsed_data['user'])
        
        return True, user_data
        
    except Exception as e:
        print(f"Error validating Telegram data: {e}")
        return False, None

def get_user_name(user_data):
    """
    Extract user name from Telegram user data
    """
    if not user_data:
        return "Unknown User"
    
    first_name = user_data.get('first_name', '')
    last_name = user_data.get('last_name', '')
    username = user_data.get('username', '')
    
    if first_name and last_name:
        return f"{first_name} {last_name}"
    elif first_name:
        return first_name
    elif username:
        return f"@{username}"
    else:
        return f"User {user_data.get('id', 'Unknown')}"
