from AgentLoader import select_agent

def main():
    agent = select_agent()
    while True:
        user_input = input("User: ")
        response = agent.invoke(user_input)
        print(response.pretty_repr())

if __name__ == "__main__":
    main()