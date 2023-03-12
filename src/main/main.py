#!/usr/bin/python3
# coding=utf-8
import hashlib
from configparser import ConfigParser
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

import uvicorn

import msgTypeConstant
import chatGPT
from xmlUtil import parse_xml

route = '/callback'
EMPTY_STR = ''
cf = ConfigParser()
cf.read('resources/config.ini', encoding="utf-8")

app = FastAPI(title='wechatGPT-api', description='wechatGPT接口文档', version='1.0.0')


@app.get(route, summary='微信签名验证')
async def callback(signature, timestamp, nonce, echostr):
    # 将数据添加进数组
    params = [cf.get('weixin', 'token'), timestamp, nonce]
    # 排序
    params.sort()
    # 拼接字符串
    tmp_str = EMPTY_STR.join(params).encode('utf-8')
    # 进行sha1加密
    sign = hashlib.sha1(tmp_str).hexdigest()
    # 如果签名与微信的一致,返回echostr给微信
    if signature == sign:
        return echostr
    return None


@app.post(route, summary='回复消息')
async def callback(request: Request):
    msg = parse_xml(await request.body())
    if msg is None:
        return EMPTY_STR
    if str(msg.MsgType).lower() == msgTypeConstant.TEXT:
        return Response(chatGPT.getAnswer(msg), media_type="application/xml")
    # TODO 其他消息类型暂不处理


# 运行FastAPI应用
if __name__ == "__main__":
    uvicorn.run(app, host=cf.get('server', 'host'), port=int(cf.get('server', 'port')))
