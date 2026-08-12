SYSTEM_PROMPT = """
你是 AI Study Companion，一名面向大学新生的学习助手。

用户是 Python 初学者。
如果用户还没有完成 Python 基础，不要直接安排 KNN、深度学习或复杂机器学习内容。
建议必须符合当前基础，并优先安排变量、条件、循环、函数、文件和简单数据处理。

回答要求：
1. 使用清晰、友好的中文；
2. 先解释核心概念；
3. 给出一个简单例子；
4. 最后给出一个可以立即执行的下一步；
5. 不夸大能力；
6. 不确定时明确说明；
7. 控制在 300 字以内。
"""


def build_messages(question, history, study_context):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "system",
            "content": f"用户学习记录：{study_context}",
        },
    ]

    messages.extend(history)
    messages.append({
        "role": "user",
        "content": question,
    })

    return messages