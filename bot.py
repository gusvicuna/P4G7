import random
import glob, os
import json
import sys

import requests
from bottle import (
    run, post, response, request as bottle_request
)

BOT_URL = 'https://api.telegram.org/bot2105695159:AAGP21o80wOJeBFXHDGTX7n7aJxAAEm3jwg/'  # <--- add your telegram token here; it should be like https://api.telegram.org/bot12345678:SOMErAn2dom/

class MChoiceQuestion:
    number = "000"
    question = ""
    correct_answer = "A"
    options = []
    open_period = 20

    def __init__(self, number, question, correct_answer, answers, open_period=20):
        self.question = question
        self.correct_answer = correct_answer
        self.options = answers
        self.open_period = open_period
        self.number = number


class CodeQuestion:
    number = "000"
    question = ""
    correct_answer = ""

    def __init__(self, number, question, correct_answer):
        self.question = question
        self.correct_answer = correct_answer
        self.number = number

current_directory = os.path.dirname(__file__)

db = {}

mChoice_questions = [[[], [], []], [[], [], []], [[], [], []]]
code_questions = [[[], [], []], [[], [], []], [[], [], []]]


def send_message(prepared_data):
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)


def process_data(data):
    print(data)
    print()
    if "message" in data and "text" in data["message"]:
        db_values = check_chat_id(data['message']['chat']['id'])

        if data["message"]["text"] == "/stats":
            json_data = {
                "chat_id": data['message']['chat']['id'],
                "text": "Your stats are:\n Level: {0}\n Points: {1}".format(db_values[0],db_values[1])
            }
            send_message(json_data)

        elif data["message"]["text"] == "/save" and data['message']['chat']['id'] == -755520407:
            save_db()

        elif data["message"]["text"] == "/pregunta":
            user = db[data['message']['chat']['id']]
            alternativa = True


            if user[1] < 25:
                random_number = random.randint(0, len(mChoice_questions[user[0]-1][0]) - 1)
                question = mChoice_questions[user[0]-1][0][random_number]
            elif db[data['message']['chat']['id']][1] < 50:
                random_number = random.randint(0, len(mChoice_questions[user[0]-1][1]) - 1)
                question = mChoice_questions[user[0]-1][1][random_number]
            elif user[1] < 100:
                random_number = random.randint(0, len(mChoice_questions[user[0]-1][2]) - 1)
                question = mChoice_questions[user[0]-1][2][random_number]
            elif user[2] == 1:
                alternativa = False
                random_number = random.randint(0, len(code_questions[user[0]-1][0]) - 1)
                question = code_questions[user[0]-1][0][random_number]
            elif user[2] == 2:
                alternativa = False
                random_number = random.randint(0, len(code_questions[user[0]-1][1]) - 1)
                question = code_questions[user[0]-1][1][random_number]
            else:
                alternativa = False
                random_number = random.randint(0, len(code_questions[user[0]-1][2]) - 1)
                question = code_questions[user[0]-1][2][random_number]

            user[3] = question.number
            user[4] = True

            if alternativa:
                user[5] = False
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": "{0}: {1}\nA) {2}\nB) {3}\nC) {4}\nD) {5}".format(question.number, question.question,
                                                                            question.options[0], question.options[1],
                                                                            question.options[2], question.options[3]),
                    "parse_mode": "HTML",
                    "reply_markup": {"keyboard": [[{"text": "A"}], [{"text": "B"}], [{"text": "C"}], [{"text": "D"}]],
                                    "one_time_keyboard": True, 
                                    "resize_keyboard": True}
                }
            else:
                user[5] = True
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": question.question,
                    "parse_mode": "HTML"
                }

            send_message(json_data)

        elif db_values[4] is True and db_values[5] is True:
            db_values[4] = False
            question_number = db_values[3]
            question = code_questions[int(question_number[0])][int(question_number[1])][int(question_number[2])-1]
            if question.correct_answer == data["message"]["text"]: #ESTO HAY QUE CAMBIAR
                db_values[2] += 1
                if db_values[2] > 3:
                    db_values[0] += 1
                    db_values[2] = 1
                    db_values[1] = 0
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": "Correcto!"
                }
            else:
                if db_values[2] == 1:
                    db_values[1] = 50
                elif db_values[2] == 2:
                    db_values[1] = 70
                else:
                    db_values[1] = 90
                db_values[2] = 1
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": "Incorrecto"
                }
            send_message(json_data)
            save_db()
        
        elif db_values[4] is True and data["message"]["text"] in ["A", "B", "C", "D"]:
            db_values[4] = False
            question_number = db_values[3]
            question = mChoice_questions[int(question_number[0])][int(question_number[1])][int(question_number[2])-1]
            if question.correct_answer == data["message"]["text"]:
                db[data['message']['chat']['id']][1] += 5
                if db[data['message']['chat']['id']][1] > 100:
                    db[data['message']['chat']['id']][1] = 100
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": "Correcto!"
                }
            else:
                db[data['message']['chat']['id']][1] -= 5
                if db[data['message']['chat']['id']][1] < 0:
                    db[data['message']['chat']['id']][1] = 0
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": "Incorrecto"
                }
            send_message(json_data)
            save_db()

    elif "poll" in data:
        print(data)
        return


