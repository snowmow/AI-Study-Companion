from prompts import SYSTEM_PROMPT, build_messages
from database import (
    add_record,
    get_records,
    initialize_database,
    record_exists,
)
from database import get_recent_summary
from llm_service import ask_deepseek

import streamlit as st
try:
    deepseek_api_key = st.secrets["DEEPSEEK_API_KEY"]
    st.sidebar.success("DeepSeek 配置已读取")
except KeyError:
    deepseek_api_key = None
    st.sidebar.error("未找到 DeepSeek API Key")

def get_weekly_study_context():
    summary = get_recent_summary(7)

    if not summary["records"]:
        return "用户近 7 天没有保存学习记录。"

    subject_text = "；".join(
        f"{subject}：{minutes} 分钟"
        for subject, minutes in summary["subject_minutes"].items()
    )

    return (
        f"用户近 7 天共有 {len(summary['records'])} 条学习记录，"
        f"累计学习 {summary['total_minutes']} 分钟。"
        f"各主题学习时长：{subject_text}。"
        "请基于这些真实数据评价学习情况，指出一个优点、一个可改进点，"
        "并给出一个具体且可执行的下一步建议。"
    )

st.set_page_config(page_title="AI 学习伙伴", page_icon="📚")
initialize_database()
def study_level(minutes, python_level):
    if minutes < 30:
        return f"{python_level}，建议先完成一个 20 分钟的小任务。"
    elif python_level == "刚开始学习":
        return "你已经学习了一段时间，建议先巩固 Python 基础语法。"
    elif minutes < 90:
        return "学习时间不错，可以继续练习一个小程序。"
    else:
        return "学习时间较长，记得适当休息，再总结今天的学习内容。"

def demo_reply(question: str) -> str:
    """暂时代替真实 AI 的本地回复，后续会换成大模型接口。"""
    text = question.lower()

    if "函数" in question or "function" in text:
        return (
            "Python 函数可以理解成一段可重复使用的小程序。\n\n"
            "例如：`def say_hello():` 定义一个叫 `say_hello` 的函数，"
            "之后调用 `say_hello()` 就能重复执行其中的内容。\n\n"
            "下一步：试着写一个 `add(a, b)` 函数，让它返回两个数字的和。"
        )
    if "计划" in question or "怎么学" in question:
        return (
            "可以先从一个小而明确的计划开始：\n"
            "1. 本周学习 Python 的变量、条件判断和函数；\n"
            "2. 每天练习 30～60 分钟；\n"
            "3. 周末做一个小程序，例如待办事项清单。\n\n"
            "你现在最想学习 Python、AI，还是其他内容？"
        )
    if "神经网络" in question:
        return (
            "神经网络是一种从数据中学习规律的模型。它由许多简单的计算单元连接而成，"
            "通过不断调整连接参数来改善预测结果。\n\n"
            "对初学者来说，先掌握 Python 基础和简单的数据处理，比直接深入公式更合适。"
        )
    if "循环" in question:
        return (
            "Python 中的 for 循环用于重复处理一组内容。\n\n"
            "例如：`for task in daily_tasks:` 会依次取出任务列表中的每一项。\n\n"
            "下一步：尝试把你自己的三个学习任务放进列表，再用 for 循环显示它们。"
        )
    return (
        f"我收到了你的问题：“{question}”。\n\n"
        "目前这是本地演示回复。之后接入大模型后，我会根据你的具体问题给出更准确的解答。"
    )


st.subheader("近 7 天学习总结")

if st.button("生成近 7 天总结"):
    summary = get_recent_summary(7)

    if not summary["records"]:
        st.info("近 7 天还没有学习记录。")
    else:
        st.write(
            f"近 7 天累计学习："
            f"{summary['total_minutes']} 分钟"
        )

        st.write("各主题学习时间：")

        for subject, minutes in summary["subject_minutes"].items():
            st.write(f"- {subject}：{minutes} 分钟")

        st.subheader("近 7 天学习记录")

        display_records = [
            {
                "日期": record["study_date"],
                "学习主题": record["subject"],
                "学习时长（分钟）": record["duration_minutes"],
                "Python基础": record["python_level"],
                "学习心得": record["note"],
            }
            for record in summary["records"]
        ]

        st.dataframe(
            display_records,
            hide_index=True,
        )

