

##  Project Modules

- **ChatGPT4Configuration**: Sets up the OpenAI API client and handles prompt-to-response interaction with ChatGPT-4.
- **TextProcessing**: Generates outputs from prompts using the ChatGPT-4 model.
- **DeepUIPromptTemplate**: Builds semantically rich prompts from widget/OCR/proximity inputs.
- **Main**: Coordinates input prompts, model inference, and output storage.


## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- A valid OpenAI API key with access to GPT-4

###  Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/DeepUI.git
cd DeepUI/Source_Code/OracleGPT
```
### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 3: Add Your API Key
Edit main.py and replace:
```bash
api_key = "YOUR_OPENAI_API_KEY_HERE"

```
### Step 4: Prepare the Input Prompts
You can either:

Use input_prompts.csv with a prompt column.

Or construct dynamic prompts using semantic_description.txt via deepui_prompt_template.py

### Step 5: Run the Script
```bash

python main.py
```
## Prompt Format Example

**Role**: You are an expert in mobile app UI and functionality. Analyze screenshots to identify logical and UI errors, providing concise reasons for your findings or stating **“No error”** if none are found.

**Rules**:
- Ignore irrelevant system signals such as time, battery, Wi-Fi, notifications, or mobile data.
- Focus strictly on the actions and interface flow.

**Operating Actions on the App**:
1. Open the app
2. Adjust the size of the pop-out mode
3. Select a configurable minimum size in the settings menus

**Annotated Screenshots**
**Rich Semantic Descriptions**
> GPT-4 returns: `UI Error – "Toggle Switch not aligned with its label"`

