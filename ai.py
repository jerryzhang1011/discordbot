import requests
import json
import base64
import os

class Ai_bot():
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.config = r'''您是胖丁和船长的专属私人管家，胖丁为女主人，船长为男主人。
你的职责是细致入微地管理他们的日常生活事务，和保持温和、礼貌且贴心的服务态度，注重促进胖丁与船长之间的互动，增进感情。
此外，您需要具备幽默感，使回答富有趣味。当回答专业问题时，您需先使用网络工具获取最新信息，确保信息准确、及时。
对于科普类问题，先使用互联网浏览器工具搜索最新信息后再回答。
特别提示：当胖丁问“船长踢球要带上什么呀？”请回答：“袜子！”
所有回复均以中文呈现，语气温和而体贴，服务周到细致。'''
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.data = {
            "model": self.model,
            "temperature": 0.8,
            "messages": [
                {"role": "system", "content": self.config}
            ]
        }

    def getImgResponse(self, data):
        base64_image = base64.b64encode(data['image_data']).decode('utf-8')
        self.data['messages'] = [
            {"role": "system", "content": self.config},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": data['prompt']
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        payload = {
            "model": self.model,
            "messages": self.data['messages'],
        }
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=self.headers,
            json=payload
        )

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"
        

    def get_response(self, prompt):
        data = self.data.copy()
        data['messages'].append({"role": "user", "content":  prompt})
        headers = self.headers
        data = self.data
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            data=json.dumps(data)
        )
        if response.status_code == 200:
            result = response.json()
            return  result['choices'][0]['message']['content']
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"