st.title("我的第一个 Python 网页应用")
student_name = "snow"
st.write("欢迎你，", student_name)
study_minutes = st.number_input(
    "今天学习了多少分钟？",
    min_value=0,
    max_value=600,
    value=90,
    step=10,
)

python_level = st.selectbox(
    "你的python基础是？",
    ["刚开始学习","了解基础语法","能写简单程序"],
)

if st.button("生成今日学习建议"):
    st.write("你当前的python基础：", python_level)
    suggestion = study_level(study_minutes, python_level)
    st.success(suggestion)

st.write("今天计划学习", study_minutes, "分钟。")
st.write("换算成小时：", study_minutes / 60)
favorite_subject = st.text_input(
    "你目前最想学习什么？",
    placeholder="例如：Python、AI、英语",
)

if favorite_subject:
    st.write("你的学习方向是：", favorite_subject)
st.write("这是你的 AI 学习伙伴。")
st.caption("面向大学新生的学习问答与规划助手 · 演示版")
st.subheader("今日学习任务")

daily_tasks = [
    "复习python变量",
    "练习if判断",
    "完成一个函数练习",
    "总结今天的学习内容",
]

for task in daily_tasks:
    st.write("- ", task)
st.write("今天共有", len(daily_tasks), "项任务。")

completed = st.checkbox("我已完成今天的学习任务")

if completed:
    st.success("太好了！记得简单总结一下今天学到了什么。")

study_date = st.date_input("学习日期")
st.write("记录日期：", study_date)

study_note = st.text_area(
    "记录今天学到了什么",
    placeholder="例如：我理解了函数可以接收参数并返回结果。",
)
if study_note:
    st.info("你记录的是：" + study_note)
study_record = {
    "日期": str(study_date),
    "学习主题": favorite_subject,
    "学习时长（分钟）": study_minutes,
    "Python 基础": python_level,
    "学习心得": study_note,
}

if st.button("预览学习记录"):
    st.write(study_record)

if st.button("保存学习记录", type="primary"):
    if not favorite_subject.strip():
        st.warning("请填写学习主题后再保存。")
    elif not study_note.strip():
        st.warning("请填写学习心得后再保存。")
    else:
        if record_exists(
            str(study_date),
            favorite_subject.strip(),
            study_minutes,
            python_level,
            study_note.strip(),
        ):
            st.warning("这条学习记录已经保存过了。")
        else:
            add_record(
                str(study_date),
                favorite_subject.strip(),
                study_minutes,
                python_level,
                study_note.strip(),
            )
            st.success("学习记录已保存到 SQLite 数据库。")
       
with st.sidebar:
    st.header("你可以问我")
    st.write("- 什么是 Python 函数？")
    st.write("- 我应该怎么学习 AI？")
    st.write("- 解释一下神经网络")
    if st.button("清空对话"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "你好！我是你的 AI 学习伙伴。今天想学习什么？",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("输入你的学习问题"):
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    try:
        history = st.session_state.messages[:-1]

        messages = build_messages(
            question=question,
            history=history,
            study_context=get_weekly_study_context(),
        )

        answer = ask_deepseek(messages)

    except Exception:
        answer = "暂时无法连接 DeepSeek，请检查网络或 API 配置。"

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)

st.subheader("历史学习记录")

records = get_records()

if records:
    total_minutes = 0

    for record in records:
        total_minutes += record["学习时长（分钟）"]

    st.write("累计学习时长：", total_minutes, "分钟")
    average_minutes = total_minutes / len(records)
    st.write("平均每次学习时长：", average_minutes, "分钟")
    subject_minutes = {}

    for record in records:
        subject = record["学习主题"]
        minutes = record["学习时长（分钟）"]

        if subject not in subject_minutes:
            subject_minutes[subject] = 0

        subject_minutes[subject] += minutes

    st.write("各学习主题的时长：")

    for subject, minutes in subject_minutes.items():
        st.write("-", subject, "：", minutes, "分钟")
    most_studied_subject = max(subject_minutes, key=subject_minutes.get)
    most_studied_minutes = subject_minutes[most_studied_subject]

    st.write(
        "目前投入时间最多的主题是：",
        most_studied_subject,
        "，共",
        most_studied_minutes,
        "分钟。",
    )
    st.dataframe(records)
else:
    st.info("暂无已保存的学习记录。")