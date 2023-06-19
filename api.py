import requests
import json

url = 'https://chatbase.co/api/v1'

def create_new_chatbot(chatbot_name, source_text):  
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'chatbotName': chatbot_name,
            'sourceText': source_text
        }
        response = requests.post(url+"/create-chatbot", headers=headers, data=json.dumps(data))
        # return bot id
        return response.json()

class BotAPI:
    def __init__(self, chatbot_name: str,chatbot_id: str, api_key: str,source_text=None, link_array=None,temp=0.7):
        self.chatbot_name=chatbot_name
        self.chatbot_id=chatbot_id
        self.api_key=api_key
        self.source_text=source_text
        self.link_array = link_array
        self.temp=temp
    
    def message_chatbot(self,message):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "messages": message,
            "chatbotId": self.chatbot_id,
            "stream": False,
            "temperature": self.temp
        }

        response = requests.post(url+"/chat", headers=headers, data=json.dumps(data))
        json_data = response.json()

        if response.status_code == 200:
            print("response:", json_data['text'])
        else:
            print('Error:' + json_data['message'])
        return json_data

