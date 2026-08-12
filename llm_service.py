from openai import OpenAI
import streamlit as st


def get_client():
    return OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )


def ask_deepseek(messages):
    client = get_client()

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content