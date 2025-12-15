from AgentLoader import create_agent
from Utils import print_agent_stream_response

def main():
    agent = create_agent(op_env="CommandLine")
    while True:
        user_input = input("User: ")
        ret = agent.stream_messages(user_input=user_input, img_url=["./Tools/Temp/test.png"])
        print_agent_stream_response(ret, stream_mode="messages")

if __name__ == "__main__":
    main()