from langchain.agents import create_agent
from langchain_ollama.chat_models import ChatOllama
from langchain.agents.middleware import PIIMiddleware, SummarizationMiddleware, HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import SystemMessage, HumanMessage, AIMessage
import ToolList

class AgentInitInfo:
    def __init__(self,
                 modelName: str,
                 temperature: float = 0.7,
                 max_tokens: int | None = None,
                 reasoning: bool = False,
                 num_predict: int | None = None,
                 base_url: str = "http://localhost:11434",
                 tool_use: bool = False,
                 sys_prompt: str = ""):
        self.modelName = modelName
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.reasoning = reasoning
        self.num_predict = num_predict
        self.base_url = base_url
        self.tool_use = tool_use
        self.sys_prompt = sys_prompt

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
            checkpointer=self.memory_saver,
            middleware=self.middle_ware
        )

    def invoke(self, user_input: str):
        return self.agent.invoke(
            input=self._convert_to_messages(user_input=user_input),
            config=self.context_config
        )

    def stream_messages(self, user_input: str):
        return self.agent.stream(
            input=self._convert_to_messages(user_input=user_input),
            config=self.context_config,
            stream_mode="messages"
        )

    def _convert_to_messages(self, user_input: str, role: str = "user") -> dict:
        return {
            "messages": [
                {"role": role, "content": user_input}
            ]
        }