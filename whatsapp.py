import asyncio
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from salesgpt.salesgptapi import SalesGPTAPI  # Use the correct class SalesGPTAPI from salesgptapi

from dotenv import load_dotenv

load_dotenv()
 
# Initialize Flask app
app = Flask(__name__)

# Initialize SalesGPTAPI (not SalesGPT)
sales_gpt_api = SalesGPTAPI(config_path="examples/example_agent_setup.json")  # Use SalesGPTAPI

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_client = Client(account_sid, auth_token)

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    try:
        """Handle incoming WhatsApp messages and respond using SalesGPTAPI"""
        incoming_msg = request.values.get('Body', '').lower()
        sender = request.values.get('From')

        # Process the incoming message with SalesGPTAPI
        gpt_response = asyncio.run(sales_gpt_api.do(human_input=incoming_msg))  # Call the correct method

        # Handle if gpt_response is None or empty
        if gpt_response is None or 'response' not in gpt_response:
            return jsonify({"error": "SalesGPT did not return a valid response"}), 500

        # Create a response message for WhatsApp
        response = MessagingResponse()
        response.message(f"SalesGPT: {gpt_response['response']}")

        return str(response), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
