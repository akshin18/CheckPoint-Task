import asyncio
import json
import re
from typing import Optional, Dict, List

import httpx

from dlp.settings import QUEUE_NAME, PATTERNS_URL, UPDATE_LEAKED_MESSAGE_URL
from redis_connector import RedisConnector


class Manager:
    def __init__(self, queue_name: str):
        self.loop = asyncio.get_event_loop()
        self.queue = queue_name
        self.redis_connector = RedisConnector()
        self.patterns = [
    {
        "name": "credit card",
        "regex": "(?:\\d{4}-?){4}",
        "id": "7c71ded6-ae28-4f41-ac52-825cb92bda69"
    }
]

    def start(self):
        self.loop.run_until_complete(self.main())

    async def _get_message(self) -> Optional[Dict]:
        """Read and pop message from SQS queue"""
        item = self.redis_connector.get_item_from_zset(self.queue)
        if item:
            return json.loads(item)
    
    @staticmethod
    async def upload_leaked_message(client_msg_id: str, pattern_id: str) -> None:
        async with httpx.AsyncClient() as client:
            try:
                data = {"client_msg_id": client_msg_id, "pattern_id": pattern_id}
                response = await client.post(UPDATE_LEAKED_MESSAGE_URL, json=data)
                return response.json()
            except httpx.ConnectError:
                pass
    
    @staticmethod
    async def _get_patterns() -> List:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(PATTERNS_URL)
                return response.json()
            except httpx.ConnectError:
                return []
            
    async def main(self) -> None:
        """Main loop to read messages from SQS queue and execute tasks"""
        if not self.patterns:
            self.patterns = await self._get_patterns()
        while self.patterns:
            message = await self._get_message()
            
            self.loop.create_task(self.task(message))
            await asyncio.sleep(1)
            
    async def task(self, message):
        for pattern in self.patterns:
            if re.search(pattern.get("regex", ""), message["event"]["text"]):
                pattern_id = pattern.get("id")
                await self.upload_leaked_message(message, pattern_id)
                break
                
                


if __name__ == "__main__":
    manager = Manager(
        queue_name=QUEUE_NAME,
    )
    manager.start()
