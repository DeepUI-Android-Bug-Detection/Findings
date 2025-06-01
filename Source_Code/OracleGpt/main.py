
from chatgpt4_config import ChatGPT4Configuration
from text_processing import TextProcessing
from deepui_prompt_template import create_deepui_prompt
import csv

if __name__ == "__main__":
    api_key = "YOUR_OPENAI_API_KEY_HERE"

    # Initialize GPT-4
    gpt4 = ChatGPT4Configuration(api_key)
    processor = TextProcessing(gpt4)

    # Sample prompt values
    role = "You are an expert in mobile app UI and functionality."
    rules = "Ignore irrelevant system signals such as time, battery, Wi-Fi, notifications, or mobile data. Focus strictly on the actions and interface flow."
    actions = "Open the app. Adjust the size of the pop-out mode. Select a configurable minimum size in the settings menus."
    semantic_descriptions = open("semantic_description.txt", "r").read()  # Optional external file

    # Compose prompt
    full_prompt = create_deepui_prompt(role, rules, actions, semantic_descriptions)

    # Get GPT-4 result
    result = processor.generate_output_for_prompt(full_prompt)

    # Output
    print("===== GPT-4 Bug Analysis =====")
    print(result)
