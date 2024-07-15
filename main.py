from openai import OpenAI  # Import the OpenAI module
from flask import Flask, render_template, request  # Import Flask modules
import time  # Import the time module for time-related functions
from flask_socketio import SocketIO, emit
from threading import Thread

app = Flask(__name__)  # Create a Flask application instance
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


response = ""

@app.route('/')  # Define a route for the root URL ('/')
def home():  # Define a function for the route
    return render_template('index.html', response=response)  # Render the 'index.html' template with response data

@socketio.on('connect')
def hand_connect():
    emit('system_messages', {'content':'Connected to server'})

@socketio.on('user_input')
def hand_user_input(message):
    global response
    user_input = message['content']
    if user_input.lower() in ["exit", "quit"]:  
        emit('system_message', {'content': 'Chat ended.'})
        return

    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    # Initialize system messages for the chatbot
    system_messages = [
        {"role": "system", "content": "Start every sentence with 'yo'."},
        {"role": "system", "content": "Take your time before answering but don't take too long"},
        {"role": "system", "content": "Act as an assistant for word definitions."},
        {"role": "system", "content": "If the user input is not related to word definition ignore them"},
        {"role": "system", "content": "Respond with accurate and concise definitions, no more than 100 words"}
    ]
    print(__name__)  # Print the name of the current module (__main__)

    # Start the Flask app in a separate thread
    # Prepare messages for the chatbot, including user input and system messages
    messages = system_messages + [{"role": "user", "content": user_input}]

# Generate a completion response from the OpenAI chat model
    completion = client.chat.completions.create(
        model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",  # Model identifier
        messages=messages,  # Messages for the chatbot
        temperature=0.7,  # Temperature parameter for response randomness
    )

# Store the response from the chatbot in the global variable
    response = completion.choices[0].message.content
    emit('update_response', {'content': response})

# Print the response from the chatbot to the console
    print(f"System: {response}") 

if __name__ == '__main__':
    flask_thread = Thread(target=lambda: socketio.run(app, debug=True, use_reloader=False))
    flask_thread.start()

# Start the chat loop
while True:  # Infinite loop to handle user input and chatbot responses
    time.sleep(0.5)  # Pause execution for 1 second
        
 