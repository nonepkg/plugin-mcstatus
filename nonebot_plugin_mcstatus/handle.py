from typing import List, cast

from mcstatus import JavaServer

from nonebot_plugin_mcstatus.parser import Namespace
from nonebot_plugin_mcstatus.data import Data, Server


class Handle:
    @classmethod
    async def check(cls, args: Namespace) -> str:
        try:
            ping = await JavaServer.lookup(args.address).async_ping()
            status = True
        except:
            ping = None
            status = False

        return (
            f"Address: {args.address}\n"
            + f"Status: {'On' if status else 'Off'}"
            + (f"\nPing: {ping}" if status else "")
        )

    @classmethod
    async def add(cls, args: Namespace) -> str:
        try:
            await JavaServer.lookup(args.address).async_ping()
            status = True
        except:
            status = False

        Data().add_server(
            Server(name=args.name, address=args.address, status=status),
            args.user_id,
            args.group_id,
        )

        return "添加服务器成功！"

    @classmethod
    async def remove(cls, args: Namespace) -> str:
        Data().remove_server(args.name, args.user_id, args.group_id)

        return "移除服务器成功！"

    @classmethod
    async def list(cls, args: Namespace) -> str:
        server_list = Data().get_server_list(args.user_id, args.group_id)

        if server_list:
            return "本群关注服务器列表如下：\n" + "\n".join(
                f"[{'o' if server.status else 'x'}] {server.name} ({server.address})"
                for server in cast(List[Server], server_list)
            )
        else:
            return "本群关注服务器列表为空！"
