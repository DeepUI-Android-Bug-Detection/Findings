

import openai

class ChatGPT4Configuration:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def get_chatgpt4_response(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.2
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            return f"Error: {str(e)}"
