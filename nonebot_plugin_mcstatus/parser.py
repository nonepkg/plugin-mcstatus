from argparse import Namespace as ArgNamespace

from nonebot.rule import ArgumentParser


class Namespace(ArgNamespace):
    user_id: int
    group_id: int
    name: str
    address: str


mc_parser = ArgumentParser("mc")

subparsers = mc_parser.add_subparsers(dest="handle")

check = subparsers.add_parser("check", help="check server once")
check.add_argument("address")

add = subparsers.add_parser("add", help="add server")
add.add_argument("name")
add.add_argument("address")

remove = subparsers.add_parser("remove", help="remove server")
remove.add_argument("name")

list = subparsers.add_parser("list", help="show server list")