def check_chat_id(chat_id):
    if chat_id not in db:
        db[chat_id] = [1, 0, 1, "000", False, False] #Nivel, Puntaje, Pregunta, Esta respondiendo
    return db[chat_id]


def save_db():
    with open(os.path.join(current_directory, "database.txt"), "w") as jsonfile:
        json.dump(db, jsonfile)


def load_db():
    with open(os.path.join(current_directory, "database.txt"), "r") as file:
        db = json.load(file)
    print(db)


def load_questions():
    for i in range(1, 4):
        for j in range(1, 6):
            question_file = open(os.path.join(current_directory, "questions", str(i), "mChoice", "beginner", str(j)), "r")
            mChoice_questions[i-1][0].append(
                MChoiceQuestion("{1}0{0}".format(j, i-1), question_file.readline()[:-1], question_file.readline()[:-1],
                                [question_file.readline()[:-1], question_file.readline()[:-1],
                                 question_file.readline()[:-1], question_file.readline()]))
            question_file.close()
            question_file = open(os.path.join(current_directory, "questions", str(i), "mChoice", "intermediate", str(j)), "r")
            mChoice_questions[i-1][1].append(
                MChoiceQuestion("{1}1{0}".format(j, i-1), question_file.readline()[:-1], question_file.readline()[:-1],
                                [question_file.readline()[:-1], question_file.readline()[:-1],
                                 question_file.readline()[:-1], question_file.readline()]))
            question_file.close()
            question_file = open(os.path.join(current_directory, "questions", str(i), "mChoice", "advanced", str(j)), "r")
            mChoice_questions[i-1][2].append(
                MChoiceQuestion("{1}2{0}".format(j, i-1), question_file.readline()[:-1], question_file.readline()[:-1],
                                [question_file.readline()[:-1], question_file.readline()[:-1],
                                 question_file.readline()[:-1], question_file.readline()]))
            question_file.close()

    for i in range(1, 4):
        for j in range(1, 2):
            question_file = open(os.path.join(current_directory, "questions", str(i), "code", "beginner", str(j)), "r")
            code_questions[i-1][0].append(
                CodeQuestion("{1}2{0}".format(j, i-1), question_file.readline()[:-1], question_file.readline()))
            question_file.close()
            question_file = open(os.path.join(current_directory, "questions", str(i), "code", "intermediate", str(j)), "r")
            code_questions[i-1][1].append(
                CodeQuestion("{1}2{0}".format(j, i-1), question_file.readline()[:-1], question_file.readline()))
            question_file.close()
            question_file = open(os.path.join(current_directory, "questions", str(i), "code", "advanced", str(j)), "r")
            code_questions[i-1][2].append(
                CodeQuestion("{1}2{0}".format(j, i-1), question_file.readline()[:-1], question_file.readline()))
            question_file.close()


@post('/')
def main():
    data = bottle_request.json
    process_data(data)

    return response  # status 200 OK by default


if __name__ == '__main__':
    print(exec("variable = 5"))
    load_db()
    load_questions()
    run(host='localhost', port=8080, debug=True)
