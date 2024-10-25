# 官方机器人无法正常获取用户相关的信息，暂待优化

# from nonebot import on_command
# from nonebot.params import CommandArg
# from nonebot.plugin import PluginMetadata
# from nonebot.matcher import Matcher
# from nonebot.adapters.qq import Bot, Event, MessageSegment, Message
# import requests
# import sqlite3
# import base64
# import time

# __plugin_meta__ = PluginMetadata(
#     name="cave",
#     description="回声洞",
#     usage="""
#     使用
#     /cave add <内容> -- 发送内容
#     /cave random -- 随机获取一条回声
#     /cave get <id> -- 获取指定id的回声
#     """,
# )

# # 数据库路径
# db_path = "cave.db"


# def init_db():
#     """初始化数据库并创建表"""
#     conn = sqlite3.connect(db_path)
#     c = conn.cursor()
#     c.execute(
#         """
#         CREATE TABLE IF NOT EXISTS echoes (
#             id INTEGER PRIMARY KEY,
#             sender_qq TEXT,
#             timestamp INTEGER,
#             message TEXT,
#             message_type TEXT,
#             image_base64 TEXT
#         )
#         """
#     )
#     conn.commit()
#     conn.close()


# # 初始化数据库
# init_db()

# # 添加回声内容的命令
# cave_add = on_command("cave add", aliases={"回声洞 add"}, priority=5)


# @cave_add.handle()
# async def handle_add_cave(bot: Bot, event: Event, args: Message = CommandArg()):
#     content = args.extract_plain_text().strip() or None
#     images = [seg.data['url'] for seg in args if seg.type == "image"] or None
#     if images.__len__() > 1:
#         await cave_add.finish('图片，有点……太多了')
#         pass
#     sender_qq = event.get_user_id()
#     timestamp = int(time.time())

#     # 计算下一个 ID
#     conn = sqlite3.connect(db_path)
#     c = conn.cursor()
#     c.execute("SELECT MAX(id) FROM echoes")
#     max_id = c.fetchone()[0]
#     new_id = (max_id + 1) if max_id is not None else 1

#     # 处理信息
#     if content and images:
#         image_bytes = requests.get(images[0]).content
#         image_base64 = base64.b64encode(image_bytes).decode("utf-8")

#         c.execute(
#             "INSERT INTO echoes (id, sender_qq, timestamp, message, message_type, image_base64) VALUES (?, ?, ?, ?, ?, ?)",
#             (new_id, sender_qq, timestamp, content, "text_image", image_base64),
#         )
#         conn.commit()
#         await cave_add.finish("回声已添加！")

# # 随机获取一条回声的命令
# cave_random = on_command("cave random", aliases={"回声洞 random"}, priority=5)


# @cave_random.handle()
# async def handle_random_cave():
#     conn = sqlite3.connect(db_path)
#     c = conn.cursor()
#     c.execute("SELECT * FROM echoes ORDER BY RANDOM() LIMIT 1")
#     echo = c.fetchone()
#     conn.close()

#     if echo:
#         echo_id, sender_qq, timestamp, message, message_type, image_base64 = echo
#         if message_type == "text":
#             await cave_random.finish(f"随机回声（来自 {sender_qq}）：{message}")
#         elif message_type == "image":
#             image_segment = MessageSegment.image(base64.b64decode(image_base64))
#             await cave_random.finish(f"随机回声（来自 {sender_qq}）：\n{image_segment}")
#         elif message_type == "text_image":
#             image_segment = MessageSegment.image(base64.b64decode(image_base64))
#             await cave_random.finish(
#                 f"随机回声（来自 {sender_qq}）：{message}\n{image_segment}"
#             )
#     else:
#         await cave_random.finish("暂无回声内容！")


# # 获取指定 ID 的回声
# cave_get = on_command("cave get", aliases={"回声洞 get"}, priority=5)


# @cave_get.handle()
# async def handle_get_cave(matcher: Matcher, args: Message = CommandArg()):
#     try:
#         echo_id = int(args.extract_plain_text().strip())
#         conn = sqlite3.connect(db_path)
#         c = conn.cursor()
#         c.execute("SELECT * FROM echoes WHERE id=?", (echo_id,))
#         echo = c.fetchone()
#         conn.close()

#         if echo:
#             _, sender_qq, timestamp, message, message_type, image_base64 = echo
#             time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
#             if message_type == "text":
#                 await matcher.finish(
#                     f"回声 {echo_id}（来自 {sender_qq}，时间：{time_str}）：{message}"
#                 )
#             elif message_type == "image":
#                 image_segment = MessageSegment.image(base64.b64decode(image_base64))
#                 await matcher.finish(
#                     f"回声 {echo_id}（来自 {sender_qq}，时间：{time_str}）：\n{image_segment}"
#                 )
#             elif message_type == "text_image":
#                 image_segment = MessageSegment.image(base64.b64decode(image_base64))
#                 await matcher.finish(
#                     f"回声 {echo_id}（来自 {sender_qq}，时间：{time_str}）：{message}\n{image_segment}"
#                 )
#         else:
#             await matcher.finish("未找到该ID的回声！")
#     except ValueError:
#         await matcher.finish("请输入有效的回声ID！")
