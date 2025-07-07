import boto3
import datetime
from aws_free_tier_monitor.config import AWS_ACCOUNTS
from aws_free_tier_monitor.notifier import send_telegram_message

def get_data_transfer(account):
    session = boto3.Session(
        aws_access_key_id=account["access_key"],  # 使用正确的字段名
        aws_secret_access_key=account["secret_key"],  # 使用正确的字段名
        region_name=account.get("region", "us-east-1")
    )
    client = session.client('ce')

    start = datetime.date.today().replace(day=1).strftime('%Y-%m-%d')
    end = datetime.date.today().strftime('%Y-%m-%d')

    response = client.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UsageQuantity"],
        Filter={
            "And": [
                {"Dimensions": {"Key": "SERVICE", "Values": ["Amazon Elastic Compute Cloud - Compute"]}},
                {"Dimensions": {"Key": "USAGE_TYPE_GROUP", "Values": ["EC2: Data Transfer - Internet (Out)"]}},
            ]
        },
        GroupBy=[
            {"Type": "DIMENSION", "Key": "USAGE_TYPE"},
        ],
    )

    results = response["ResultsByTime"][0]["Groups"]
    total_usage_gb = 0.0

    for group in results:
        usage_quantity = float(group["Metrics"]["UsageQuantity"]["Amount"])
        total_usage_gb += usage_quantity

    return total_usage_gb

def check_accounts():
    for account in AWS_ACCOUNTS:
        usage = get_data_transfer(account)
        name = account["name"]
        threshold = account["threshold_gb"]

#        if usage >= threshold:
#            msg = (
#                f"🛰 AWS 出站流量提醒（{name}）\n\n"
#                f"✅ 当前使用流量：{usage:.2f} GB / 100 GB\n"
#                f"⚠️ 已超过阈值（{threshold} GB）\n\n"
#                f"📅 截止日期：{datetime.date.today().strftime('%Y-%m-%d')}"
#            )
#            print("⚠️ " + msg.replace('\n', ' '))
#            send_telegram_message(msg)
def check_accounts():
    for account in AWS_ACCOUNTS:
        usage = get_data_transfer(account)
        name = account["name"]
        threshold = account["threshold_gb"]

        # 无论是否超过阈值，都发送提醒
        msg = (
            f"🛰 AWS 出站流量提醒（{name}）\n\n"
            f"✅ 当前使用流量：{usage:.2f} GB / {threshold} GB\n"
            f"📅 截止日期：{datetime.date.today().strftime('%Y-%m-%d')}"
        )
        
        # 打印信息
        print(f"✅ {msg.replace('\n', ' ')}")

        # 发送 Telegram 消息
        send_telegram_message(msg)
#        else:
#            print(f"✅ {name}：{usage:.2f} GB / {threshold} GB")
