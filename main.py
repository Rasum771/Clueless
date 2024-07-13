'''from openai import OpenAI as openai

# Point to the local server
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "lm-studio"

# Initialize the system message
def create_chat_completion(user_input, system_message):
    return openai.ChatCompletion.create(
        model="local-model",
        messages=[
            
         {"role" : "system", "content" : system_message},
         {"role" : "user", "content" : user_input}
        ], temperature=0.7
    )

# Start the chat loop
while True:
    system_message = ("You are an assistant or a chatbot", "Respond in a helpful and concise manner")
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Create the chat completion request
    completion = create_chat_completion(user_input, system_message)

    print("Model Responses: ", completion.choices[0].message.content)

    # Print the response from the model '''
 
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Initialize the system messages
system_messages = [
    {"role": "system", "content": "Start every sentence with 'yo'."},
    {"role": "system", "content": "Take your time before answering."},
    {"role": "system", "content": "Act as an assistant for word definitions."},
    {"role": "system", "content": "If the user input is not related to word definition ignore them"},
    {"role": "system", "content": "Respond with accurate and concise definitions, no more than 100 words"}
]

# Start the chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Create the chat completion request
    messages = system_messages + [{"role": "user", "content": user_input}]
    
    completion = client.chat.completions.create(
        model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        messages=messages,
        temperature=0.7,
    )

    # Print the response from the model
    response = completion.choices[0].message.content
    print(f"System: {response}")