#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/10/2 10:33
@Author  : 596642721@qq.com
@File    : ApiResponse.py
"""
from typing import Any

from openai import BaseModel


class ApiResponse(BaseModel):
    code: int
    message: str
    data: Any  # 任意类型的数据
