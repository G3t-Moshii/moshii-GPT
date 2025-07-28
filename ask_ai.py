# ask_ai.py

import os
import openai
import requests

def ask_ai(prompt, apis, provider="chatgpt"):
    if provider == "chatgpt":
        return ask_chatgpt(prompt, apis["chatgpt"])
    elif provider == "deepseek":
        return ask_deepseek(prompt, apis["deepseek"])
    elif provider == "together":
        return ask_togetherai(prompt, apis["together"])
    else:
        return "[AI ERROR] Unknown provider."

def ask_chatgpt(prompt, api_key):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[AI ERROR] {str(e)}"

def ask_deepseek(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[AI ERROR] {str(e)}"

def ask_togetherai(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[AI ERROR] {str(e)}"
