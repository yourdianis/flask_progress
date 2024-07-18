import redis

def test_redis_connection():
    try:
        client = redis.StrictRedis(
            host='192.168.0.49',
            port=6379,
            password='123456',
            db=0,
            decode_responses=True
        )
        client.ping()
        print("Successfully connected to Redis")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")

test_redis_connection()
