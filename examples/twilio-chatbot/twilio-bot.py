import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()
app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    user = request.values.get('From', '')
    resp = MessagingResponse()
    resp.message(f'Hello, {user}, thank you for your message!')
    return str(resp)


def start_ngrok():
    from twilio.rest import Client
    from pyngrok import ngrok

    url = ngrok.connect(8765).public_url
    print(' * Tunnel URL:', url)
    client = Client()
    client.incoming_phone_numbers.list(
        phone_number=os.environ.get('TWILIO_PHONE_NUMBER'))[0].update(
            voice_url=url)


if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        start_ngrok()
    app.run(debug=True)
