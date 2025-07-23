from autogen_agentchat.agents import AssistantAgent
from agents.common import create_model_client

def diagnosis_agent():
    return AssistantAgent(
        name="diagnosis_agent",
        model_client=create_model_client(),
        system_message=(
            "You are a medical diagnosis assistant. Given symptoms, output a diagnosis in the following format:\n"
            "Diagnosis: <diagnosis goes here>\n"
            "Make sure to be medically sound, but concise."
        )
    )
