#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/10/2 10:33
@Author  : 596642721@qq.com
@File    : ChatRequest.py
"""
from openai import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str
