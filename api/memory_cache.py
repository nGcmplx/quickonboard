import os
import json
import redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "memory"),  # use Docker service name
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

MAX_TURNS = 10  # user + assistant = 10 entries

def get_session_history(session_id: str, limit: int = MAX_TURNS) -> list[dict]:
    """Retrieve last N user-assistant messages (returns list of dicts)."""
    raw = redis_client.lrange(session_id, -limit * 2, -1)
    return [json.loads(m) for m in raw]

def append_to_session(session_id: str, user_msg: str, bot_msg: str):
    """Append a user & assistant turn to the session."""
    redis_client.rpush(session_id, json.dumps({"role": "user", "content": user_msg}))
    redis_client.rpush(session_id, json.dumps({"role": "assistant", "content": bot_msg}))
    redis_client.ltrim(session_id, -MAX_TURNS * 2, -1)  # Keep only last N exchanges
