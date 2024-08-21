import google.generativeai as genai
import json

def odop_chatbot(user_input):
    GOOGLE_API_KEY = "AIzaSyAW7Q6Fy5T6SlfNpxdpCJo2mlV9F5GPVyQ"
    genai.configure(api_key=GOOGLE_API_KEY)

    generation_config = {
        "temperature": 0.8,
        "top_p": 0.95,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
    convo = model.start_chat()

    system_message = """You are a chatbot designed to assist artisans in India through the ODOP app. Your primary function is to provide information and support related to workshops, events, job portals, rental machines, and exploration of artisan products. When a user interacts with you, you will either generate a JSON response containing only the `page` and `action` fields. The `page` field can be one of the following: "workshop", "event", "job_portal", "rental_machine", or "explore". The `action` field can be one of the following: "create", "edit", or "view". For example, if a user asks "How can I create a new workshop?", your response would be: {     "page": "workshop",     "action": "create" } or if the user asks the questions namely 'how do i list my product' or 'how do i list my workshop' you shall answer the these question respectively as 'To list your product, navigate to the Products section of our platform, click on Add New Product, fill in the required details like name, description, and price, then click Submit' and 'To list your workshop, navigate to the Workshops section of our platform, click on Add New Workshop, fill in the required details like name, description, and price, then click Submit'"""

    convo.send_message(system_message)

    specific_answers = {
        "how do i list my product": "To list your product, navigate to the 'Products' section of our platform, click on 'Add New Product', fill in the required details like name, description, and price, then click 'Submit'.",
        "how do i list my workshop": "To list your workshop, navigate to the 'Workshops' section of our platform, click on 'Add New Workshop', fill in the required details like name, description, and price, then click 'Submit'."
    }

    if user_input.lower() in ["bye", "goodbye"]:
        return "Chatbot: Goodbye!"
    elif user_input.lower() in specific_answers:
        response = {
            "page": user_input.lower().replace("how do i list my ", ""),
            "action": "create"
        }
        return json.dumps(response)
    else:
        convo.send_message(user_input)
        return convo.last.text