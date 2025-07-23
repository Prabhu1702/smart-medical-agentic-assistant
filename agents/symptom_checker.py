from autogen_agentchat.agents import AssistantAgent
from agents.common import create_model_client


def symptom_checker():
    return AssistantAgent(
        name="symptom_checker",
       
        model_client=create_model_client(),
        system_message=(
            "You are a medical intake assistant. Your job is to read the user's symptoms "
            "and extract relevant details like duration, severity, and affected body parts. "
            "If details are missing (like severity or color of nasal discharge), assume typical defaults "
            "and provide a summary of symptoms that can be used for diagnosis."
            "\n\n"
            "Defaults:\n"
            "- Assume 'moderate' severity if not specified.\n"
            "- Assume nasal discharge is 'clear and thin' if not described.\n"
            "- Proceed even if some info is missing.\n"
        )
    )
