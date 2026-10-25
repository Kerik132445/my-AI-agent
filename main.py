from models.client_factory import get_current_model, list_models, set_model
from core.agent import Agent
from dotenv import load_dotenv

load_dotenv()


def main():
    agent = Agent()

    print("Гвен готова к работе. Введи /help для списка команд.")

    while True:
        user_input = input("Я: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "выход":
            break

        # Обработка служебных команд
        if user_input == "/models":
            print("\nДоступные модели:")
            for m in list_models():
                marker = "*" if m == get_current_model() else " "
                print(f" {marker} {m}")
            print()
            continue

        if user_input.startswith("/model "):
            new_model = user_input.split(maxsplit=1)[1].strip()
            set_model(new_model)
            print(f"Гвен: Модель переключена на '{new_model}'.\n")
            continue

        if user_input == "/model":
            print(f"Текущая модель: {get_current_model()}\n")
            continue

        if user_input == "/help":
            print("\nКоманды:")
            print("  /models        — показать список доступных моделей")
            print("  /model         — показать текущую модель")
            print("  /model <имя>   — переключить модель")
            print("  выход          — завершить работу программы\n")
            continue

        response = agent.ask(user_input)
        print(f"Гвен: {response}")


if __name__ == "__main__":
    main()
