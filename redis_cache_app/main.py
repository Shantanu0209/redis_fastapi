from fastapi import FastAPI
import redis
import time
import json

app = FastAPI()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

fake_user_db = {
    "1": {"name": "Alice", "age": 30},
    "2": {"name": "Bob", "age": 25},
    "3": {"name": "Charlie", "age": 28},
}

def slow_db_call(user_id:str):
    time.sleep(3)

    return fake_user_db.get(user_id, None)

@app.get("/user/{user_id}")
def get_user(user_id:str):

    cache_key = f"user_id:{user_id}"


    cache_user = r.get(cache_key)
    if cache_user:
        print("cache hit...")
        return json.loads(cache_user)

    else:
        print("cache missed ....")
        user = slow_db_call(user_id)
        if user:
            r.set(cache_key, json.dumps(user), ex=60)
    return user
