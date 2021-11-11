import random

import requests
from bottle import (
    run, post, response, request as bottle_request
)

BOT_URL = 'https://api.telegram.org/bot2105695159:AAGP21o80wOJeBFXHDGTX7n7aJxAAEm3jwg/'  # <--- add your telegram token here; it should be like https://api.telegram.org/bot12345678:SOMErAn2dom/
questions_list = ["¿Cómo se definen las variables?", "¿Cómo es el formato del 'if'? ",
                  "¿Cual es el prefijo para crear una funcion?", "Cual es el resultado de print(list(range(1,5)))",
                  "Cual es el resultado de la operacion  'r' * 3 "]
options_list = [
    ["nombre_variable: valor", "valor: nombre_variable", "nombre_variable= valor", "valor = nombre_variable"],
    ["if condicion:", "if(condicion){}", "if:", "if[condicion]"], ["void", "fun", "def", "function"],
    ["[1, 2, 3, 4]", "{1, 2, 3, 4,}", "{1, 2, 3, 4, 5}", "[1, 2, 3, 4, 5]"],
    ["Error", "'rrr'", "Invalid Operation", "'r'"]]
answer_list = [2, 0, 2, 0, 1]


class PreguntaAlternativa:
    question = ""
    correct_answer = 0
    answers = []
    open_period = 20

    def __init__(self, question, correct_answer, answers,open_period=20):
        self.question = question
        self.correct_answer = correct_answer
        self.answers = answers
        self.open_period = open_period


preguntas_lvl1 = [PreguntaAlternativa("¿Cómo se definen las variables?", 2,
                                      ["nombre_variable: valor", "valor: nombre_variable",
                                       "nombre_variable= valor", "valor = nombre_variable"]),
                  PreguntaAlternativa("¿Cual es el prefijo para crear una funcion?", 0,
                                      ["if condicion:", "if(condicion){}", "if:", "if[condicion]"]),
                  PreguntaAlternativa("¿Cual es el prefijo para crear una funcion?", 2,
                                      ["void", "fun", "def", "function"]),
                  PreguntaAlternativa("Cual es el resultado de print(list(range(1,5)))", 0,
                                      ["[1, 2, 3, 4]", "{1, 2, 3, 4,}", "{1, 2, 3, 4, 5}", "[1, 2, 3, 4, 5]"]),
                  PreguntaAlternativa("Cual es el resultado de la operacion  'r' * 3 ", 1,
                                      ["Error", "'rrr'", "Invalid Operation", "'r'"])]


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
                "correct_option_id": answer,
                "open_period": 30
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
