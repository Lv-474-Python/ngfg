"""
Redis manager module
"""

import pickle
from app import REDIS
from app.config import REDIS_EXPIRE_TIME


class RedisManager:
    """
    Class to interact with Redis
    """

    @staticmethod
    def get(name, key):
        """
        Get object from Redis by name and key

        :param name:
        :param key:
        :return:
        """
        result = REDIS.hget(name, key)
        if result is not None:
            result = pickle.loads(result)
        return result

    @staticmethod
    def set(name, instance):
        """
        Save object to Redis by name

        :param name:
        :param instance:
        :return:
        """
        REDIS.hset(name, 'data', pickle.dumps(instance))
        REDIS.expire(name, REDIS_EXPIRE_TIME)

    @staticmethod
    def delete(name):
        """
        Delete object from Redis by name

        :param name:
        :return:
        """
        return REDIS.delete(name)

    @staticmethod
    def generate_key(basic_name, hash_dict):
        """
        Generate key for instance

        :param basic_name:
        :param hash_dict:
        :return: generated string
        """
        hash_string = basic_name

        for key, value in hash_dict.items():
            hash_string += f'{key}:{value}'

        return hash_string
