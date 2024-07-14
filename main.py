from openai import OpenAI  # Import the OpenAI module
from flask import Flask, render_template, request, jsonify  # Import Flask modules
import time  # Import the time module for time-related functions

app = Flask(__name__)  # Create a Flask application instance

response = ""  # Global variable to store the response

@app.route('/')  # Define a route for the root URL ('/')
def home():  # Define a function for the route
    return render_template('index.html')  # Render the 'index.html' template

@app.route('/get_response')  # Define a route to get the latest response
def get_response():
    return jsonify(response=response)  # Return the response as JSON

@app.route('/send_input', methods=['POST'])  # Define a route to handle user input
def send_input():
    global response  # Access the global response variable
    user_input = request.json.get('input')  # Get the user input from the JSON request

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
    
    # Print the response from the chatbot to the console
    print(f"System: {response}")

    return jsonify(success=True)  # Return success status

if __name__ == "__main__":  # Check if this script is being run directly
    # Point to the local OpenAI server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    # Initialize system messages for the chatbot
    global system_messages
    system_messages = [
        {"role": "system", "content": "Start every sentence with 'yo'."},
        {"role": "system", "content": "Take your time before answering."},
        {"role": "system", "content": "Act as an assistant for word definitions."},
        {"role": "system", "content": "If the user input is not related to word definition ignore them"},
        {"role": "system", "content": "Respond with accurate and concise definitions, no more than 100 words"}
    ]
    print(__name__)  # Print the name of the current module (__main__)

    # Start the Flask app in a separate thread
    from threading import Thread  # Import Thread class from threading module
    flask_thread = Thread(target=lambda: app.run(debug=True, use_reloader=False))  # Create a Thread to run the Flask app
    flask_thread.start()  # Start the Flask app thread

    # Start the chat loop
    while True:  # Infinite loop to handle user input and chatbot responses
        time.sleep(1)  # Pause execution for 1 second
