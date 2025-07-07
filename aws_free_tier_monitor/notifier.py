import requests
from aws_free_tier_monitor.config import TELEGRAM_CONFIG

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_CONFIG['bot_token']}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CONFIG['chat_id'],
        "text": message
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("✅ Telegram 消息已发送！")
    else:
        print("⚠️ Telegram 消息发送失败！")
