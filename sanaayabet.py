import sys
from flask import Flask, request
import telepot
from telepot.loop import OrderedWebhook
import os

"""
$ python2.7 flask_skeleton.py <token> <listening_port> <webhook_url>
Webhook path is '/webhook', therefore:
<webhook_url>: https://<base>/webhook
"""

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)


TOKEN = '895872757:AAH75clxWg4qja8byHiEs_pqismo_GTnj3Q'
PORT = int(os.environ.get('PORT', 5000))
URL = 'https://sanaayabet.herokuapp.com'

app = Flask(__name__)
bot = telepot.Bot(TOKEN)
webhook = OrderedWebhook(bot, {'chat': on_chat_message,
                               'callback_query': on_callback_query})

@app.route('/', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'

if __name__ == '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(host='0.0.0.0', port=PORT, debug=True)