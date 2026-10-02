#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/10/2 10:25
@Author  : 596642721@qq.com
@File    : index.py.py
"""
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s")


def generate_session_id():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# 根据文件名获取会话数据
def get_session_data(session_id):
    with open(f"sessions/{session_id}.json", "r", encoding="utf-8") as f:
        return json.load(f)
