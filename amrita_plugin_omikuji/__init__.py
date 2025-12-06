import contextlib
import os
from datetime import datetime
from importlib import metadata

from nonebot import get_driver, logger
from nonebot.plugin import PluginMetadata, require

require("amrita.plugins.chat")
require("amrita.plugins.menu")

from amrita.plugins.chat.API import ToolsManager

from . import commands, llm_tool, sql_models
from .cache import OmikujiCache
from .config import get_cache_dir, get_config
from .llm_tool import TOOL_DATA

__plugin_meta__ = PluginMetadata(
    name="御神签",
    description="依赖AmritaBot的聊天御神签抽签插件模块",
    usage="/omikuji [板块]\n/omikuji 解签\n或者使用聊天直接抽签。",
    type="application",
    homepage="https://github.com/AmritaBot/amrita_plugin_omikuji",
    supported_adapters={"~onebot.v11"},
)


@get_driver().on_startup
async def init():
    version = "Unknown"
    with contextlib.suppress(Exception):
        version = metadata.version("amrita_plugin_omikuji")
        if "dev" in version:
            logger.warning("当前版本为开发版本，可能存在不稳定情况！")
    logger.info(f"Loading OMIKUJI V{version}......")
    conf = get_config()
    if conf.enable_omikuji:
        ToolsManager().register_tool(TOOL_DATA)
    logger.info("正在初始化缓存数据......")
    os.makedirs(get_cache_dir(), exist_ok=True)
    for cache in get_cache_dir().glob("*.json"):
        if cache is not None:
            with cache.open("r", encoding="utf-8") as f:
                data = OmikujiCache.model_validate_json(f.read())
            if not data.timestamp.date() == datetime.now().date():
                os.remove(str(cache))
    logger.info("缓存数据初始化完成！")


__all__ = ["commands", "llm_tool", "sql_models"]
