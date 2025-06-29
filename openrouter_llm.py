from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import requests
import os

class OpenRouterChat:
    def __init__(self, model="mistralai/mistral-7b-instruct", api_key=None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def invoke(self, messages, **kwargs):
        # Handle single string input
        if isinstance(messages, str):
            messages = [HumanMessage(content=messages)]

        formatted_messages = []
        for msg in messages:
            role = (
                "user" if isinstance(msg, HumanMessage)
                else "system" if isinstance(msg, SystemMessage)
                else "assistant"
            )
            formatted_messages.append({"role": role, "content": msg.content})

        response = requests.post(
            self.api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "http://localhost",
                "X-Title": "My Research App",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": formatted_messages,
            },
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return AIMessage(content=content)
