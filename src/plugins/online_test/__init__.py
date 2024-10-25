from nonebot.plugin import PluginMetadata
from nonebot import on_command
import platform
import psutil
import cpuinfo

__plugin_meta__ = PluginMetadata(
    name="online_test",
    description="在线测试",
    usage="""
    使用
    /在线测试
    /系统消息
    """,
)


online_test = on_command("在线测试", aliases={"测试在线"}, block=True)


@online_test.handle()
async def handle_online_test():
    await online_test.finish("在……")


# 创建一个命令触发器
system_info = on_command("系统信息", aliases={"获取系统信息", "系统状态"}, block=True)


@system_info.handle()
async def handle_system_info():
    # 获取系统信息
    system_name = platform.system()
    system_version = platform.version()
    cpu_info = cpuinfo.get_cpu_info()
    cpu = cpu_info.get("brand_raw", "未知")
    cpu_usage = psutil.cpu_percent()

    memory = psutil.virtual_memory()
    memory_used = memory.used / (1024**3)  # 转换为 GB
    memory_total = memory.total / (1024**3)  # 转换为 GB
    memory_percentage = memory.percent

    # 格式化回复内容
    response = (
        f" 要……看看我的内在么……\n"
        f"系统名称: {system_name}\n"
        f"系统版本: {system_version}\n"
        f"CPU: {cpu}\n"
        f"CPU使用率: {cpu_usage}%\n"
        f"内存使用量: {
            memory_used:.2f} GB / {memory_total:.2f} GB ({memory_percentage}%)"
    )

    # 发送系统信息
    await system_info.finish(response)
