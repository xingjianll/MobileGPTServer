import os
import sys
import openai
from typing import Optional


class ChatGPT:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def get_response(self, conversation: list[dict]) -> str:
        response = openai.ChatCompletion.create(model="gpt-4-1106-preview",
                                                messages=conversation)
        result = response['choices'][0]['message']
        return result
