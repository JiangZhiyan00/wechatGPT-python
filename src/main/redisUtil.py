import redis

from main import cf


class RedisUtil:
    def __init__(self, host=cf.get('redis', 'host'), port=cf.get('redis', 'port'), db=cf.get('redis', 'db'),
                 password=cf.get('redis', 'password'), decode=True):
        pool = redis.ConnectionPool(host=host, port=port, db=db, password=password, decode_responses=decode)
        self.r = redis.Redis(connection_pool=pool)

    # 是否存在key的缓存
    def exist(self, key):
        return self.r.exists(key)
    ###################################################      string方法       ###################################################
    # 加入缓存,存在会替换
    def set_str(self, key, value):  # value可以为复杂的json
        return self.r.set(key, value)

    # 不存在则加入,否则不变
    def add_str_nx(self, key, value):  # value可以为复杂的json
        return self.r.setnx(key, value)

    # 加入缓存,存在会替换,并加入过期时间(s)
    def add_str_ex(self, key, time, value):  # value可以为复杂的json
        return self.r.setex(key, time, value)

    # 获取缓存
    def get_str(self, key):
        return self.r.get(key)

    ###################################################      list方法       ###################################################
    # 返回指定key对应list的长度
    def list_len(self, key):
        return self.r.llen(key)

    # 添加新元素到list的最右方
    def rpush(self, key, *values):
        self.r.rpush(key, *values)  # rpush 如果没有列表会创建 rpushx不创建

    # 弹出list里的第一个元素,如果队列为空返回None
    def get_and_pop_first(self, key):
        return self.r.lpop(key)

    # 获取list对应索引的值
    def get_item_index(self, key, index):
        return self.r.lindex(key, index)

    # 获取list所有元素
    def get_all_list_items(self, key):  # 获取list所有元素 无key会返回[]
        return self.r.lrange(key, 0, -1)

    # 获取list中start到end的元素,切头切尾
    def get_list_item(self, key, start, end):
        return self.r.lrange(key, start, end)

    # 删除list中第一个值为value的元素
    def del_value(self, key, value):
        self.r.lrem(key, 1, value)

    # 删除list中指定数量的value,count为0表示删除所有值为value的元素
    def del_more_values(self, key, count, value):
        self.r.lrem(key, count, value)

    # 获取并只保留start-end的元素,切头切尾
    def save_start2end(self, key, start, end):
        return self.r.ltrim(key, start, end)

    # 批量获取删除
    def batch_get_and_pop(self, key, n):  # n>=1, 返回格式[['value'], True]
        p = self.r.pipeline()
        p.lrange(key, 0, n - 1)
        p.ltrim(key, n, -1)
        data = p.execute()
        return data

    ###################################################      set集合方法       ###################################################
    # 加入集合中
    def add2set(self, key, *values):
        self.r.sadd(key, *values)

    # 查看元素是否存在集合中
    def is_member_exist(self, key, member):
        check = self.r.sismember(key, member)
        return check

    ###################################################      hash散列方法       ###################################################
    # 向item散列中添加key-value键值对
    def hset(self, item, key, value):
        self.r.hset(item, key, value)

    # 不存在才添加
    def hset_nx(self, item, key, value):
        self.r.hsetnx(item, key, value)

    # 获取item散列中key对应的value
    def get_value(self, item, key):
        return self.r.hget(item, key)  # key不存在会返回None

    # 批量获取item哈希中多个key对应的value
    def get_values(self, item, keyList):
        return self.r.hmget(item, keyList)  # key不存在会返回None ['a', 's', None, None]

    # 批量删除item哈希中key-value
    def del_key_value(self, item, *keys):
        self.r.hdel(item, *keys)

    # 判断item哈希中是否存在key
    def is_hash_key_exist(self, item, key):
        return self.r.hexists(item, key)

    # 获取item哈希中所有key
    def get_all_keys(self, item):
        return self.r.hkeys(item)

    # 获取item哈希中所有value
    def get_all_values(self, item):
        return self.r.hvals(item)

    # 获取item哈希中所有key-value键值对
    def get_all_key_values(self, item):
        return self.r.hgetall(item)

    # 获取item散列key-value个数
    def get_hash_size(self, item):
        return self.r.hlen(item)

    ###################################################      通用方法       ###################################################
    # 查看指定key距离过期的剩余秒数
    def get_expire_time(self, key):
        return self.r.ttl(key)

    # 给指定key设置过期时间(秒)
    def set_expire_time(self, key, time):
        return self.r.expire(key, time)
