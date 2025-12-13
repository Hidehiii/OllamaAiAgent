from .Agent import LocalAiAgent, AgentInitInfo
import os
import json

CONFIG_PATH = "./config.json"

def select_agent() -> LocalAiAgent:
    print("Select an AI Agent:")
    print("1. llama3.2:3b (can not use tools)")
    print("2. deepseek-r1:8b (can not use tools)")