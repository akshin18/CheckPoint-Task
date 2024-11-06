from typing import Optional

from redis import Redis

from settings import REDIS_HOST, REDIS_PORT, REDIS_DB


class RedisConnector:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def get_item_from_zset(self, key: str, index=0) -> Optional[str]:
        # Get one item from the sorted set at the specified index
        items = self.redis.zrange(key, index, index)
        if items:
            self.remove_item_from_zset(key, items[0])
            return items[0]
        return None

    def remove_item_from_zset(self, key, value):
        # Remove the item from the sorted set
        self.redis.zrem(key, value)