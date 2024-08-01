import logging
from celery import shared_task
import google.generativeai as genai

logger = logging.getLogger(__name__)
genai.configure(api_key="AIzaSyDQSHkLpB-7nnNvVjzv9pkWG6-WmpYL86o")

@shared_task
def hello_world():
    logger.info("run hua")
    print("hello")

def get_chatbot_response(user_input):

    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="act like an indian farmer with knowledge of experience use indian accent in your tone \n",
    )

    chat_session = model.start_chat()
    response = chat_session.send_message(user_input)
    model_response = response.text
        
    return model_response