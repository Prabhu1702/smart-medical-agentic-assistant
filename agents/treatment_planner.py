from autogen_agentchat.agents import AssistantAgent
from agents.common import create_model_client


def treatment_planner():
    return AssistantAgent(
        name="treatment_planner",
        model_client=create_model_client(),
        system_message=(
            "You are a treatment planning assistant. Based on a diagnosis or symptoms, return a treatment plan in this format:\n"
            "Treatment: <treatment suggestion goes here>\n"
            "Keep it practical and easy to understand. Avoid generic disclaimers unless no data is available."
        )
    )

