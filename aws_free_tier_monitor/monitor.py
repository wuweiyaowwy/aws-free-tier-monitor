import boto3
import datetime
from aws_free_tier_monitor.config import AWS_ACCOUNTS
from aws_free_tier_monitor.notifier import send_telegram_message

def get_data_transfer(account):
    try:
        session = boto3.Session(
            aws_access_key_id=account['access_key'],
            aws_secret_access_key=account['secret_key'],
            region_name=account.get('region', 'us-east-1')
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

        if not response["ResultsByTime"]:
            raise ValueError("No data returned from AWS Cost Explorer.")

        results = response["ResultsByTime"][0]["Groups"]
        total_usage_gb = 0.0

        for group in results:
            usage_quantity = float(group["Metrics"]["UsageQuantity"]["Amount"])
            total_usage_gb += usage_quantity

        return total_usage_gb

    except Exception as e:
        error_message = f"⚠️ AWS 成本查询错误：{str(e)}"
        print("❌ 错误：", error_message)
        return error_message  # 返回错误信息

def check_accounts():
    messages = []  # 存储所有账户的消息
    for account in AWS_ACCOUNTS:
        usage = get_data_transfer(account)
        name = account["name"]
        threshold = account["threshold_gb"]

        if isinstance(usage, str):  # 如果返回的是错误信息
            msg = f"🛑 AWS 成本查询错误（{name}）\n{usage}"
        elif usage >= threshold:
            msg = (
                f"🛰 AWS 出站流量提醒（{name}）\n\n"
                f"✅ 当前使用流量：{usage:.2f} GB / {threshold} GB\n"
                f"📅 截止日期：{datetime.date.today().strftime('%Y-%m-%d')}"
            )
        else:
            msg = (
                f"🛰 AWS 出站流量提醒（{name}）\n\n"
                f"✅ 当前使用流量：{usage:.2f} GB / {threshold} GB\n"
                f"📅 截止日期：{datetime.date.today().strftime('%Y-%m-%d')}"
            )
        
        messages.append(msg)  # 添加到消息列表

    # 一次性发送所有账户的消息
    final_message = "\n\n".join(messages)
    send_telegram_message(final_message)

