import sys
import time
from typing import Optional, Dict, List
import asyncio
import json
import re

import httpx
from loguru import logger

from settings import QUEUE_NAME, PATTERNS_URL, UPDATE_MESSAGE_URL
from redis_connector import RedisConnector

logger.remove()
logger.add(sys.stderr, level="INFO")


class Manager:
    def __init__(self, queue_name: str) -> None:
        self.loop = asyncio.get_event_loop()
        self.queue = queue_name
        self.redis_connector = RedisConnector()
        self.patterns = []

    def start(self):
        logger.info("Starting manager")
        self.loop.run_until_complete(self.main())

    async def _get_message(self) -> Optional[Dict]:
        """Read and pop message from SQS queue"""
        logger.debug("Getting message from queue")
        item = self.redis_connector.get_item_from_zset(self.queue)
        if item:
            logger.debug(f"Message: {item}")
            return json.loads(item)

    @staticmethod
    async def update_message(
        client_msg_id: str, pattern_id: Optional[str]
    ) -> Optional[bool]:
        logger.info(f"Updating message {client_msg_id=} {pattern_id=}")
        async with httpx.AsyncClient() as client:
            try:
                data = {"client_msg_id": client_msg_id, "pattern_id": pattern_id}
                response = await client.post(UPDATE_MESSAGE_URL, json=data)
                logger.info(f"Response: {response.status_code=} {response.text=}")
                return True
            except httpx.ConnectError:
                logger.exception("Could not connect to update service")

    async def _get_patterns(self, retries: int = 0) -> List:
        if retries > 10:
            logger.error("Could not get patterns, Connection failed")
            return []
        async with httpx.AsyncClient() as client:
            try:
                logger.debug(f"{PATTERNS_URL=}")
                response = await client.get(PATTERNS_URL)
                if response.status_code != 200:
                    logger.error(
                        f"Could not get patterns: {response.status_code=} {response.text=}"
                    )
                    time.sleep(100000)
                    return []
                patterns_list = response.json()
                logger.debug(f"Patterns: {patterns_list}")
                return patterns_list
            except httpx.ConnectError:
                logger.exception("Could not connect to patterns service, retrying")
                await asyncio.sleep(5)
                return await self._get_patterns(retries + 1)
            except Exception as e:
                logger.exception(f"Error: {e}")
                return []

    async def main(self) -> None:
        """Main loop to read messages from SQS queue and execute tasks"""
        if not self.patterns:
            logger.info("No patterns found -> try to get patterns")
            self.patterns = await self._get_patterns()
        while self.patterns:
            logger.debug("Starting main loop")
            message = await self._get_message()
            if not message:
                logger.warning("No message found")
                await asyncio.sleep(1)
                continue
            self.loop.create_task(self.task(message))
            await asyncio.sleep(1)

    async def task(self, message) -> None:
        message_text = message["event"]["text"]
        client_msg_id = message["event"]["client_msg_id"]
        for pattern in self.patterns:
            logger.info(f"Checking message against {pattern=}")
            if re.search(pattern.get("regex", ""), message_text):
                logger.warning(f"Message leaked: {message=}")
                pattern_id = pattern.get("id")
                if not await self.update_message(client_msg_id, pattern_id):
                    logger.error("Could not update message")
                    self.redis_connector.add_item_to_zset(
                        self.queue, json.dumps(message, separators=(",", ":"))
                    )
                break
        else:
            logger.info("No pattern matched")
            if not await self.update_message(client_msg_id, None):
                logger.error("Could not update message")
                self.redis_connector.add_item_to_zset(
                    self.queue, json.dumps(message, separators=(",", ":"))
                )


if __name__ == "__main__":
    manager = Manager(
        queue_name=QUEUE_NAME,
    )
    manager.start()
