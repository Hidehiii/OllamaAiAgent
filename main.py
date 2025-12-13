from AgentLoader import select_agent
from Utils import print_agent_stream_response

def main():
    agent = select_agent()
    while True:
        user_input = input("User: ")
        #response = agent.invoke(user_input)
        #print(response.pretty_repr())
        ret = agent.stream_messages(user_input)
        print_agent_stream_response(ret, stream_mode="messages")

if __name__ == "__main__":
    main()