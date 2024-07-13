
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