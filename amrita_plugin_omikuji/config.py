from __future__ import annotations

from pathlib import Path

from nonebot import get_plugin_config
from nonebot_plugin_localstore import get_plugin_cache_dir
from pydantic import BaseModel, model_validator


class Config(BaseModel):
    """
    Configuration for amrita_plugin_omikuji
    """

    omikuji_send_by_chat: bool = False  # 是否交给模型进行二次响应
    enable_omikuji: bool = True  # 是否启用
    omikuji_add_system_prompt: bool = (
        True  # 是否加入AmritaBot的系统提示(生成更符合角色设定的答案)
    )
    omikuji_use_cache: bool = True  # 是否使用语料库的缓存（LLM生成后的缓存）
    omikuji_cache_expire_days: int = (
        14  # 御神签语料缓存有效期，创建时间超过该天数之前会被清除（-1表示长期有效）
    )
    omikuji_cache_update_expire_days: int = (
        7  # 更新时间差大于这个数值就会清除缓存(-1表示不检查更新时间)
    )
    omikuji_long_cache_mode: bool = True  # 启用长期缓存模式(不会清除缓存)
    omikuji_long_cache_update: bool = True  # 仅在语料库长期模式下生效，是否自动更新语料
    omikuji_long_cache_update_days: int = 3  # 仅在语料库长期模式下生效，同一个Level和主题添加缓存内容的间隔天数(0为不更新,即使命中内容过少也会命中)
    omikuji_long_cache_update_max_count: int = (
        100  # 仅在语料库长期模式下生效，添加缓存内容的最大数量
    )

    @model_validator(mode="after")
    def check(self) -> Config:
        if self.omikuji_long_cache_update_max_count < 1:
            raise ValueError(
                "omikuji_long_cache_update_max_count must be greater than 0"
            )
        if self.omikuji_long_cache_update_days < 1:
            raise ValueError("omikuji_long_cache_update_days must be greater than 0")
        return self


def get_config() -> Config:
    return get_plugin_config(Config)


def get_cache_dir() -> Path:
    return get_plugin_cache_dir()
