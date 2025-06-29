import requests 
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


def get_context(file_name): 
    with open(file_name) as file: 
        context = file.read() 
    
    return context 

## generating the prompt based on the template, variables and instructions passed
def generating_prompt(template, variables, instructions):
    for key, value in variables.items(): 
        placeholder = f"[{key}]"
        template = template.replace(placeholder, value)

    prompt = f"#### TEMPLATE: \n {template} \n\n #### INSTRUCTIONS: {instructions}"

    return prompt 

instructions = """
Please rewrite the above letter's body to make it sound more formal and grammatically correct.
You can add the relavant details, but don't introduce new variables.
Output only the final polished letter.
Also write the output in a letter's format. Use newlines and indentation whereever necessary.
Also tone should be respectful"""



API_KEY = os.getenv("API_KEY")

template = get_context('Context_for_permission_letter.txt')


def generate_letter(variables): 

    prompt = generating_prompt(template, variables, instructions)

    headers = {
        "Authorization": f"Bearer {API_KEY}", 
        "Content-Type": "application/json"
    }


    json_data = {
        "model": "llama3-8b-8192", 

        "messages" : [
            {
                "role" : "system", 
                "content": "You are a helpful assistant."
            }, 
            {
                "role" : "user", 
                "content" : f"{prompt}"
            }
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions", 
        headers=headers, 
        json= json_data
    )

    return response.json()['choices'][0]['message']['content']
