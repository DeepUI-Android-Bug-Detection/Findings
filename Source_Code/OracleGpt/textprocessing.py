

class TextProcessing:
    def __init__(self, chatgpt4_config):
        self.chatgpt4_config = chatgpt4_config

    def generate_output_for_prompt(self, prompt):
        return self.chatgpt4_config.get_chatgpt4_response(prompt)
