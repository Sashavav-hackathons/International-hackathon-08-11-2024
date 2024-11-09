import redis

class RedisDB:

    __redis_connect = redis.Redis(host='localhost', port=6180)
    
    @classmethod
    def set_pair(cls, name: str, dialog: str):
        
        cls.__redis_connect.set(name, dialog)

    @classmethod
    def get_pair(cls, name):
        return cls.__redis_connect.get(name)
    