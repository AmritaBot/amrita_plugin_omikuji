import json
import random
from copy import deepcopy
from datetime import datetime, timedelta

from amrita.plugins.chat.config import (
    config_manager,
)
from amrita_core.libchat import tools_caller
from amrita_core.types import Message
from nonebot import logger

from .cache import OmikujiCacheData
from .config import get_config
from .models import (
    OMIKUJI_SCHEMA_META,
    THEME_TYPE,
    OmikujiData,
    OmikujiSections,
    random_level,
)


async def _hit_cache_omikuji(
    theme: THEME_TYPE,
    level: str = "",
) -> OmikujiData | None:
    if cache := await OmikujiCacheData.get(level, theme):
        if cache.updated_date < (
            datetime.now() - timedelta(days=get_config().omikuji_cache_expire_days)
        ).strftime("%Y-%m-%d"):
            logger.debug(f"{theme}/{level} cache expired!")
            return
        logger.debug(f"{theme}/{level} cache hit!")
        keys = list(cache.sections.keys())
        random.shuffle(keys)
        sections = [
            OmikujiSections(name=k, content=random.choice(cache.sections[k]))
            for k in keys
        ]
        if len(sections) < 4:
            return
        while len(sections) > 8:
            sections.pop()

        model = OmikujiData(
            level=level,
            theme=theme,
            sections=sections,
            sign_number=random.choice([i.content for i in cache.sign_number]),
            intro=random.choice([i.content for i in cache.intro]),
            divine_title=random.choice([i.content for i in cache.divine_title]),
            maxim=random.choice([i.content for i in cache.maxim]),
            end=random.choice([i.content for i in cache.end]),
        )
        return model


async def generate_omikuji(
    theme: THEME_TYPE,
    is_group: bool = False,
    level: str | None = None,
) -> OmikujiData:
    config = get_config()
    level = level or random_level()
    if config.omikuji_use_cache:
        if cache := await _hit_cache_omikuji(theme, level):
            return cache
    logger.debug(f"theme: {theme}, level: {level} Cache miss")
    system_prompt = Message.model_validate(
        deepcopy(
            config_manager.group_train if is_group else config_manager.private_train
        )
    )
    system_prompt["content"] += "\n你现在需要结合你的角色设定生成御神签。"
    user_prompt = Message(
        role="user",
        content=f"御神签的运势是：'{level}'\n现在生成一张主题为：'{theme}'的御神签",
    )
    msg_input = [system_prompt, user_prompt]
    data = await tools_caller(
        messages=msg_input, tools=[OMIKUJI_SCHEMA_META], tool_choice="required"
    )
    assert data.tool_calls
    args = json.loads(data.tool_calls[0].function.arguments)
    args["level"] = level
    args["theme"] = theme
    model = OmikujiData.model_validate(args)
    if level:
        model.level = level
    if config.omikuji_use_cache:
        await OmikujiCacheData.cache_omikuji(model)
    return model


def format_omikuji(data: OmikujiData, user_name: str | None = ""):
    ln = "\n"
    msg = f"""{data.intro}
{(user_name + "，" if user_name else "")}你的签上刻了什么？

＝＝＝ 御神签 第{data.sign_number} ＝＝＝
✨ 天启：{data.divine_title}
🌸 运势：{data.level} - {data.theme}

{"".join(f"▫ {section.name}{ln}{section.content}{ln}" for section in data.sections)}

⚖ 真言偈：{data.maxim}

{data.end}
"""
    return msg
