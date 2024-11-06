import os

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = int(os.environ.get("REDIS_DB", 0))

QUEUE_NAME = os.environ.get("QUEUE_NAME")

PATTERNS_URL = os.environ.get("PATTERNS_URL", "http://localhost:8000/patterns/")
UPDATE_LEAKED_MESSAGE_URL = os.environ.get("UPDATE_URL", "http://localhost:8000/update_leaked_message/")
