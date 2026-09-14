from core.agent import Agent


def main():
    agent = Agent()

    while True:
        user_input = input("Я: ")

        if user_input.lower() == "выход":
            break

        response = agent.ask(user_input)

        print(f"Гвен: {response}")


if __name__ == "__main__":
    main()
