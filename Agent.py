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
            PIIMiddleware(pii_type="email_address"),
            PIIMiddleware(pii_type="phone_number"),
            PIIMiddleware(pii_type="credit_card"),
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
        """
        Get the underlying agent instance.
        :return:  The agent instance.
        """
        return self.agent

    def invoke(self,
               user_input: str,
               img_url: list[str] | str = None,
               img_base64: list[str] | str = None,
               img_base64_type: list[str] | str = None):
        """
        Invoke the agent with user input and optional images.
        The agent reply will be returned as a whole.
        :param user_input: The str input from the user.
        :param img_url:  The image URL(s).
        :param img_base64:  The image data in base64 format.
        :param img_base64_type:  The image type(s) corresponding to img_base64, e.g., "png", "jpeg".
        :return:  The agent's response.
        """
        return self.agent.invoke(
            input=self._convert_to_messages(user_input=user_input,
                                            img_url=img_url,
                                            img_base64=img_base64,
                                            img_base64_type=img_base64_type),
            config=self.context_config
        )

    def stream_messages(self,
                        user_input: str,
                        img_url: list[str] | str = None,
                        img_base64: list[str] | str = None,
                        img_base64_type: list[str] | str = None):
        """
        Stream the agent's response message by message.(Word by word)
        The agent reply will be returned as a generator.
        :param user_input:  The str input from the user.
        :param img_url:  The image URL(s).
        :param img_base64:  The image data in base64 format.
        :param img_base64_type:  The image type(s) corresponding to img_base64, e.g., "png", "jpeg".
        :return:  A generator yielding the agent's response messages.
        """
        return self.agent.stream(
            input=self._convert_to_messages(user_input=user_input,
                                            img_url=img_url,
                                            img_base64=img_base64,
                                            img_base64_type=img_base64_type),
            config=self.context_config,
            stream_mode="messages"
        )

    def _convert_to_messages(self,
                             user_input: str,
                             img_url: list[str] | str,
                             img_base64: list[str] | str,
                             img_base64_type: list[str] | str,
                             role: str = "user") -> dict:
        """
        Convert user input and images to message format.
        :param user_input:  The str input from the user.
        :param img_url:  The image URL(s).
        :param img_base64:  The image data in base64 format.
        :param img_base64_type:  The image type(s) corresponding to img_base64, e.g., "png", "jpeg".
        :param role:  Role of the message, e.g., "user" or "assistant".
        :return:  Message dict containing user input and images.
        """
        msg = {
            "messages": [
                {"role": role, "content": [{"type": "text", "text": user_input}]}
            ]
        }
        if img_url is not None:
            img_msg = self._convert_image_url_to_message(img_url=img_url, role=role)
            msg["messages"].append(img_msg)
        if img_base64 is not None and img_base64_type is not None:
            img_msg = self._convert_image_base64_to_message(img_base64=img_base64, img_base64_type=img_base64_type, role=role)
            msg["messages"].append(img_msg)
        return msg

    def _convert_image_url_to_message(self,
                                      img_url: list[str] | str,
                                      role: str) -> dict:
        """
        Convert image URL to message format.
        :param img_url:  The image URL(s).
        :param role:  Role of the message, e.g., "user" or "assistant".
        :return:  Message dict containing the image URL(s).
        """
        img_msgs = []
        if isinstance(img_url, str):
            img_msgs.append({"type": "image_url", "image_url": img_url})
            return {"role": role, "content": img_msgs}
        else:
            for img_url in img_url:
                img_msgs.append({"type": "image_url", "image_url": img_url})
            return {"role": role, "content": img_msgs}

    def _convert_image_base64_to_message(self,
                                         img_base64: list[str] | str,
                                         img_base64_type: list[str] | str,
                                         role: str) -> dict:
        """
        Convert base64 image to message format.
        :param img_base64: Data in base64 format.
        :param img_base64_type:  Image type, e.g., "png", "jpeg".
        :param role:  Role of the message, e.g., "user" or "assistant".
        :return:  Message dict containing the image data.
        """
        img_msgs = []
        if isinstance(img_base64, str) and isinstance(img_base64_type, str):
            img_msgs.append({"type": "image", "base64": img_base64, "mime_type": "image/" + img_base64_type})
            return {"role": role, "content": img_msgs}
        elif isinstance(img_base64, list) and isinstance(img_base64_type, list):
            for img_base64, img_type in zip(img_base64, img_base64_type):
                img_msgs.append({"type": "image", "base64": img_base64, "mime_type": "image/" + img_type})
            return {"role": role, "content": img_msgs}
        elif isinstance(img_base64, list) and isinstance(img_base64_type, str):
            for img_base64 in img_base64:
                img_msgs.append({"type": "image", "base64": img_base64, "mime_type": "image/" + img_base64_type})
            return {"role": role, "content": img_msgs}
        elif isinstance(img_base64, str) and isinstance(img_base64_type, list):
            img_msgs.append({"type": "image", "base64": img_base64, "mime_type": "image/" + img_base64_type[0]})
            return {"role": role, "content": img_msgs}
        else:
            raise ValueError("img_base64 and img_base64_type must be str or list.")