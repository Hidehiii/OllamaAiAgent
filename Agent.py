from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_ollama.chat_models import ChatOllama
from langchain.agents.middleware import PIIMiddleware, SummarizationMiddleware, HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import SystemMessage, HumanMessage, AIMessage

class AgentInitInfo:
    def __init__(self,
                 modelName: str,
                 temperature: float = 0.7,
                 max_tokens: int | None = None,
                 reasoning: bool = False,
                 num_predict: int | None = None,
                 base_url: str = "http://localhost:11434"):
        self.modelName = modelName
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.reasoning = reasoning
        self.num_predict = num_predict
        self.base_url = base_url

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
        self.tools = [
            #get_time,
        ]
        # `thread_id` is a unique identifier for a given conversation.
        self.context_config = {"configurable": {"thread_id": "1"}}

        self.memory_saver = InMemorySaver()
        self.system_prompt = SystemMessage(
            content=
                """
                You are a little girl and talk like a girl.
                """
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
            input={"messages": [{"role": "user", "content": user_input}]},
            config=self.context_config
        )["messages"][-1]