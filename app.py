from flask import Flask, request, jsonify, render_template
import json
import random
from difflib import get_close_matches
import os

app = Flask(__name__, static_url_path='/static')

# Load conversation data
try:
    with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'r', encoding='utf-8') as file:
        conversation_data = json.load(file)
except Exception as e:
    print(f"Error loading data.json: {e}")
    conversation_data = {"conversations": []}

def find_best_match(user_message, patterns):
    try:
        user_message = user_message.lower()
        matches = get_close_matches(user_message, patterns, n=1, cutoff=0.6)
        return matches[0] if matches else None
    except Exception as e:
        print(f"Error in find_best_match: {e}")
        return None

def get_response(user_message):
    try:
        for conversation in conversation_data['conversations']:
            match = find_best_match(user_message, conversation['patterns'])
            if match:
                return random.choice(conversation['responses'])
        
        return random.choice([
            "I'm not sure how to respond to that. Could you rephrase?",
            "मुझे समझ नहीं आया। क्या आप दोबारा बता सकते हैं?",
            "मैं आपकी बात समझ नहीं पाया। कृपया दूसरे तरीके से पूछें।"
        ])
    except Exception as e:
        print(f"Error in get_response: {e}")
        return "Sorry, I encountered an error. Please try again."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        response = get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
