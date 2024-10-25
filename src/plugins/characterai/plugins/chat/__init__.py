from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_message
from nonebot.adapters.qq import Bot, Event
from src.utils.db import db_read
from characterai import aiocai
from nonebot.log import logger

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="CharacterAI对话",
    description="通过CharacterAI对话",
    usage="@Bot 你的问题",
    config=Config,
)

config = get_plugin_config(Config)

characterai_chat = on_message(priority=5)


@characterai_chat.handle()
async def handle_characterai_chat(bot: Bot, event: Event):

    await characterai_chat.finish(await characterai_client(event.get_message()))


async def characterai_client(message: str):
    char_id = "06JnthTLSRBY2CI7oPKme5t15M9bSIgw0Qa1p7EaGmQ"
    token_data = db_read("xineyc", "config", {})
    token = token_data[0]["characterai"]["token"]

    client = aiocai.Client(token)
    me = await client.get_me()

    async with await client.connect() as chat:
        try:
            new_chat, answer = await chat.new_chat(char_id, me.id)

            # Convert the message to a string if it's not already
            message_str = str(message)

            response = await chat.send_message(char_id, new_chat.chat_id, message_str)
            logger.info(f"{response.name}: {response.text}")
            return f"{response.text}"
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise
