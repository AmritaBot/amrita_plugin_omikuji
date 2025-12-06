import os
from datetime import datetime, timedelta
from typing import overload

import aiofiles
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot_plugin_orm import AsyncSession, get_session
from pydantic import BaseModel, Field
from sqlalchemy import delete, select
from typing_extensions import Self

from .config import get_cache_dir, get_config
from .models import THEME_TYPE, OmikujiData
from .sql_models import OmikujiCache as SQLOmikujiCache
from .sql_models import db_lock


class OmikujiCache(BaseModel):
    data: OmikujiData
    timestamp: datetime = Field(default_factory=datetime.now)


async def cache_omikuji(event: MessageEvent, data: OmikujiData) -> None:
    CACHE_DIR = get_cache_dir()
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = CACHE_DIR / f"{event.user_id!s}.json"
    cache = OmikujiCache(data=data)
    async with aiofiles.open(cache_file, "w", encoding="utf-8") as f:
        await f.write(cache.model_dump_json())


async def get_cached_omikuji(event: MessageEvent) -> OmikujiData | None:
    CACHE_DIR = get_cache_dir()
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = CACHE_DIR / f"{event.user_id!s}.json"
    if not cache_file.exists():
        return None
    async with aiofiles.open(cache_file, encoding="utf-8") as f:
        cache = OmikujiCache.model_validate_json(await f.read())
    if cache.timestamp.date() == datetime.now().date():
        return cache.data
    else:
        os.remove(str(cache_file))


class OmikujiCacheContent(BaseModel):
    content: str


class OmikujiCacheData(BaseModel):
    level: str
    theme: THEME_TYPE
    sections: dict[str, list[str]]
    intro: list[OmikujiCacheContent]
    maxim: list[OmikujiCacheContent]
    end: list[OmikujiCacheContent]
    divine_title: list[OmikujiCacheContent]
    sign_number: list[OmikujiCacheContent]
    created_date: str
    updated_date: str

    @overload
    @classmethod
    async def get(cls, level: str, theme: THEME_TYPE) -> Self | None: ...

    @overload
    @classmethod
    async def get(cls, level: str) -> dict[str, Self]: ...

    @classmethod
    async def get(
        cls, level: str, theme: THEME_TYPE | None = None
    ) -> Self | dict[str, Self] | None:
        async with db_lock(theme, level):
            async with get_session() as session:
                await cls._expire_cache(session=session)
                if theme:
                    stmt = select(SQLOmikujiCache).where(
                        SQLOmikujiCache.level == level,
                        SQLOmikujiCache.theme == theme,
                    )
                    result = await session.execute(stmt)
                    data = result.scalar_one_or_none()
                    if not data:
                        return None
                    return cls.model_validate(data, from_attributes=True)
                else:
                    stmt = select(SQLOmikujiCache).where(
                        SQLOmikujiCache.level == level,
                    )
                    result = await session.execute(stmt)
                    data = result.scalars().all()
                    return {
                        model.theme: cls.model_validate(model, from_attributes=True)
                        for model in data
                    }

    @classmethod
    async def cache_omikuji(cls, data: OmikujiData) -> None:
        config = get_config()

        def unique_append(ls: list[dict[str, str]], content: str):
            d = OmikujiCacheContent(content=content).model_dump()
            if d not in ls:
                ls.append(d)
            while len(d) > config.omikuji_long_cache_update_max_count:
                ls.pop(0)

        async with db_lock(data.theme, data.level):
            async with get_session() as session:
                await cls._expire_cache(session=session)
                stmt = (
                    select(SQLOmikujiCache)
                    .where(
                        SQLOmikujiCache.theme == data.theme,
                        SQLOmikujiCache.level == data.level,
                    )
                    .with_for_update()
                )
                if (
                    cache := (await session.execute(stmt)).scalar_one_or_none()
                ) is None:
                    cache = SQLOmikujiCache(
                        theme=data.theme,
                        level=data.level,
                        sections={i.name: [i.content] for i in data.sections},
                        intro=[
                            OmikujiCacheContent(content=data.sign_number).model_dump()
                        ],
                        maxim=[OmikujiCacheContent(content=data.maxim).model_dump()],
                        end=[OmikujiCacheContent(content=data.end).model_dump()],
                        divine_title=[
                            OmikujiCacheContent(content=data.divine_title).model_dump()
                        ],
                        sign_number=[
                            OmikujiCacheContent(content=data.sign_number).model_dump()
                        ],
                    )
                    session.add(cache)
                    await session.commit()
                    await session.refresh(cache)

                sections = cache.sections
                intro = cache.intro
                maxim = cache.maxim
                end = cache.end
                divine_title = cache.divine_title
                sign_number = cache.sign_number

                for i in data.sections:
                    if i.name not in sections:
                        sections[i.name] = []
                    if i.content not in sections[i.name]:
                        sections[i.name].append(i.content)

                unique_append(intro, data.intro)
                unique_append(maxim, data.maxim)
                unique_append(end, data.end)
                unique_append(divine_title, data.divine_title)
                unique_append(sign_number, data.sign_number)

                cache.intro = intro
                cache.sections = sections
                cache.maxim = maxim
                cache.end = end
                cache.divine_title = divine_title
                cache.sign_number = sign_number

                await session.commit()

    @staticmethod
    async def _expire_cache(*, session: AsyncSession) -> None:
        config = get_config()
        if not config.omikuji_long_cache_mode:
            if config.omikuji_cache_expire_days > 0:
                expire_time = datetime.now() - timedelta(
                    days=config.omikuji_cache_expire_days
                )
                await session.execute(
                    delete(SQLOmikujiCache).where(
                        SQLOmikujiCache.created_date < expire_time.strftime("%Y-%m-%d")
                    )
                )
                await session.commit()
            if config.omikuji_cache_update_expire_days > 0:
                expire_time = datetime.now() - timedelta(
                    days=config.omikuji_cache_update_expire_days
                )
                await session.execute(
                    delete(SQLOmikujiCache).where(
                        SQLOmikujiCache.updated_date < expire_time.strftime("%Y-%m-%d")
                    )
                )
                await session.commit()
