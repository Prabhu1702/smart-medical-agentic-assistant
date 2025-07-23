from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo
from dotenv import load_dotenv
import os

load_dotenv()  

api_key = os.getenv("GEMINI_API_KEY")

def create_model_client():
    return OpenAIChatCompletionClient(
        model="gemini-2.0-flash-lite",
        api_key=api_key,
        model_info=ModelInfo(
            vision=True,
            function_calling=True,
            json_output=True,
            family="unknown",
            structured_output=True
        ),
       
    )
