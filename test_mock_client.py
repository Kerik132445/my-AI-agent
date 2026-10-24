from core.agent import Agent
from models.mock_client import send_message


agent = Agent(model_client=send_message)

print(agent.ask("Проверь работу тестового клиента"))
