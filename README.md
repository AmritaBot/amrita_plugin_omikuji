<div align="center">
  <a href="https://github.com/JohnRichard4096/amrita_plugin_omikuji/">
    <img src="https://github.com/user-attachments/assets/b5162036-5b17-4cf4-b0cb-8ec842a71bc6" width="200" alt="omikuji Logo">
  </a>
  <h1>Omikuji</h1>
  <h3>适用于AmritaBot的御神签插件！</h3>

  <p>
    <a href="https://pypi.org/project/nonebot-plugin-omikuji/">
      <img src="https://img.shields.io/pypi/v/nonebot-plugin-omikuji?color=blue&style=flat-square" alt="PyPI Version">
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/python-3.10+-blue?logo=python&style=flat-square" alt="Python Version">
    </a>
    <a href="https://nonebot.dev/">
      <img src="https://img.shields.io/badge/nonebot2-2.4.3+-blue?style=flat-square" alt="NoneBot Version">
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/github/license/AmritaBot/amrita_plugin_omikuji?style=flat-square" alt="License">
    </a>
    <a href="https://qm.qq.com/q/5URbtujxx6">
      <img src="https://img.shields.io/badge/QQ%E7%BE%A4-1006893368-blue?style=flat-square" alt="QQ Group">
    </a>
  </p>
</div>

## 🌸 简介

**Omikuji（御神签）** 是一款基于大型语言模型（LLM）的 [NoneBot2](https://nonebot.dev/) 插件，专为 [AmritaBot](https://github.com/AmritaBot/Amrita) 框架设计。该插件为用户提供传统日本神社抽签体验的现代化数字版本，通过 AI 生成个性化、富有文化氛围的签文。

御神签（おみくじ）是日本神道教中一种传统的占卜方式，参拜者在神社或寺庙中摇动签筒，随机抽取一支签，上面写着对未来的预言或建议。本插件将这一传统文化与现代 AI 技术相结合，每次抽取都会根据主题和运势等级生成独特的签文内容。

### 🌟 特性

- **AI 驱动签文生成**：利用大型语言模型生成富有创意和文化内涵的签文
- **多样化主题**：支持多个主题，包括综合运势、恋爱姻缘、学业考试、事业财运等
- **智能缓存系统**：内置缓存机制，提高响应速度并减少 API 调用
- **丰富的运势等级**：从大吉到大凶共 7 个等级，增加占卜体验的真实感
- **灵活配置**：支持多种配置选项，可根据需求调整插件行为
- **多平台支持**：基于 NoneBot2 开发，支持多种聊天平台

## 🚀 安装

### 环境要求

- Python 3.10+
- NoneBot2 2.4.3+
- AmritaBot 框架
- 支持的 LLM 服务（如 OpenAI、Anthropic 等）

### 使用 Amrita CLI 安装

```shell
amrita plugin install amrita_plugin_omikuji
```

### 使用 uv 安装

```shell
uv add nonebot-plugin-omikuji
```

## ⚙️ 配置

在项目的 `.env` 文件中添加以下配置项：

```env
# 是否启用御神签插件（默认：True）
ENABLE_OMIKUJI=true

# 是否交给模型进行二次响应（默认：False）
OMIKUJI_SEND_BY_CHAT=false

# 是否加入AmritaBot的系统提示（默认：True）
OMIKUJI_ADD_SYSTEM_PROMPT=true

# 是否使用语料库的缓存（默认：True）
OMIKUJI_USE_CACHE=true

# 御神签语料缓存有效期（天），创建时间超过该天数之前会被清除（-1表示长期有效）（默认：14）
OMIKUJI_CACHE_EXPIRE_DAYS=14

# 更新时间差大于这个数值就会清除缓存（-1表示不检查更新时间）（默认：7）
OMIKUJI_CACHE_UPDATE_EXPIRE_DAYS=7

# 启用长期缓存模式（不会清除缓存）（默认：True）
OMIKUJI_LONG_CACHE_MODE=true

# 仅在语料库长期模式下生效，是否自动更新语料（默认：True）
OMIKUJI_LONG_CACHE_UPDATE=true

# 仅在语料库长期模式下生效，同一个Level和主题添加缓存内容的间隔天数（0为不更新）（默认：3）
OMIKUJI_LONG_CACHE_UPDATE_DAYS=3

# 仅在语料库长期模式下生效，添加缓存内容的最大数量（默认：100）
OMIKUJI_LONG_CACHE_UPDATE_MAX_COUNT=100
```

## 🎯 使用方法

### 命令触发

1. **随机主题抽签**：

   ```
   /omikuji
   ```

2. **指定主题抽签**：

   ```
   /omikuji <主题>
   ```

   支持的主题包括：

   - 综合运势
   - 恋爱姻缘
   - 学业考试
   - 事业财运
   - 健康平安
   - 人际和谐
   - 旅行出行
   - 樱花时节
   - 星幽秘境
   - 灵感创意

3. **示例**：
   ```
   /omikuji 恋爱姻缘
   ```

### 别名触发

也可以使用以下别名触发抽签：

- `/御神签`
- `/抽签`

### 聊天触发

在启用了 AmritaBot 的环境中，也可以通过自然语言触发，例如：

- "我想抽个签"
- "给我来个御神签"

## 🧠 工作原理

1. 用户触发抽签命令或通过聊天触发
2. 插件根据主题和随机运势等级生成请求
3. 调用配置的 LLM 服务生成符合要求的签文内容
4. 将生成的签文按照传统御神签格式进行排版
5. 返回给用户完整的签文体验

签文通常包括：

- 签文编号
- 天启名称
- 运势等级和主题
- 多个分类的详细预言
- 箴言/和歌
- 主题引入和总结

## 📁 缓存机制

为了提高响应速度和减少 API 调用，插件实现了多层缓存机制：

1. **短期缓存**：临时存储用户最近一次抽签结果
2. **语料库缓存**：存储已生成的签文内容，按主题和运势等级分类
3. **长期缓存**：可配置的长期存储模式，保留优质签文内容

缓存内容会根据配置的过期时间自动清理和更新。

## 🤝 依赖

- [nonebot2](https://github.com/nonebot/nonebot2)
- [Amrita](https://github.com/AmritaBot/Amrita)
- [nonebot-adapter-onebot](https://github.com/nonebot/adapter-onebot)
- [nonebot-plugin-localstore](https://github.com/nonebot/nonebot-plugin-localstore)
- [nonebot-plugin-orm](https://github.com/nonebot/nonebot-plugin-orm)
- [aiofiles](https://github.com/Tinche/aiofiles)

## 📄 许可证

本项目使用 [GPL-3.0](./LICENSE) 许可证。

## 🙏 鸣谢

特别感谢以下项目的贡献者：

- [NoneBot2](https://github.com/nonebot/nonebot2)
- [Amrita](https://github.com/AmritaBot/Amrita)
- [nonebot-plugin-suggarchat](https://github.com/LiteSuggarDEV/nonebot-plugin-suggarchat)
