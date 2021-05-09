import yaml
from pathlib import Path
from typing import Optional, Union, Any, Dict


class ServerList:
    __server_list: Dict[str, Dict[int, Dict[str, Any]]]
    __path: Path

    def __init__(self, path=Path() / "data" / "mcstatus" / "server_list.yml"):
        self.__path = path
        self.__load()

    def get_server(
        self, user_id: Optional[int] = None, group_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:

        server_list = self.__server_list

        if user_id:
            if user_id not in server_list["user"]:
                server_list["user"][user_id] = {}
            result = server_list["user"][user_id]
        elif group_id:
            if group_id not in server_list["group"]:
                server_list["group"][group_id] = {}
            result = server_list["group"][group_id]
        else:
            result = server_list

        return result

    def add_server(
        self,
        server: Dict[str, Any],
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ):
        self.__update_server("add", server, user_id, group_id)

    def remove_server(
        self,
        server: str,
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ):
        self.__update_server("remove", server, user_id, group_id)

    # 更新待办事项列表

    def __update_server(
        self,
        mode: str,
        server: Union[str, Dict[str, Any]],
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ):

        tmp_server_list = self.get_server(user_id, group_id)

        if mode == "add":
            tmp_server_list.update(server)
        elif mode == "remove":
            tmp_server_list.pop(server)

        if user_id:
            self.__server_list["user"][user_id] = tmp_server_list
            if not tmp_server_list:
                self.__server_list["user"].pop(user_id)
        elif group_id:
            self.__server_list["group"][group_id] = tmp_server_list
            if not tmp_server_list:
                self.__server_list["group"].pop(group_id)
        self.__dump()

    def __load(self):
        try:
            self.__server_list = yaml.safe_load(self.__path.open("r", encoding="utf-8"))
        except FileNotFoundError:
            self.__server_list = {"user": {}, "group": {}}

    def __dump(self):
        self.__path.parent.mkdir(parents=True, exist_ok=True)
        yaml.dump(
            self.__server_list,
            self.__path.open("w", encoding="utf-8"),
            allow_unicode=True,
        )
