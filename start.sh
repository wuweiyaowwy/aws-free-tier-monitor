#!/bin/bash
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "?? 正在创建虚拟环境..."
    python3 -m venv venv
fi

echo "? 激活虚拟环境..."
source venv/bin/activate

echo "?? 安装依赖..."
pip install -r requirements.txt

echo "?? 执行脚本..."
python run.py