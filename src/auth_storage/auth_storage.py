from redis import Redis
if __name__!= "__main__":
    import config as config

if __name__ == "__main__":
    redis_store = Redis(host="127.0.0.1", port=6379, db=0, password="", decode_responses=True)
else:
    redis_store = Redis(host=config.redis_host, port=config.redis_port, password=config.redis_password, decode_responses=True)

class UserAuthStorage():
    __solt__ = ()

    @staticmethod
    def save_auth_info(value: dict, id: int, expires: int = None) -> None:
        result = redis_store.hset(name=f"user-session:{id}", mapping=value)
        if expires is not None:
            redis_store.expire(name=f"user-session:{id}", time=expires)


    @staticmethod
    def delete_auth_info(id: str) -> str:
        redis_store.hdel(name=id)


    @staticmethod
    def get_auth_info(id: str) -> dict:
        return redis_store.hgetall(name=f"user-session:{id}")


if __name__ == "__main__":
    redis_store.set("foo", "bar")
    print(redis_store.get("foo"))

    # result = redis_store.hset('user-session:123', mapping={
    #     'name': 'John',
    #     "surname": 'Smith',
    #     "company": 'Redis',
    #     "age": 29
    # })
    print(result)
    # print(redis_store.delete('user-session:123'))
    print(redis_store.hgetall('user-session:123'))

    