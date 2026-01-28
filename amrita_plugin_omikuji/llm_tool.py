import typing

from amrita.plugins.chat.API import (
    ToolContext,
    on_tools,
)
from nonebot import get_bot, logger
from nonebot.adapters.onebot.v11 import MessageEvent

from .cache import cache_omikuji, get_cached_omikuji
from .config import get_config
from .models import FUNC_DEFINTION, OmikujiData
from .utils import generate_omikuji

LEVEL = ["大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶"]


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


@on_tools(FUNC_DEFINTION, custom_run=True, strict=True)
async def omikuji(ctx: ToolContext) -> str:
    logger.info("获取御神签")
    nb_event: MessageEvent = typing.cast(MessageEvent, ctx.event.get_nonebot_event())
    is_group = hasattr(nb_event, "group_id")
    bot = get_bot(str(ctx.event._nbevent.self_id))

    if (data := await get_cached_omikuji(nb_event)) is None:
        await bot.send(
            ctx.event._nbevent,
            "轻轻摇动古老的签筒，竹签哗啦作响... 心中默念所求之事... 一支签缓缓落下。",
        )
        data = await generate_omikuji(ctx.data["theme"], is_group)
        await cache_omikuji(nb_event, data)
    if get_config().omikuji_send_by_chat:
        return data.model_dump_json()
    msg = format_omikuji(data)
    await bot.send(nb_event, msg)
    return "Generated a omikuji for user."
