import pickle
from app import REDIS
from app.config import REDIS_EXPIRE_TIME


class RedisManager:
    @staticmethod
    def get(name, key):
        result = REDIS.hget(name, key)
        if result is not None:
            result = pickle.loads(result)
        return result

    @staticmethod
    def set(name, instance):
        REDIS.hset(name, 'data', pickle.dumps(instance))
        REDIS.expire(name, REDIS_EXPIRE_TIME)

    @staticmethod
    def generate_hash_string_by_dict(basic_name, hash_dict):
        hash_string = basic_name

        for key, value in hash_dict.items():
            hash_string += f'{key}:{value}'

        return hash_string
