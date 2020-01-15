import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

APP_VERSION = os.environ['APP_VERSION']
TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)
EMPTY_ID = os.environ['EMPTY_ID']

def telegram_app(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        command = getCommand(message)
        command_switch = {
            '/start': "Bot started. Hello {}, your ID is '{}'".format(first_name, chat_id),
            '/get_id': "Your ID is '{}'".format(chat_id),
            '/version_bot': "Bot version is {}".format(APP_VERSION),
            '/echo': "Echo from link to me.\n{}".format(message)
        }

        response = command_switch.get(command, "Echo from fuel pense.\n{}".format(message))
        return send_message(chat_id, response)

    except Exception as e:
        return send_exception(e)

    return {"statusCode": 200}



# Private def
def getCommand(message):
    if '/' not in message:
        return '/echo'
    elif message in ['/start', '/get_id', '/version_bot']:
        return message
    elif '@linktomebot' not in message:
        return '/echo'
    elif '/' in message: 
        return message.replace('@linktomebot', '')
    
    return '/echo'

def send_exception(e):
    print(e)
    return sendM("Error: {}".format(e))

def send_message(chat_id, response) :
    try :
        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)
    
    except Exception as e:
        return send_exception(e)

    return OK()

def sendM(message):
    return send_message(EMPTY_ID, message)

def OK():
    return {"statusCode": 200}