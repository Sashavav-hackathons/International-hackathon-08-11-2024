import redis

class RedisDB:
    """
        Класс, реализующий взаимодействие с базой данных Redis

        __redis_connect - класс базы данных

        set_pair() - метод, устанавливающий в элемент с индексом name значение dialog

        get_pair() - метод, возвращающий значение элемента с индексом dialog
    """

    __redis_connect = redis.Redis(host='localhost', port=6180)
    
    @classmethod
    def set_pair(cls, name: str, dialog: str):
        
        cls.__redis_connect.set(name, dialog)

    @classmethod
    def get_pair(cls, name):
        return cls.__redis_connect.get(name)
    