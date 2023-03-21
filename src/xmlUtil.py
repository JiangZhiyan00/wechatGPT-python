# coding=utf-8
import xml.etree.ElementTree as ET

from message import TextMessage
import msgTypeConstant

XML_PREFIX = '<![CDATA['
XML_SUFFIX = ']]>'


# 解析微信消息xml为Message对象
def parse_xml(xml_str):
    root = ET.fromstring(xml_str)
    FromUserName = root.find("FromUserName").text
    ToUserName = root.find("ToUserName").text
    CreateTime = root.find("CreateTime").text
    MsgType = root.find("MsgType").text
    # 文本消息
    if msgTypeConstant.TEXT == MsgType.lower():
        Content = root.find("Content").text
        return TextMessage(FromUserName, ToUserName, CreateTime, Content)
    # TODO 其他类型消息暂不处理
    return None


def get_answer_xml(answer: TextMessage):
    xml = ET.Element('xml')
    ET.SubElement(xml, 'FromUserName').text = XML_PREFIX + answer.FromUserName + XML_SUFFIX
    ET.SubElement(xml, 'ToUserName').text = XML_PREFIX + answer.ToUserName + XML_SUFFIX
    ET.SubElement(xml, 'CreateTime').text = XML_PREFIX + answer.CreateTime + XML_SUFFIX
    ET.SubElement(xml, 'MsgType').text = XML_PREFIX + answer.MsgType + XML_SUFFIX
    ET.SubElement(xml, 'Content').text = XML_PREFIX + answer.Content + XML_SUFFIX
    ET.SubElement(xml, 'FuncFlag').text = XML_PREFIX + str(answer.FuncFlag) + XML_SUFFIX
    return ET.tostring(xml, encoding='utf-8').decode()
