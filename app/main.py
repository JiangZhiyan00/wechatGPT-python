#!/usr/bin/python3
# coding=utf-8
import hashlib
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

import uvicorn

from chatGPT import getAnswer
from config import get_config
from msgTypeConstant import TEXT
from xmlUtil import parse_xml

route = '/wechat/chat/callback'
EMPTY_STR = ''

app = FastAPI(title='wechatGPT-api', description='wechatGPT接口文档', version='1.0.0', docs_url=None, redoc_url=None)


@app.get(route, summary='微信签名验证')
async def callback(signature, timestamp, nonce, echostr: int):
    return echostr
    # # 将数据添加进数组
    # params = [get_config('weixin', 'token'), timestamp, nonce]
    # # 排序
    # params.sort()
    # # 拼接字符串
    # tmp_str = EMPTY_STR.join(params).encode('utf-8')
    # # 进行sha1加密
    # sign = hashlib.sha1(tmp_str).hexdigest()
    # # 如果签名与微信的一致,返回echostr给微信
    # if signature == sign:
    #     print("验证成功:" + sign)
    #     return echostr
    # print("验证失败:" + sign)
    # return None


@app.post(route, summary='回复消息')
async def callback(request: Request):
    msg = parse_xml(await request.body())
    if msg is None:
        return EMPTY_STR
    if str(msg.MsgType).lower() == TEXT:
        return Response(getAnswer(msg), media_type="application/xml")
    # TODO 其他消息类型暂不处理


@app.get("/wechat/test", summary='测试')
async def test():
    return "success"


# 运行FastAPI应用
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
