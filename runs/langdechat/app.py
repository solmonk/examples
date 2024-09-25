import json
import os
from typing import List

import gradio as gr
import requests

LANGDECHAT_ENDPOINT = "http://localhost:8000"

if os.environ.get("LANGDECHAT_ENDPOINT"):
    LANGDECHAT_ENDPOINT = os.environ.get("LANGDECHAT_ENDPOINT")

def format_history(history: List[str]):
    formatted = []
    print(">>>>>>>>>> History")
    print(history)
    for h in history:
        print(h)
        formatted.append({
            "role": "user",
            "content": h[0]
        })
        formatted.append({
            "role": "agent",
            "content": h[1]
        })
    return formatted

continuation_token: str = None

def query_langdechat(message: str, history: List[str]):
    global continuation_token 
    data = {
        "query": message,
        # "history": format_history(history),
        "variables": {}
    }

    if continuation_token:
        data["continuation_token"] = continuation_token

    print(">>>>>>>>>> Data")
    print(json.dumps(data))

    r = requests.post(f"{LANGDECHAT_ENDPOINT}/chat", json=data)

    if r.status_code != 200:
        print(f">>>>>>>>>> Error: {r.status_code}")
        print(r.text)
        return "Error"
    res_data = r.json()
    continuation_token = res_data["continuation_token"]
    return res_data["message"]



demo = gr.ChatInterface(
    fn=query_langdechat,
    examples=[{"text": "hello"}, {"text": "hola"}, {"text": "merhaba"}],
    title="Langdechat Test Bot",
)

port=4999
if os.environ.get("PORT"):
    port = int(os.environ.get("PORT"))

demo.launch(server_port=port)