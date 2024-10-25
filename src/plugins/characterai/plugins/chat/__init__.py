from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_message, on_command
from nonebot.adapters.qq import Bot, Event
from src.utils.db import db_read, db_insert, db_delete
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
    char_id = "06JnthTLSRBY2CI7oPKme5t15M9bSIgw0Qa1p7EaGmQ"
    token_data = db_read("xineyc", "config", {})
    token = token_data[0]["characterai"]["token"]

    client = aiocai.Client(token)
    me = await client.get_me()

    async with await client.connect() as chat:
        try:
            dialogue = db_read("xineyc", "dialogue", {"user_id": event.get_user_id()})
            if len(dialogue) == 0:
                new_chat, answer = await chat.new_chat(char_id, me.id)
                db_insert(
                    "xineyc",
                    "dialogue",
                    {"user_id": event.get_user_id(), "chat_id": new_chat.chat_id},
                )
                chat_id = new_chat.chat_id
            else:
                chat_id = dialogue[0]["chat_id"]
            message_str = str(event.get_message())
            response = await chat.send_message(char_id, chat_id, message_str)
            logger.info(f"{response.name}: {response.text}")
            await characterai_chat.finish(f"{response.text}")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise


# 清除对话
characterai_delete = on_command("清除对话", block=True)


@characterai_delete.handle()
async def clear_dialogue(bot: Bot, event: Event):
    db_delete("xineyc", "dialogue", {"user_id": event.get_user_id()})
    await characterai_delete.finish(f"{event.get_user_id()}的对话记忆已清除")
