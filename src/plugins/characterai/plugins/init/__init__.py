from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.qq import Bot, Event, Message, EventType
from nonebot.log import logger
from characterai import sendCode, authUser
from src.utils.db import db_insert, db_read, db_delete

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="CharacterAI初始化",
    description="通过提供的数据获取token",
    usage="@Bot 你的问题",
    config=Config,
)

config = get_plugin_config(Config)

characterai = on_command("cai init", block=True)


@characterai.handle()
async def handle_characterai(bot: Bot, event: Event):
    if event.__type__ == EventType.C2C_MESSAGE_CREATE:
        await characterai.finish("请发送/cai email [你的characterai登录邮箱]")
    else:
        await characterai.finish("请私聊发送/cai init")


characterai_init = on_command("初始化cai", block=True)


@characterai_init.handle()
async def handle_characterai_init(bot: Bot, event: Event):
    await characterai_init.finish("请私聊发送/cai init")


characterai_email = on_command("cai email", block=True)


@characterai_email.handle()
async def handle_characterai_email(bot: Bot, event: Event, args: Message = CommandArg()):
    if event.__type__ == EventType.C2C_MESSAGE_CREATE:
        email = args.extract_plain_text()
        if email:
            try:
                sendCode(email)
                # 使用用户ID作为键来存储邮箱
                db_insert("xineyc", "cache", {event.get_user_id(): email})
                await characterai_email.finish(
                    "发送成功，请检查邮箱，输入/cai auth [登录url]"
                )
            except Exception as e:
                logger.error(e)
                await characterai_email.finish("发送验证码失败，请重试")
        else:
            await characterai_email.finish("请输入你的characterai登录邮箱")
    else:
        await characterai_email.finish("请私聊发送/cai init")


characterai_auth = on_command("cai auth", block=True)


@characterai_auth.handle()
async def handle_characterai_auth(bot: Bot, event: Event, args: Message = CommandArg()):
    if event.__type__ == EventType.C2C_MESSAGE_CREATE:
        loginUrl = args.extract_plain_text()
        if loginUrl:
            try:
                # 使用用户ID来读取邮箱
                email = db_read("xineyc", "cache", {event.get_user_id(): None})[0][
                    "email"
                ]
                logger.info(f"选择登录的邮箱: {email} \n选择的登录url: {loginUrl}")
                if email:
                    token = authUser(loginUrl, email)
                    logger.info(f"获取到的token: {token}")
                    db_delete("xineyc", "cache", {event.get_user_id(): None})
                    db_insert("xineyc", "config", {
                              "characterai": {"token": token}})
                    await characterai_auth.finish("登录成功")
                else:
                    await characterai_auth.finish("未找到缓存的邮箱，请重新发送/cai email")
            except Exception as e:
                logger.error(e)
                await characterai_auth.finish("登录失败，请重试")
        else:
            await characterai_auth.finish("请检查你的输入是否合法")
    else:
        await characterai_auth.finish("请私聊发送/cai init")
