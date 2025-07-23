# main.py

import asyncio
import os
from typing import Sequence
from dotenv import load_dotenv

from autogen_core.models import ModelInfo
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from agents.final_summary_termination import FinalSummaryTermination

#  Memory Handling
from memory.chroma_memory import (
    store_user_memory,
    retrieve_user_memory,
    manually_store_dummy_data,
    extract_structured_summary
)

# 🤖 Agent Imports
from agents.user_proxy import user_proxy
from agents.symptom_checker import symptom_checker
from agents.diagnosis_agent import diagnosis_agent
from agents.treatment_planner import treatment_planner
from agents.knowledge_refiner import knowledge_refiner
from agents.planner import planning_agent

# 🔐 Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 🧠 Model client setup
model_client = OpenAIChatCompletionClient(
    model="gemini-2.0-flash-lite",
    api_key=api_key,
    model_info=ModelInfo(
        vision=True,
        function_calling=True,
        json_output=True,
        structured_output=True,
        family="unknown"
    )
)


# 👇 Task Selector Function
def selector_func(messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> str | None:
    if messages[-1].source != planning_agent().name:
        return planning_agent().name
    return None

# 🧪 Diagnosis Workflow
async def run_diagnosis_workflow(user_id: str):
    group = SelectorGroupChat(
        [
            planning_agent(),
            symptom_checker(),
            diagnosis_agent(),
            treatment_planner(),
            knowledge_refiner()
        ],
        model_client=model_client,
        selector_prompt="Select the most appropriate agent to handle the user input.",
        allow_repeated_speaker=True,
        selector_func=selector_func,
        # termination_condition=TextMentionTermination("planner") | MaxMessageTermination(10) [ this is not working]
         termination_condition=FinalSummaryTermination() 
    )

    print("\n🩺 Please describe your symptoms below.\n")
    task = input("Your symptoms: ")

    full_conversation = ""

    while True:
        if "✅ Final Structured Summary:" in full_conversation:
            print("\n📦 Final summary detected. Auto-exiting chat loop...\n")
            break
        stream = group.run_stream(task=task)
        output = await Console(stream)

        output_str = output.render() if hasattr(output, "render") else str(output)
        full_conversation += "\n" + output_str

        print("\n🧾 Agent Response:\n")
        print(output_str)


        cont = input("\n🤖 Would you like to continue the conversation? (y/n): ").strip().lower()
        if cont != "y":
            break

        task = input("\n💬 Please provide more info or respond to the agent above:\n")

    summary = extract_structured_summary(full_conversation)
    store_user_memory([{"role": "user", "content": summary}], user_id)
    print("\n✅ Summary saved successfully to ChromaDB.")
    print("\n✅ Ending conversation. Take care!")

# 🧠 Retrieve memory summary
async def run_memory_retrieval(user_id: str):
    summary = retrieve_user_memory(user_id)
    print(f"\n📄 Medical Summary for user {user_id}:\n")
    print(summary)

# 🔁 Entry point
async def main():
    print("🧠 Welcome to the Medical Assistant Multi-Agent System\n")
    user_id = input("Enter your name or user ID: ").strip()

    print("\nWhat would you like to do?")
    print("1. Diagnose symptoms and get treatment plan")
    print("2. Retrieve previous medical info from memory")
    print("3. Insert dummy data into memory (manual test)")
    choice = input("Enter 1, 2 or 3: ").strip()

    if choice == "1":
        await run_diagnosis_workflow(user_id)
    elif choice == "2":
        await run_memory_retrieval(user_id)
    elif choice == "3":
        manually_store_dummy_data(user_id)
    else:
        print("❌ Invalid choice. Please enter 1, 2 or 3.")

    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())
