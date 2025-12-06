from __future__ import annotations

import asyncio
from datetime import datetime
from functools import lru_cache

from nonebot_plugin_orm import Model
from sqlalchemy import JSON, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .models import THEME_TYPE


@lru_cache(1024)
def db_lock(*args, **kwargs):
    return asyncio.Lock()


class OmikujiCache(Model):
    __tablename__ = "omikuji_cache"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level: Mapped[str] = mapped_column(String(64), nullable=False)
    theme: Mapped[THEME_TYPE] = mapped_column(String(64), nullable=False)
    sections: Mapped[dict[str, list[str]]] = mapped_column(
        JSON,
        default={},
        nullable=False,
    )  # {"板块":["板块内容"]}
    intro: Mapped[list[dict[str, str]]] = mapped_column(
        JSON,
        default=[],
        nullable=False,
    )  # [{"content":"内容"}]
    maxim: Mapped[list[dict[str, str]]] = mapped_column(
        JSON,
        default=[],
        nullable=False,
    )
    end: Mapped[list[dict[str, str]]] = mapped_column(
        JSON,
        default=[],
        nullable=False,
    )
    divine_title: Mapped[list[dict[str, str]]] = mapped_column(
        JSON,
        default=[],
        nullable=False,
    )
    sign_number: Mapped[list[dict[str, str]]] = mapped_column(
        JSON,
        default=[],
        nullable=False,
    )
    created_date: Mapped[str] = mapped_column(
        String(30), default=lambda: datetime.now().strftime("%Y-%m-%d"), nullable=False
    )
    updated_date: Mapped[str] = mapped_column(
        String(30),
        default=lambda: datetime.now().strftime("%Y-%m-%d"),
        onupdate=lambda: datetime.now().strftime("%Y-%m-%d"),
        nullable=False,
    )
    __table_args__ = (
        Index("ix_omikuji_cache_level_theme", "level", "theme"),
        UniqueConstraint("level", "theme", name="uq_omikuji_cache_level_theme"),
    )
