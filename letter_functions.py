from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig  
import torch 

# this is used for using the GPU powers!!!
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,   # or load_in_8bit=True
    bnb_4bit_quant_type="nf4",  # recommended for LLMs
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,
)

## for loading the model
def load_model(model_name):

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name) 

    return model, tokenizer 

## for loading the prompt
def load_prompt(model, tokenizer, prompt):
    prompt = f"""
        {prompt}
    """
    # inputs returns a dictionary which contains a list of token IDs which are basically tensors of shape (batch_size, sequence_length) 
    # it also contains a tensor for "attention_mask" which basically denotes the importance of that specific token in the context 
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # passing the inputs to the model to generate an output
    outputs = model.generate(**inputs, max_new_tokens=800)

    # printing the first output as there will be variety of output for the same input
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


## for reading the context file
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


## for generating output after passing the prompt
def generating_output(prompt): 
    model, tokenizer = load_model("tiiuae/falcon-7b-instruct")
    raw_output = load_prompt(model, tokenizer, prompt)

    start_index = raw_output.rfind("Dear")

    if start_index != -1: 
        final_output = raw_output[start_index:].strip()

    else: 
        final_output = raw_output.strip()

    return final_output


# template = get_context("Context_for_permission_letter.txt")
# variables = {
#     "head_in_charge_name": "Geetanjali",
#     "program_name": "Web Development Student Induction Program",
#     "room_no": "A-101",
#     "name": "Sam"
# }


# instructions = """
# Please rewrite the above letter's body to make it sound more formal and grammatically correct.
# Do not add or change any factual details.
# Output only the final polished letter.
# Also write the output in a letter's format. Use newlines and indentation whereever necessary"""


# prompt = generating_prompt(template, variables, instructions)

# model, tokenizer = load_model("tiiuae/falcon-7b-instruct")
# print(load_prompt(model, tokenizer, prompt))

# print(prompt)