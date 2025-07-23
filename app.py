import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from typing import Sequence

from agents.user_proxy import user_proxy
from agents.symptom_checker import symptom_checker
from agents.diagnosis_agent import diagnosis_agent
from agents.treatment_planner import treatment_planner
from agents.knowledge_refiner import knowledge_refiner
from agents.planner import planning_agent
from agents.final_summary_termination import FinalSummaryTermination

from memory.chroma_memory import (
    retrieve_user_memory,
    extract_structured_summary,
    store_user_memory
)

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient

# PDF generation utility
from utils.pdf_generator import generate_summary_pdf

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

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

def selector_func(messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> str | None:
    if messages[-1].source != planning_agent().name: #used to check which agent is called last and if its not planning agent call it 
        return planning_agent().name
    return None

async def diagnosis_workflow(user_id: str, user_input: str):
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
        termination_condition=FinalSummaryTermination()
    )

    full_conversation = "" #the string is empty first  
    task = user_input

    stream = group.run_stream(task=task) # runs the multi-agent loop there chats and interaction
    output = await Console(stream)

    output_str = output.render() if hasattr(output, "render") else str(output)
    full_conversation += "\n" + output_str #adding all data in full_conversation

    summary = extract_structured_summary(full_conversation)
    store_user_memory([{"role": "user", "content": summary}], user_id)

    return output_str, summary

#Streamlit UI 

st.set_page_config(page_title="🧠 Medical Multi-Agent", layout="centered", initial_sidebar_state="auto")
st.title("🩺 Medical Assistant (Multi-Agent)")
st.markdown("### A  multi-agent system for diagnosis and memory retrieval")

st.markdown("#### Enter your name or user ID")
user_id = st.text_input("Enter your name or user ID", key="user_id")

st.markdown("#### Choose an action:")
action = st.radio(
    "Choose an action:",
    options=["Diagnose symptoms", "Retrieve previous medical summary"],
    key="action"
)

if action == "Diagnose symptoms":
    st.markdown("#### Describe your symptoms")
    user_input = st.text_area("Enter symptoms here...", height=150, key="symptom_input")

    if st.button("Run Diagnosis", type="primary"):
        if not user_input.strip() or not user_id.strip():
            st.warning("Please fill in both User ID and Symptoms.")
        else:
            with st.spinner("Running agents..."):
                response, summary = asyncio.run(diagnosis_workflow(user_id, user_input))

            st.markdown("#### Add more details or reply:")
            st.text_input("Respond here...", key="follow_up_input")

            st.success("Summary saved to memory.")

            st.markdown("### ✅ Final Summary")
            st.write(summary if summary else "Summary not found.")

            #download button
            if summary:
                pdf_path = generate_summary_pdf(user_id, summary)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📄 Download Summary as PDF",
                        data=f,
                        file_name=f"{user_id}_medical_summary.pdf",
                        mime="application/pdf"
                    )

elif action == "Retrieve previous medical summary":
    if st.button("Retrieve Summary"):
        if not user_id.strip():
            st.warning("Please enter a valid User ID.")
        else:
            with st.spinner("Retrieving memory..."):
                memory_summary = retrieve_user_memory(user_id)
            if memory_summary:
                st.markdown("### 🧠 Retrieved Summary")
                st.write(memory_summary)
            else:
                st.info("No data found for this user.")
