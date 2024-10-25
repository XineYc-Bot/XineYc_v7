from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_message, on_command
from nonebot.params import CommandArg
from nonebot.adapters.qq import Bot, Event, Message, EventType
from nonebot.log import logger

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="CharacterAI",
    description="使用CharacterAI对话",
    usage="@Bot 你的问题",
    config=Config,
)

config = get_plugin_config(Config)

characterai = on_command("cai init")


@characterai.handle()
async def handle_characterai(bot: Bot, event: Event, args: Message = CommandArg()):
    if event.__type__ == EventType.C2C_MESSAGE_CREATE:
        await characterai.finish("请发送/cai email [你的characterai登录邮箱]")
    else:
        await characterai.finish("请私聊发送/cai init")


characterai_init = on_command("初始化cai")


@characterai_init.handle()
async def handle_characterai_init(bot: Bot, event: Event):
    await characterai_init.finish("请私聊发送/cai init")
