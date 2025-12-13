from Agent import LocalAiAgent, AgentInitInfo
import os
import json

CONFIG_PATH = "./config.json"

def _create_agent_from_config(model_name: str, model_config: dict) -> LocalAiAgent:
    model_info = model_config.get(model_name, {}).get("init_info", {})
    return LocalAiAgent(AgentInitInfo(
        modelName=model_info.get("modelName", model_name),
        temperature=model_info.get("temperature", 0.7),
        max_tokens=model_info.get("max_tokens", None),
        reasoning=model_info.get("reasoning", False),
        num_predict=model_info.get("num_predict", None),
        base_url=model_info.get("base_url", "http://localhost:11434"),
        tool_use=model_info.get("tool_use", False),
        sys_prompt=model_info.get("sys_prompt", "")
    ))

def select_agent() -> LocalAiAgent:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            model_config = json.load(f).get("models", {})
    else:
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    print("Select an AI Agent:")
    while True:
        print("1. llama3.2:3b (can not use tools)")
        print("2. deepseek-r1:8b (can not use tools)")
        print("3. granite3-dense (can use tools)")
        print("4. granite3.2-vision (can use tools and images)")
        print("5. llama3-groq-tool-use (can use tools)")
        print("6. phi4-mini (can use tools)")
        user_selection = input("Enter the number of the agent you want to use: ")
        if user_selection == "1":
            return _create_agent_from_config("llama3.2:3b", model_config)
        elif user_selection == "2":
            return _create_agent_from_config("deepseek-r1:8b", model_config)
        elif user_selection == "3":
            return _create_agent_from_config("granite3-dense", model_config)
        elif user_selection == "4":
            return _create_agent_from_config("granite3.2-vision", model_config)
        elif user_selection == "5":
            return _create_agent_from_config("llama3-groq-tool-use", model_config)
        elif user_selection == "6":
            return _create_agent_from_config("phi4-mini", model_config)
        else:
            print("Invalid selection. Please choose a number between 1 and 6.")