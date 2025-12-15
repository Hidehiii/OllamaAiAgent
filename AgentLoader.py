from Agent import LocalAiAgent, AgentInitInfo
import os
import json
from typing import Literal
from Agent import AgentOperateEnv

CONFIG_PATH = "./config.json"

def _create_agent_from_config(model_name: str, config: dict, op_env: AgentOperateEnv) -> LocalAiAgent:
    if "models" not in config or model_name not in config["models"] or "init_info" not in config["models"][model_name]:
        return None
    model_info = config.get("models", {}).get(model_name, {}).get("init_info", {})
    return LocalAiAgent(AgentInitInfo(
        modelName=model_info.get("modelName", model_name),
        temperature=model_info.get("temperature", 0.7),
        max_tokens=model_info.get("max_tokens", None),
        reasoning=model_info.get("reasoning", False),
        num_predict=model_info.get("num_predict", None),
        base_url=model_info.get("base_url", "http://localhost:11434"),
        tool_use=model_info.get("tool_use", False),
        sys_prompt=config.get("sys_prompt", ""),
        agent_operate_env=op_env,
    ))

def create_agent(op_env: AgentOperateEnv) -> LocalAiAgent:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    else:
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    if op_env == "CommandLine":
        if "commandline_model" not in config:
            raise ValueError("commandline_model not specified in config")
        model_name = config["commandline_model"]
    elif op_env == "LanggraphChatUi":
        if "langgraph_chat_ui_model" not in config:
            raise ValueError("langgraph_chat_ui_model not specified in config")
        model_name = config["langgraph_chat_ui_model"]
    else:
        raise ValueError(f"Unsupported operation environment: {op_env}")
    agent = _create_agent_from_config(model_name, config, op_env)
    return agent