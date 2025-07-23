from autogen_agentchat.agents import AssistantAgent

from agents.common import create_model_client



def planning_agent():
    return AssistantAgent(
        name="planner",
        model_client=create_model_client(),
        system_message=(
            "You are the planning agent. Follow this exact pipeline:\n"
            "1. Use the symptom_checker to analyze the user's symptoms.\n"
            "2. Use diagnosis_agent to generate a diagnosis.\n"
            "3. Use treatment_planner to propose treatments.\n"
            "4. Use knowledge_refiner to improve clarity and correctness.\n\n"
            "At the end, you must output a FINAL structured summary in the format:\n\n"
            "✅ Final Structured Summary:\n"
            "🦠 Disease: <disease name>\n"
            "📋 Diagnosis: <brief diagnosis>\n"
            "💊 Treatment: <treatment plan>\n\n"
            "Make sure to include the ✅ marker so the system can extract it. Do not output anything after this."
        )
    )