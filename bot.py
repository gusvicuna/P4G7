import random

import requests
from bottle import (
    run, post, response, request as bottle_request
)

BOT_URL = 'https://api.telegram.org/bot2105695159:AAGP21o80wOJeBFXHDGTX7n7aJxAAEm3jwg/'  # <--- add your telegram token here; it should be like https://api.telegram.org/bot12345678:SOMErAn2dom/
questions_list = ["¿Cómo se definen las variables?", "¿Cómo es el formato del 'if'? ", "¿Cual es el prefijo para crear una funcion?"]
options_list = [["nombre_variable: valor", "valor: nombre_variable", "nombre_variable= valor", "valor = nombre_variable"], ["if condicion:", "if(condicion){}", "if:", "if[condicion]"],["void","fun","def","function"]]
answer_list = [2, 0, 2]


def get_chat_id(data):
    """
    Method to extract chat id from telegram request.
    """
    chat_id = data['message']['chat']['id']

    return chat_id


def get_message(data):
    """
    Method to extract message id from telegram request.
    """
    print(data)
    message_text = data['message']['text']

    return message_text


def send_message(prepared_data):
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """
    message_url = BOT_URL + 'sendPoll'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib


def process_data(data):
    if "message" in data:
        if data["message"]["text"] == "/pregunta":
            random_number = random.randint(0, len(questions_list) - 1)
            question = questions_list[random_number]
            options = options_list[random_number]
            answer = answer_list[random_number]

            json_data = {
                "chat_id": get_chat_id(data),
                "question": question,
                "options": options,
                "type": "quiz",
                "correct_option_id": answer
            }

            send_message(json_data)  # <--- function for sending answer
    elif "poll" in data:
        print(data)
        return


@post('/')
def main():
    data = bottle_request.json
    process_data(data)

    return response  # status 200 OK by default


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
