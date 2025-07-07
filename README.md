# AWS Free Tier Monitor

监控多个 AWS 账户的 EC2 出站流量（每月 15GB 免费），并通过 Telegram 推送提醒。

## 使用方法

1. 配置 `aws_free_tier_monitor/config.py`
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 运行脚本：
   ```
   python run.py
   ```

支持设置 cron 定时运行。