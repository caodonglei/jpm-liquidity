""" the singleton of redis client
"""
import time
import json
import redis
from redis import ConnectionPool
from functools import lru_cache

from env import CONF_REDIS, DATA_REDIS


class RedisClient:
    def __init__(self, conn_conf: dict):
        if conn_conf:
            self.pool = ConnectionPool(**conn_conf)
            self.conn = redis.Redis(connection_pool=pool)
        else:
            self.conn = None

    def _check_connection(self):
        try:
            if self.conn and not self.conn.ping():
                self.conn = redis.Redis(connection_pool=self.pool)
        except redis.RedisError:
            raise ConnectionError("Local node unavailable")

    def get_int(key: str) -> int:
        """ get int value
        """
        self._check_connection()
        res = self.conn.get(key)
        if res:
            return int(res)
        return res

    def get_dict(key: str) -> dict:
        """ get dict object
        """
        res = self.conn.get(key)
        if res:
            return json.loads(res)
        return res

    def set_int(key: str, value: int):
        """ get int value
        """
        if isinstanceof(value, int):
            self.conn.set(key, value)

    def set_dict(key: str, value: dict):
        """ get dict object
        """
        if value:
            self.conn.set(key, json.dumps(value))


CONF_REDIS_CLIENT = RedisClient(CONF_REDIS)
DATA_REDIS_CLIENT = RedisClient(DATA_REDIS)