from flask import Flask, request, jsonify, render_template
import json
import random
from difflib import get_close_matches
import os
import logging

app = Flask(__name__, static_url_path='/static')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load conversation data
current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(current_dir, 'data.json')

try:
    with open(data_file, 'r', encoding='utf-8') as file:
        conversation_data = json.load(file)
    logger.info(f"Successfully loaded data from {data_file}")
    logger.debug(f"Loaded conversations: {len(conversation_data.get('conversations', []))}")
except Exception as e:
    logger.error(f"Error loading data.json: {e}")
    logger.error(f"Attempted to load from: {data_file}")
    conversation_data = {"conversations": []}

def find_best_match(user_message, patterns):
    try:
        user_message = user_message.lower()
        logger.debug(f"Finding match for: {user_message}")
        logger.debug(f"Patterns to match against: {patterns}")
        matches = get_close_matches(user_message, patterns, n=1, cutoff=0.6)
        if matches:
            logger.debug(f"Found match: {matches[0]}")
            return matches[0]
        logger.debug("No match found")
        return None
    except Exception as e:
        logger.error(f"Error in find_best_match: {e}")
        return None

def get_response(user_message):
    try:
        logger.debug(f"Getting response for: {user_message}")
        for conversation in conversation_data['conversations']:
            match = find_best_match(user_message, conversation['patterns'])
            if match:
                response = random.choice(conversation['responses'])
                logger.debug(f"Found response: {response}")
                return response
        
        default_responses = [
            "I'm not sure how to respond to that. Could you rephrase?",
            "मुझे समझ नहीं आया। क्या आप दोबारा बता सकते हैं?",
            "मैं आपकी बात समझ नहीं पाया। कृपया दूसरे तरीके से पूछें।"
        ]
        response = random.choice(default_responses)
        logger.debug(f"Using default response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in get_response: {e}")
        return "Sorry, I encountered an error. Please try again."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        logger.debug(f"Received data: {data}")
        
        if not data:
            logger.error("No data received")
            return jsonify({'response': 'Please send a message'}), 400
        
        user_message = data.get('message', '').strip()
        logger.debug(f"Processing message: {user_message}")
        
        if not user_message:
            logger.error("Empty message received")
            return jsonify({'response': 'Please type a message'}), 400
        
        response = get_response(user_message)
        logger.debug(f"Sending response: {response}")
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'response': 'An error occurred. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
