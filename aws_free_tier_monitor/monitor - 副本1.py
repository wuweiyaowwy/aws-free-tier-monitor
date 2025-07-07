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
        send_telegram_message(error_message)  # 发送错误通知
        print("❌ 错误：", error_message)
        return None  # 返回 None 表示查询失败

def check_accounts():
    for account in AWS_ACCOUNTS:
        usage = get_data_transfer(account)
        name = account["name"]
        threshold = account["threshold_gb"]

        if usage is None:  # 如果查询失败
            msg = (
                f"⚠️ AWS 成本查询失败（{name}）\n"
                "无法获取出站流量数据，请检查 AWS 设置或权限！"
            )
            send_telegram_message(msg)
        elif usage >= threshold:
            msg = (
                f"🛰 AWS 出站流量提醒（{name}）\n\n"
                f"✅ 当前使用流量：{usage:.2f} GB / {threshold} GB\n"
                f"⚠️ 已超过阈值（{threshold} GB）\n\n"
                f"📅 截止日期：{datetime.date.today().strftime('%Y-%m-%d')}"
            )
            send_telegram_message(msg)
            print("⚠️ " + msg.replace('\n', ' '))
        else:
            print(f"✅ {name}：{usage:.2f} GB / {threshold} GB")
