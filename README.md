# Nonebot Plugin MCStatus

基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的 Minecraft 服务器状态查询插件

[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_mcstatus)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)
![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-mcstatus.svg)

### 安装

#### 从 PyPI 安装（推荐）

- 使用 nb-cli  

```
nb plugin install nonebot_plugin_mcstatus
```

- 使用 poetry

```
poetry add nonebot_plugin_mcstatus
```

- 使用 pip

```
pip install nonebot_plugin_mcstatus
```

#### 从 GitHub 安装（不推荐）

```
git clone https://github.com/Jigsaw111/nonebot_plugin_mcstatus.git
```

### 使用

**使用前请先确保命令前缀为空，否则请在以下命令前加上命令前缀 (默认为 `/` )。**

- `mc list` 查看当前会话（群/私聊）的关注服务器列表
- `mc add server address` 添加服务器到当前会话（群/私聊）的关注服务器列表
- `mc remove server` 从当前会话（群/私聊）的关注服务器列表移除服务器
- `mc check address` 查看指定地址的服务器状态（一次性）

### Bug

### To Do

### Changelog
