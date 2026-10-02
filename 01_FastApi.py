#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/10/2 6:27
@Author  : 596642721@qq.com
@File    : 01.FastApi.py
"""
import json
import logging
import os.path

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from chap07.pojo.ApiResponse import ApiResponse
from chap07.pojo.ChatRequest import ChatRequest
from chap07.utils.index import generate_session_id, get_session_data
from chap07.utils.prompt import SYSTEM_PROMPT

app = FastAPI(title="汉字迷盒", description="一个用Python编写的汉字迷盒游戏")

app.mount("/static", StaticFiles(directory="static"), name="static")

if not os.path.exists("sessions"):
    os.makedirs("sessions")


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get('/api/sessions')
async def get_sessions():
    logging.info("获取会话列表")
    session_lists = os.listdir("sessions")

    session_ids = [file.split(".")[0] for file in session_lists]
    session_ids.sort(reverse=True)

    return ApiResponse(code=200, message="获取会话列表成功", data=session_ids)


@app.post("/api/sessions")
async def session():
    session_id = generate_session_id()

    session_data = {
        "current_session": session_id,
        "messages": []
    }

    with open(os.path.join("sessions", session_id + ".json"), "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    return ApiResponse(code=200, message="创建会话成功", data=session_id)


@app.post("/api/chat")
async def chat(request: ChatRequest) -> ApiResponse:
    logging.info(f"与ai交互：{request.message} : {request.session_id}")
    # 加载json文件中的数据
    session_data = get_session_data(request.session_id)

    # 接入大模型
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *session_data["messages"],
        {"role": "user", "content": request.message}
    ]

    load_dotenv()

    client = OpenAI(
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")

    # 调用deepseek
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        stream=False,
        temperature=1.5
    )

    # 获取数据
    ai_message = response.choices[0].message.content

    # 更新消息列表中的信息
    messages.pop(0)
    messages = [*messages, {"role": "assistant", "content": ai_message}]

    session_data["messages"] = messages

    # 保存会话数据到json中
    with open(os.path.join("sessions", request.session_id + ".json"), "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    #     返回给前端数据
    return ApiResponse(code=200, message="请求成功", data=ai_message)


@app.get('/api/sessions/{session_id}')
async def get_session_by_id(session_id: str) -> ApiResponse:
    logging.info(f"获取会话详情：{session_id}")
    session_data = get_session_data(session_id)
    return ApiResponse(code=200, message="获取会话详情成功", data=session_data)


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str) -> ApiResponse:
    logging.info(f"删除会话：{session_id}")
    path = os.path.join("sessions", session_id + ".json")
    if os.path.exists(path):
        os.remove(path)
        return ApiResponse(code=200, message="删除会话成功", data=None)
    else:
        return ApiResponse(code=404, message="会话不存在", data=None)


# 处理全局异常
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    logging.error(f"Exception on {request.method} {request.url}: {exc}")
    return ApiResponse(code=500, message=str(exc), data=None)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
