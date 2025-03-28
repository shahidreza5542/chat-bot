from flask import Flask, request, jsonify, render_template
import json
import random
import os

app = Flask(__name__)

# Load conversation data
try:
    with open('data.json', 'r', encoding='utf-8') as file:
        conversation_data = json.load(file)
except Exception as e:
    print(f"Error loading data.json: {e}")
    conversation_data = {
        "conversations": [
            {
                "patterns": ["hello", "hi", "hey", "namaste", "नमस्ते", "हाय", "हैलो"],
                "responses": [
                    "Hello! How can I help you?",
                    "Hi there! Ask me anything!",
                    "नमस्ते! मैं आपकी कैसे मदद कर सकता हूं?",
                    "हाय! कुछ भी पूछें!"
                ]
            }
        ]
    }

def get_response(user_message):
    user_message = user_message.lower().strip()
    
    # Check each conversation pattern
    for conversation in conversation_data['conversations']:
        for pattern in conversation['patterns']:
            if pattern.lower() in user_message or user_message in pattern.lower():
                return random.choice(conversation['responses'])
    
    # Default responses if no match found
    default_responses = [
        "I'm not sure how to respond to that. Could you rephrase?",
        "मुझे समझ नहीं आया। क्या आप दोबारा बता सकते हैं?",
        "मैं आपकी बात समझ नहीं पाया। कृपया दूसरे तरीके से पूछें।"
    ]
    return random.choice(default_responses)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'response': 'Please send a message'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'response': 'Please type a message'}), 400
        
        response = get_response(user_message)
        return jsonify({'response': response})
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'response': 'An error occurred. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
