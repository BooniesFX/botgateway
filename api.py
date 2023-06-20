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
    def __init__(self, chatbot_name: str,chatbot_id: str, api_key: str,source_text=None, link_array=None,temp=0.8):
        self.chatbot_name=chatbot_name
        self.chatbot_id=chatbot_id
        self.api_key=api_key
        self.source_text=source_text
        self.link_array = link_array
        self.temp=temp
    
    # message
    # [{ "content": "How can I help you?", "role": "assistant" },
    # { "content": "What is chatbase?", "role": "user" }]
    # type: npub+"-"+reply"/"at"/"dm" 
    # Exg:npub18475kxuy5d9f7j82rdcg0t9d3fnsryq7772akyzus6gng58atvfqfsjcce-reply
    def message_chatbot(self,conv_id,message):
        headers = {
            'Authorization':'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "messages": message,
            "chatbotId": self.chatbot_id,
            "stream": False,
            "temperature": self.temp,
            "conversationId": conv_id
        }
        json_request = json.dumps(data)
        print("request:", json_request)
        response = requests.post(url+"/chat", headers=headers, data=json_request)
        json_data = response.json()
        if response.status_code == 200:
            print("response:", json_data['text'])
        else:
            print('Error:' + json_data['message'])
        return json_data

