from client import redis_connect
import requests
import json


redis = redis_connect()

def fetch_api_data(url: str) -> str:
    response = requests.get(url)
    return json.loads(response.text)


# define redis function that add new data to the cache if it doesn't exist
def add_to_cache_if_not_exists(key: str, dict: dict) -> None:
    ''' Add new data to the cache if key doesn't yet exist, print the data and returns it '''
    if redis.exists(key) == 0:
        print(f"new key '{key}' added  to redis")
        redis.hmset(key, dict)
    print(f"retrieving key '{key}' from redis")
    data = redis.hgetall(key)
    return data

def add_to_cache(key: str, dict: dict) -> None:
    ''' Add data to the cache'''
    print(f"adding data to key '{key}'")
    redis.hmset(key, dict)
    

def main():
    for page in range(1, 5):
        data = fetch_api_data(f'https://jsonplaceholder.typicode.com/posts/{page}')
        dict_from_redis = add_to_cache_if_not_exists(f'postss:{page}', data)


if __name__ == '__main__':
    main()




