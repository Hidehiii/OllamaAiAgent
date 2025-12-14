from langchain.agents import create_agent
from langchain_ollama.chat_models import ChatOllama
from langchain.agents.middleware import PIIMiddleware, SummarizationMiddleware, HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import SystemMessage, HumanMessage, AIMessage
import ToolList
from typing import Literal

AgentOperateEnv = Literal["CommandLine", "LanggraphChatUi"]

class AgentInitInfo:
    def __init__(self,
                 modelName: str,
                 temperature: float = 0.7,
                 max_tokens: int | None = None,
                 reasoning: bool = False,
                 num_predict: int | None = None,
                 base_url: str = "http://localhost:11434",
                 tool_use: bool = False,
                 sys_prompt: str = "",
                 agent_operate_env: AgentOperateEnv = "LanggraphChatUi"):
        self.modelName = modelName
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.reasoning = reasoning
        self.num_predict = num_predict
        self.base_url = base_url
        self.tool_use = tool_use
        self.sys_prompt = sys_prompt
        self.agent_operate_env = agent_operate_env

class LocalAiAgent:
    def __init__(self, init_info: AgentInitInfo):
        self.model = ChatOllama(
            model=init_info.modelName,
            validate_model_on_init=True,
            temperature=init_info.temperature,
            max_tokens=init_info.max_tokens,
            reasoning=init_info.reasoning,
            num_predict=init_info.num_predict,
            base_url=init_info.base_url,
        )
        self.tool_use = init_info.tool_use
        self.tools = ToolList.TOOL_LIST if self.tool_use else []
        # `thread_id` is a unique identifier for a given conversation.
        self.context_config = {"configurable": {"thread_id": "1"}}

        self.memory_saver = InMemorySaver()
        self.system_prompt = SystemMessage(
            content=init_info.sys_prompt
        )
        self.middle_ware = [
            PIIMiddleware(pii_type="ip"),
            SummarizationMiddleware(model=self.model),
            HumanInTheLoopMiddleware(interrupt_on={"send_email": {"allowed_decisions": ["approve", "reject"]}}),
        ]
        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.system_prompt,
            checkpointer=self.memory_saver if init_info.agent_operate_env == "CommandLine" else None,
            middleware=self.middle_ware
        )

    def get_agent(self):
        return self.agent

    def invoke(self, user_input: str, img_input: list[str] = None):
        return self.agent.invoke(
            input=self._convert_to_messages(user_input=user_input, img_input=img_input),
            config=self.context_config
        )

    def stream_messages(self, user_input: str, img_input: list[str] = None):
        return self.agent.stream(
            input=self._convert_to_messages(user_input=user_input, img_input=img_input),
            config=self.context_config,
            stream_mode="messages"
        )

    def _convert_to_messages(self, user_input: str, img_input: list[str], role: str = "user") -> dict:
        return {
            "messages": [
                {
                    "role": role,
                    "content": user_input,
                    "images": img_input if img_input is not None else []
                }
            ]
        }