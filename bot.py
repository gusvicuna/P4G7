import random
import glob, os

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


class MChoiceQuestion:
    question = ""
    correct_answer = 0
    options = []
    open_period = 20

    def __init__(self, question, correct_answer, answers, open_period=20):
        self.question = question
        self.correct_answer = correct_answer
        self.options = answers
        self.open_period = open_period


class CodeQuestion:
    question = ""
    correct_answer = ""

    def __init__(self, question, correct_answer):
        self.question = question
        self.correct_answer = correct_answer


db = {}

questions_lvl1 = [MChoiceQuestion("¿Cómo se definen las variables?", 2,
                                      ["nombre_variable: valor", "valor: nombre_variable",
                                       "nombre_variable= valor", "valor = nombre_variable"]),
                  MChoiceQuestion("¿Cual es el prefijo para crear una funcion?", 0,
                                      ["if condicion:", "if(condicion){}", "if:", "if[condicion]"]),
                  MChoiceQuestion("¿Cual es el prefijo para crear una funcion?", 2,
                                      ["void", "fun", "def", "function"]),
                  MChoiceQuestion("Cual es el resultado de print(list(range(1,5)))", 0,
                                      ["[1, 2, 3, 4]", "{1, 2, 3, 4,}", "{1, 2, 3, 4, 5}", "[1, 2, 3, 4, 5]"]),
                  MChoiceQuestion("Cual es el resultado de la operacion  'r' * 3", 1,
                                      ["Error", "'rrr'", "Invalid Operation", "'r'"])]


def send_message(prepared_data):
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """
    message_url = BOT_URL + 'sendPoll'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib


def process_data(data):
    if "message" in data:
        print(data)
        db_values = check_chat_id(data['message']['chat']['id'])
        if data["message"]["text"] == "/close" and data['message']['chat']['id']==-755520407:
            save_db()
        if data["message"]["text"] == "/pregunta":
            random_number = random.randint(0, len(questions_lvl1) - 1)
            question = questions_lvl1[random_number]

            json_data = {
                "chat_id": data['message']['chat']['id'],
                "question": question.question,
                "options": question.options,
                "type": "quiz",
                "correct_option_id": question.correct_answer,
                "open_period": 30
            }

            send_message(json_data)  # <--- function for sending answer
    elif "poll" in data:
        print(data)
        return


def check_chat_id(chat_id):
    if chat_id not in db:
        db[chat_id] = [1, 0, 1]
    return db[chat_id]

def save_db():
    for key in db:
        chat_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\database\\" + str(key) + ".txt", "w")
        for value in db[key]:
            chat_file.write(str(value) + "\n")
        chat_file.close()

def load_db():
    os.chdir("C:\\Users\\gus19\\Desktop\\P4G7\\database")
    for file in glob.glob("*.txt"):
        chat_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\database\\" + str(file), "r")
        chat_values = [int(chat_file.readline()[:-1]), int(chat_file.readline()[:-1]), int(chat_file.readline()[:-1])]
        db[file[:-4]] = chat_values
    print(db)

def load_questions():
    for i in range()

@post('/')
def main():
    data = bottle_request.json
    process_data(data)

    return response  # status 200 OK by default


if __name__ == '__main__':
    load_db()
    run(host='localhost', port=8080, debug=True)
