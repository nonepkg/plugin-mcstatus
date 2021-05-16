import nonebot
from nonebot.plugin import on_shell_command, require
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    PrivateMessageEvent,
    GroupMessageEvent,
)
from nonebot import get_bots
from mcstatus import MinecraftServer

from nonebot_plugin_mcstatus.parser import Namespace, mc_parser
from nonebot_plugin_mcstatus.handle import Handle
from nonebot_plugin_mcstatus.data import Data

scheduler = require("nonebot_plugin_apscheduler").scheduler

# 注册 shell_like 事件响应器
mc = on_shell_command("mc", parser=mc_parser, priority=5)

# 每分钟进行一次检测
@scheduler.scheduled_job("cron", minute="*/5", id="mcstatus")
async def _():
    data = Data()
    server_list = data.get_server_list()
    bots = nonebot.get_bots()

    for type in server_list:
        for id in server_list[type]:
            for server in server_list[type][id]:
                try:
                    ping = await MinecraftServer.lookup(server.address).async_ping()
                    status = True
                except:
                    status = False
                if status != server.status:
                    server.status = status
                    data.remove_server(
                        server.name,
                        user_id=id if type == "user" else None,
                        group_id=id if type == "group" else None,
                    )
                    data.add_server(
                        server,
                        user_id=id if type == "user" else None,
                        group_id=id if type == "group" else None,
                    )
                    for bot in bots:
                        await bots[bot].send_msg(
                            user_id=id if type == "user" else None,
                            group_id=id if type == "group" else None,
                            message=(
                                "【服务器状态发生变化】\n"
                                + f"Name: {server.name}\n"
                                + f"Address: {server.address}\n"
                                + f"Status: {'On' if status else 'Off'}"
                                + (f"\nPing: {ping}" if status else "")
                            ),
                        )


@mc.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    args.user_id = event.user_id if isinstance(event, PrivateMessageEvent) else None
    args.group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
    args.is_admin = (
        event.sender.role in ["admin", "owner"]
        if isinstance(event, GroupMessageEvent)
        else False
    )
    if hasattr(args, "handle"):
        result = await getattr(Handle, args.handle)(args)
        if result:
            await bot.send(event, result)
