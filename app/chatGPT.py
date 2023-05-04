# coding=utf-8
import json
import time

import openai

from config import get_config
from message import TextMessage
from redisUtil import RedisUtil
from xmlUtil import get_answer_xml

EMPTY_STR = ''
OPENAI_KEYS = get_config('openai', 'keys').split(',')
USER_KEY_PREFIX = "wx_users:"
ALL_QUESTIONS_KEY_PREFIX = "all_questions:"
USER_QUESTIONS_KEY_PREFIX = "wx_users-questions:"
intervalFlag = get_config('server', 'interval_flag')
interval = int(get_config('server', 'interval'))
too_many_question = get_config('server', 'too_many_question')
session_time = int(get_config('server', 'session_time'))
answer_cache_time = int(get_config('server', 'answer_cache_time'))
redisUtil = RedisUtil()
key_point = -1


def getAnswer(message: TextMessage):
    answer = TextMessage(message.ToUserName, message.FromUserName, str(int(time.time())), EMPTY_STR)
    try:
        if redisUtil.is_hash_key_exist(ALL_QUESTIONS_KEY_PREFIX + message.FromUserName, message.Content):
            answer.Content = redisUtil.get_value(ALL_QUESTIONS_KEY_PREFIX + message.FromUserName,
                                                 message.Content).strip()
            print('openai-cache回复:' + answer.Content)
        elif intervalFlag and redisUtil.exist(USER_KEY_PREFIX + message.FromUserName):
            answer.Content = too_many_question
        else:
            messages = redisUtil.get_all_list_items(USER_QUESTIONS_KEY_PREFIX + message.FromUserName)
            user_messages = []
            for msg in messages:
                user_messages.append(json.loads(msg, object_hook=dict))
            user_message = {'content': message.Content, 'role': 'user'}
            user_messages.append(user_message)
            redisUtil.add_str_ex(USER_KEY_PREFIX + message.FromUserName, interval, 0)
            # 随机拿一个key
            global key_point
            key_point = (key_point + 1) % len(OPENAI_KEYS)
            openai.api_key = OPENAI_KEYS[key_point]
            # 调用openai获取回复
            openaiMessage = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=user_messages
            ).choices[0].message
            answer.Content = openaiMessage.content.strip()
            openaiMessage.content = answer.Content
            redisUtil.hset(ALL_QUESTIONS_KEY_PREFIX + message.FromUserName, message.Content, answer.Content)
            redisUtil.set_expire_time(ALL_QUESTIONS_KEY_PREFIX + message.FromUserName, answer_cache_time)
            redisUtil.rpush(USER_QUESTIONS_KEY_PREFIX + message.FromUserName,
                            json.dumps(user_message, ensure_ascii=False))
            redisUtil.rpush(USER_QUESTIONS_KEY_PREFIX + message.FromUserName,
                            json.dumps(openaiMessage, ensure_ascii=False))
            redisUtil.set_expire_time(USER_QUESTIONS_KEY_PREFIX + message.FromUserName, session_time)
            print('openai回复:' + answer.Content)
    except Exception as ex:
        print('openai回复信息错误:' + str(ex))
        answer.Content = "ChatGPT正忙,请稍后再试..."
    return get_answer_xml(answer)
