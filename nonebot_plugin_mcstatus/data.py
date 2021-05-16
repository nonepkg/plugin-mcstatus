import yaml
from pathlib import Path
from typing import Optional, Union, List, Dict
from pydantic import BaseModel


class Server(BaseModel):
    name: str
    address: str
    status: bool


ServerList = Dict[str, Dict[int, List[Server]]]


class Data:
    __server_list: ServerList = {"user": {}, "group": {}}
    __path: Path

    def __init__(self, path: Path = Path() / "data" / "mcstatus" / "server_list.yml"):
        self.__path = path
        self.__load()

    def get_server_list(
        self, user_id: Optional[int] = None, group_id: Optional[int] = None
    ) -> Union[ServerList, List[Server]]:

        server_list = self.__server_list

        if user_id:
            if user_id not in server_list["user"]:
                server_list["user"][user_id] = []
            result = server_list["user"][user_id]
        elif group_id:
            if group_id not in server_list["group"]:
                server_list["group"][group_id] = []
            result = server_list["group"][group_id]
        else:
            result = server_list

        return result

    def add_server(
        self,
        server: Server,
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ):
        server_list = self.get_server_list(user_id, group_id)
        if server not in server_list:
            server_list.append(server)

        if user_id:
            self.__server_list["user"][user_id] = server_list
        elif group_id:
            self.__server_list["group"][group_id] = server_list

        self.__dump()

    def remove_server(
        self,
        name: str,
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ):

        server_list = list(
            filter(
                lambda server: server.name != name,
                self.get_server_list(user_id, group_id),
            )
        )

        if user_id:
            if server_list:
                self.__server_list["user"][user_id] = server_list
            else:
                self.__server_list["user"].pop(user_id)
        elif group_id:
            if server_list:
                self.__server_list["group"][group_id] = server_list
            else:
                self.__server_list["group"].pop(group_id)

        self.__dump()

    def __load(self):
        try:
            server_list = yaml.safe_load(self.__path.open("r", encoding="utf-8"))
            for type in server_list:
                for id in server_list[type]:
                    self.__server_list[type][id] = [
                        Server(**server) for server in server_list[type][id]
                    ]
        except FileNotFoundError:
            self.__server_list = {"user": {}, "group": {}}

    def __dump(self):
        self.__path.parent.mkdir(parents=True, exist_ok=True)
        server_list = {"user": {}, "group": {}}
        for type in self.__server_list:
            for id in self.__server_list[type]:
                server_list[type][id] = [
                    server.dict() for server in self.__server_list[type][id]
                ]
        yaml.dump(
            server_list,
            self.__path.open("w", encoding="utf-8"),
            allow_unicode=True,
        )
