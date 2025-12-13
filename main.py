from Agent import LocalAiAgent

def main():
    #agent = LocalAiAgent(modelName="deepseek-r1:8b")
    agent = LocalAiAgent(modelName="llama3.2:3b")
    while True:
        user_input = input("User: ")
        response = agent.invoke(user_input)
        print("AI Response:", response.pretty_repr())

if __name__ == "__main__":
    main()