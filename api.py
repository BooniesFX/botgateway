import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('API_KEY')

url = 'https://chatbase.co/api/v1/create-chatbot'

def create_chatbot(chatbot_name, source_text):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'chatbotName': chatbot_name,
        'sourceText': source_text
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
