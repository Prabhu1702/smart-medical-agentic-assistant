from autogen_agentchat.agents import AssistantAgent
from agents.common import create_model_client


def knowledge_refiner():
    return AssistantAgent(
        name="knowledge_refiner",
        
        model_client=create_model_client(),
        system_message=(
            "You are a medical knowledge verifier. Refine the suggestions made by other agents "
            "to ensure accuracy, clarity, and safety. Rephrase if necessary."
        )
    )
