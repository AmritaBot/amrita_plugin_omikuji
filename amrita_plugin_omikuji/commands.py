import random
import typing

from amrita.plugins.menu import MatcherData
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.params import CommandArg

from .cache import cache_omikuji, get_cached_omikuji
from .config import get_config
from .models import OMIKUJI_THEMES, THEME_TYPE
from .utils import format_omikuji, generate_omikuji

omikuji = on_command(
    "omikuji",
    aliases={"御神签", "抽签"},
    priority=10,
    block=True,
    rule=lambda: get_config().enable_omikuji,
    state=MatcherData(
        name="omikuji", description="抽御神签", usage="/omikuji [主题]"
    ).model_dump(),
)


@omikuji.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    if args:
        theme = args.extract_plain_text()
        if theme not in OMIKUJI_THEMES:
            await omikuji.finish(
                f"当前可用御神签主题：{''.join(i + ',' for i in OMIKUJI_THEMES)}"
            )
    else:
        theme = random.choice(list(OMIKUJI_THEMES))
    theme = typing.cast(THEME_TYPE, theme)
    is_group = isinstance(event, GroupMessageEvent)
    if (data := await get_cached_omikuji(event)) is None:
        data = await generate_omikuji(theme, is_group)
        await cache_omikuji(event, data)
    msg = format_omikuji(data)
    await omikuji.finish(msg)
