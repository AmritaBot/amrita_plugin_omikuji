from __future__ import annotations

import random
from typing import Literal

from amrita.plugins.chat.API import (
    FunctionDefinitionSchema,
    FunctionParametersSchema,
    FunctionPropertySchema,
    ToolFunctionSchema,
)
from pydantic import BaseModel, Field

LEVEL = ["大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶"]
OMIKUJI_THEMES = [
    "综合运势",  # 默认选项
    "恋爱姻缘",  # 情感
    "学业考试",  # 学习
    "事业财运",  # 工作
    "健康平安",  # 健康
    "人际和谐",  # 关系
    "旅行出行",  # 出行
    "樱花时节",  # 季节/文化
    "星幽秘境",  # 奇幻
    "灵感创意",  # 创作
]
THEME_TYPE = Literal[
    "综合运势",
    "恋爱姻缘",
    "学业考试",
    "事业财运",
    "健康平安",
    "人际和谐",
    "旅行出行",
    "樱花时节",
    "星幽秘境",
    "灵感创意",
]


def random_level() -> str:
    return random.choice(LEVEL)


class OmikujiSections(BaseModel):
    name: str
    content: str


class OmikujiData(BaseModel):
    level: str = Field(default_factory=random_level)
    theme: THEME_TYPE
    sign_number: str
    divine_title: str
    sections: list[OmikujiSections]
    maxim: str
    intro: str
    end: str


OMIKUJI_SCHEMA_META = ToolFunctionSchema(
    strict=True,
    type="function",
    function=FunctionDefinitionSchema(
        name="omikuji_content",
        description="获取御神签签文",
        parameters=FunctionParametersSchema(
            type="object",
            properties={
                "theme": FunctionPropertySchema(
                    type="string",
                    description="御神签主题",
                    enum=OMIKUJI_THEMES,
                ),
                "sign_number": FunctionPropertySchema(
                    type="string",
                    description="御神签编号(随机中文大写数字)",
                ),
                "divine_title": FunctionPropertySchema(
                    type="string",
                    description="神签标题/天启名（2-4字奇幻风格名称）",
                ),
                "sections": FunctionPropertySchema(
                    type="array",
                    items=FunctionPropertySchema(
                        type="object",
                        properties={
                            "name": FunctionPropertySchema(
                                type="string", description="分类名称"
                            ),
                            "content": FunctionPropertySchema(
                                type="string", description="分类的预言内容（1～2句话）"
                            ),
                        },
                        description="签文主体",
                        required=["name", "content"],
                    ),
                    description="签文主体",
                    maxItems=8,
                    minItems=4,
                    uniqueItems=True,
                ),
                "maxim": FunctionPropertySchema(
                    type="string", description="一句箴言/和歌（结尾注明出处）"
                ),
                "intro": FunctionPropertySchema(
                    type="string",
                    description="主题引入(不包含引号)：e.g. '「欢迎来到古树根下的祠堂。异界之风正为你捎来命运的启示…」\n'",
                ),
                "end": FunctionPropertySchema(
                    type="string",
                    description="主题总结(不包含引号)",
                ),
            },
            required=[
                "theme",
                "sign_number",
                "divine_title",
                "sections",
                "maxim",
                "intro",
            ],
        ),
    ),
)

FUNC_META = ToolFunctionSchema(
    strict=True,
    function=FunctionDefinitionSchema(
        name="omikuji",
        description="抽取一个御神签",
        parameters=FunctionParametersSchema(
            type="object",
            properties={
                "theme": FunctionPropertySchema(
                    type="string",
                    description="御神签主题（如果包含不良内容则随机选择）",
                )
            },
            required=["theme"],
        ),
    ),
)
