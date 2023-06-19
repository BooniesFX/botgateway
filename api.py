import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('API_KEY')
botid = os.getenv('BOT_ID')
url = 'https://chatbase.co/api/v1'

# class BotAPI:
def create_chatbot(chatbot_name, source_text):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'chatbotName': chatbot_name,
        'sourceText': source_text
    }
    response = requests.post(url+"/create-chatbot", headers=headers, data=json.dumps(data))
    return response.json()

def message_chatbot(chatbot_id, messages,is_stream,temp):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "messages": messages,
        "chatbotId": chatbot_id,
        "stream": is_stream,
        "temperature": temp
    }

    response = requests.post(url+"/chat", headers=headers, data=json.dumps(data))
    json_data = response.json()

    if response.status_code == 200:
        print("response:", json_data['text'])
    else:
        print('Error:' + json_data['message'])
    return json_data