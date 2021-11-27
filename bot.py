import random
import glob, os
import json
import sys

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
    correct_answer = ""
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

mChoice_questions = [[[], [], []], [[], [], []], [[], [], []]]
code_questions = [[[], [], []], [[], [], []], [[], [], []]]


def send_message(prepared_data):
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib


def process_data(data):
    if "message" in data and "text" in data["message"]:
        print(data)
        db_values = check_chat_id(data['message']['chat']['id'])

        if data["message"]["text"] == "/save" and data['message']['chat']['id'] == -755520407:
            save_db()

        if data["message"]["text"] == "/pregunta":
            random_number = random.randint(0, len(mChoice_questions[0][0]) - 1)
            question = mChoice_questions[0][0][random_number]

            json_data = {
                "chat_id": data['message']['chat']['id'],
                "text": "{0}\nA){1}\nB){2}\nC){3}\nD){4}".format(question.question, question.options[0], question.options[1], question.options[2], question.options[3]),
                "reply_markup": {"keyboard": [[{"text": "A"}], [{"text": "B"}], [{"text": "C"}], [{"text": "D"}]], 
                                 "one_time_keyboard": True}
            }

            send_message(json_data)  # <--- function for sending answer

        if "reply_to_message" in data["message"]:
            print(data["message"]["text"])
    elif "poll" in data:
        print(data)
        return


def check_chat_id(chat_id):
    if chat_id not in db:
        db[chat_id] = [1, 0, 1]
    return db[chat_id]


def save_db():
    with open("C:\\Users\\gus19\\Desktop\\P4G7\\database.txt", "w") as jsonfile:
        json.dump(db, jsonfile)


def load_db():
    with open("C:\\Users\\gus19\\Desktop\\P4G7\\database.txt", "r") as file:
        db = json.load(file)
    print(db)


def load_questions():
    for j in range(1, 6):
        question_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\questions\\{0}\\mChoice\\beginner\\{1}".format(1, j),
                             "r")
        mChoice_questions[0][0].append(MChoiceQuestion(question_file.readline()[:-1], question_file.readline()[:-1],
                                                      [question_file.readline()[:-1], question_file.readline()[:-1],
                                                       question_file.readline()[:-1], question_file.readline()[:-1]]))
        question_file.close()
        question_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\questions\\{0}\\mChoice\\intermediate\\{1}".format(1, j),
                             "r")
        mChoice_questions[0][1].append(MChoiceQuestion(question_file.readline()[:-1], question_file.readline()[:-1],
                                                      [question_file.readline()[:-1], question_file.readline()[:-1],
                                                       question_file.readline()[:-1], question_file.readline()[:-1]]))
        question_file.close()
        question_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\questions\\{0}\\mChoice\\advanced\\{1}".format(1, j),
                             "r")
        mChoice_questions[0][2].append(MChoiceQuestion(question_file.readline()[:-1], question_file.readline()[:-1],
                                                      [question_file.readline()[:-1], question_file.readline()[:-1],
                                                       question_file.readline()[:-1], question_file.readline()[:-1]]))
        question_file.close()
    for j in range(1, 6):
        question_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\questions\\{0}\\mChoice\\beginner\\{1}".format(2, j),
                             "r")
        mChoice_questions[1][0].append(MChoiceQuestion(question_file.readline()[:-1], question_file.readline()[:-1],
                                                      [question_file.readline()[:-1], question_file.readline()[:-1],
                                                       question_file.readline()[:-1], question_file.readline()[:-1]]))
        question_file.close()
        question_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\questions\\{0}\\mChoice\\intermediate\\{1}".format(2, j),
                             "r")
        mChoice_questions[1][1].append(MChoiceQuestion(question_file.readline()[:-1], question_file.readline()[:-1],
                                                      [question_file.readline()[:-1], question_file.readline()[:-1],
                                                       question_file.readline()[:-1], question_file.readline()[:-1]]))
        question_file.close()
        question_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\questions\\{0}\\mChoice\\advanced\\{1}".format(2, j),
                             "r")
        mChoice_questions[1][2].append(MChoiceQuestion(question_file.readline()[:-1], question_file.readline()[:-1],
                                                      [question_file.readline()[:-1], question_file.readline()[:-1],
                                                       question_file.readline()[:-1], question_file.readline()[:-1]]))
        question_file.close()
    for j in range(1, 6):
        question_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\questions\\{0}\\mChoice\\beginner\\{1}".format(3, j),
                             "r")
        mChoice_questions[2][0].append(MChoiceQuestion(question_file.readline()[:-1], question_file.readline()[:-1],
                                                      [question_file.readline()[:-1], question_file.readline()[:-1],
                                                       question_file.readline()[:-1], question_file.readline()[:-1]]))
        question_file.close()
        question_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\questions\\{0}\\mChoice\\intermediate\\{1}".format(3, j),
                             "r")
        mChoice_questions[2][1].append(MChoiceQuestion(question_file.readline()[:-1], question_file.readline()[:-1],
                                                      [question_file.readline()[:-1], question_file.readline()[:-1],
                                                       question_file.readline()[:-1], question_file.readline()[:-1]]))
        question_file.close()
        question_file = open("C:\\Users\\gus19\\Desktop\\P4G7\\questions\\{0}\\mChoice\\advanced\\{1}".format(3, j),
                             "r")
        mChoice_questions[2][2].append(MChoiceQuestion(question_file.readline()[:-1], question_file.readline()[:-1],
                                                      [question_file.readline()[:-1], question_file.readline()[:-1],
                                                       question_file.readline()[:-1], question_file.readline()[:-1]]))
        question_file.close()
    print(len(mChoice_questions[0][0]))


@post('/')
def main():
    data = bottle_request.json
    process_data(data)

    return response  # status 200 OK by default


if __name__ == '__main__':
    load_db()
    load_questions()
    run(host='localhost', port=8080, debug=True)
