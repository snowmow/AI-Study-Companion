# AI Study Companion

一个面向大学新生的 AI 学习助手，提供学习问答、学习记录管理、近 7 天学习总结和个性化学习建议。

## 功能

- 基于 DeepSeek 大语言模型的学习问答
- 保留当前会话的聊天上下文
- 保存学习日期、主题、时长、基础水平和学习心得
- 使用 SQLite 持久化保存学习记录
- 防止完全相同的学习记录重复保存
- 展示全部历史学习记录和基础统计
- 统计近 7 天学习时长与主题分布
- 基于近 7 天真实学习记录生成个性化建议

## 技术栈

- Python
- Streamlit
- DeepSeek API
- OpenAI Python SDK
- SQLite

## 项目结构

```text
AI-Study-Companion/
├── app.py             # Streamlit 页面和用户交互
├── database.py        # SQLite 数据库操作
├── llm_service.py     # DeepSeek API 调用
├── prompts.py         # AI 角色设定与消息构造
├── requirements.txt   # 项目依赖
└── .gitignore         # Git 忽略规则