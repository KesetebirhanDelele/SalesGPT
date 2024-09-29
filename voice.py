from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import os
import asyncio
from salesgpt.salesgptapi import SalesGPTAPI

from dotenv import load_dotenv

load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Initialize SalesGPTAPI
sales_gpt_api = SalesGPTAPI(config_path="examples/example_agent_setup.json")

# Twilio client
twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

@app.route('/voice-webhook', methods=['POST'])
def voice_webhook():
    """Handle incoming voice call and convert speech to text."""
    response = VoiceResponse()

    # Use Twilio's <Gather> to collect speech input
    gather = response.gather(input='speech', action='/process-voice', method='POST')
    gather.say("Hello! How can I help you today? Please speak after the tone.")
    
    return str(response)

@app.route('/process-voice', methods=['POST'])
def process_voice():
    """Process the speech input and respond using SalesGPT."""
    speech_input = request.form.get('SpeechResult', '')
    
    if speech_input:
        # Pass the speech input to SalesGPT
        gpt_response = asyncio.run(sales_gpt_api.do(human_input=speech_input))

        if gpt_response and 'response' in gpt_response:
            response_text = gpt_response['response']
        else:
            response_text = "I'm sorry, I couldn't process your request."

        # Respond back via voice
        response = VoiceResponse()
        response.say(response_text)
        return str(response)
    else:
        response = VoiceResponse()
        response.say("I didn't catch that. Please try again.")
        return str(response)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)