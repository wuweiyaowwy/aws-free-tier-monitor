AWS_ACCOUNTS = [
    {
        "name": "XXX",
        "access_key": "XXX",  # 确保用 'access_key'
        "secret_key": "XXX",  # 确保用 'secret_key'
        "region": "XXX",
        "threshold_gb": 100
    }, 
    {
        "name": "XXX",  # 第二个账户
        "access_key": "XXX",  # 真实的 access_key
        "secret_key": "XXX",  # 真实的 secret_key
        "region": "XXX",  # 选择合适的 region
        "threshold_gb": 100  # 你可以设置第二个账户的阈值
    }
]

TELEGRAM_CONFIG = {
    "bot_token": "XXX",
    "chat_id": "-XXX"
}
