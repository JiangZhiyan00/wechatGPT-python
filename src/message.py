# coding=utf-8
"""微信消息类"""


class BaseMessage(object):
    def __init__(self, FromUserName, ToUserName, CreateTime, MsgType, FuncFlag=0):
        self.FromUserName = FromUserName
        self.ToUserName = ToUserName
        self.CreateTime = CreateTime
        self.MsgType = MsgType
        self.FuncFlag = FuncFlag


class TextMessage(BaseMessage):
    def __init__(self, FromUserName, ToUserName, CreateTime, Content, FuncFlag=0):
        super(TextMessage, self).__init__(FromUserName, ToUserName, CreateTime, 'text', FuncFlag)
        self.Content = Content
