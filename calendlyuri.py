import os
import requests
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
api_key = os.getenv('CALENDLY_API_KEY')

def list_available_event_uris():
    '''List available event URIs from the Calendly account'''
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.calendly.com/event_types'
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        event_types = data.get('collection', [])
        
        # List all the event names and their full URIs
        for event_type in event_types:
            event_name = event_type['name']
            event_uri = event_type['uri']
            print(f"Event: {event_name}, URI: {event_uri}")
        
        return [event_type['uri'] for event_type in event_types]
    else:
        print(f"Failed to retrieve event types: {response.status_code} - {response.text}")
        return None

# Call the function
list_available_event_uris()