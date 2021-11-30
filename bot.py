import random
import glob, os
import json
import sys

import requests
from bottle import (
    run, post, response, request as bottle_request
)

BOT_URL = 'https://api.telegram.org/bot2105695159:AAGP21o80wOJeBFXHDGTX7n7aJxAAEm3jwg/' 

class MChoiceQuestion:
    number = "000"
    question = ""
    correct_answer = "A"
    options = []
    open_period = 20
    hint = ""

    def __init__(self, number, question, correct_answer, answers, hint, open_period=20):
        self.question = question
        self.correct_answer = correct_answer
        self.options = answers
        self.open_period = open_period
        self.number = number
        self.hint = hint



class CodeQuestion:
    number = "000"
    question = ""
    correct_answer = ""
    hint = ""

    def __init__(self, number, question, correct_answer, hint):
        self.question = question
        self.correct_answer = correct_answer
        self.number = number
        self.hint = hint

current_directory = os.path.dirname(__file__)

db = {}

mChoice_questions = [[[], [], []], [[], [], []], [[], [], []],[[], [], []],[[], [], []]]
code_questions = [[[], [], []], [[], [], []], [[], [], []],[[], [], []],[[], [], []]]


def send_message(prepared_data):
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)


def process_data(data):
    global db

    print(data)
    print()
    if "message" in data and "text" in data["message"]:
        user = check_chat_id(data['message']['chat']['id'])

        if data["message"]["text"] == "/stats":
            print(user)
            json_data = {
                "chat_id": data['message']['chat']['id'],
                "text": "Your stats are:\n Level: {0}\n Points: {1}".format(user[0],user[1])
            }
            send_message(json_data)
        
        elif data["message"]["text"] == "/help":
            help_text = "In this bot you'll try to get complete all the levels gaining points for each on of them while you answer questions about coding on python.\n\nThere are currently 3 levels with different subjects:\n  Level 1 : Comments and Variables\n  Level 2 : Data types and Operators\n  Level 3 : Lists, Tuples, Sets and Dictionaries\n  Level 4 : if and loops\n  Level 5 : functions\nEach time you get to 25 and 50 points on each level the difficulty will increase! And when you get to 100 points you will be tested with 3 questions where you have to write code. If you answer them all correctly you pass to the next level! if you don't, then you will lose points and try again later.\n\nCommands:\n  /question: get a new question\n  /stats: see your current stats\n  /help: I will send you this message again\n\nGood luck!"
            json_data = {
                "chat_id": data['message']['chat']['id'],
                "text": help_text
            }
            send_message(json_data)
            json_data = {
                "chat_id": data['message']['chat']['id'],
                "text": "Your stats are:\n Level: {0}\n Points: {1}".format(user[0],user[1])
            }
            send_message(json_data)
        elif data["message"]["text"] == "/save" and data['message']['chat']['id'] == -755520407:
            save_db()

        elif data["message"]["text"] == "/question":
            alternativa = True
            used = True

            if len(mChoice_questions[user[0]-1][0]) == len(user[6][0]):
                user[6][0] = []
            elif len(mChoice_questions[user[0]-1][1]) == len(user[6][1]):
                user[6][1] = []
            elif len(mChoice_questions[user[0]-1][2]) == len(user[6][2]):
                user[6][2] = []
            elif len(code_questions[user[0]-1][0]) == len(user[7][0]):
                user[7][0] = []
            elif len(code_questions[user[0]-1][1]) == len(user[7][1]):
                user[7][1] = []
            elif len(code_questions[user[0]-1][2]) == len(user[7][2]):
                user[7][2] = []

            while used:
                if user[1] <= 25:
                    random_number = random.randint(0, len(mChoice_questions[user[0]-1][0]) - 1)
                    question = mChoice_questions[user[0]-1][0][random_number]
                    if question.number not in user[6][0]:
                        used = False
                elif user[1] <= 60:
                    random_number = random.randint(0, len(mChoice_questions[user[0]-1][1]) - 1)
                    question = mChoice_questions[user[0]-1][1][random_number]
                    if question.number not in user[6][1]:
                        used = False
                elif user[1] < 100:
                    random_number = random.randint(0, len(mChoice_questions[user[0]-1][2]) - 1)
                    question = mChoice_questions[user[0]-1][2][random_number]
                    if question.number not in user[6][2]:
                        used = False
                elif user[2] == 1:
                    alternativa = False
                    random_number = random.randint(0, len(code_questions[user[0]-1][0]) - 1)
                    question = code_questions[user[0]-1][0][random_number]
                    if question.number not in user[7][0]:
                        used = False
                elif user[2] == 2:
                    alternativa = False
                    random_number = random.randint(0, len(code_questions[user[0]-1][1]) - 1)
                    question = code_questions[user[0]-1][1][random_number]
                    if question.number not in user[7][1]:
                        used = False
                else:
                    alternativa = False
                    random_number = random.randint(0, len(code_questions[user[0]-1][2]) - 1)
                    question = code_questions[user[0]-1][2][random_number]
                    if question.number not in user[7][2]:
                        used = False

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

        elif data["message"]["text"] == "/hint" and user[4] is True:
            question_number = user[3]
            user[8] = True
            if user[5] is True:
                question = code_questions[int(question_number[0])][int(question_number[1])][int(question_number[2])-1]
            else:
                question = mChoice_questions[int(question_number[0])][int(question_number[1])][int(question_number[2])-1]
            json_data = {
                "chat_id": data['message']['chat']['id'],
                "text": question.hint,
                "parse_mode": "HTML"
            }
            send_message(json_data)
        
        elif user[4] is True and user[5] is True:
            user[4] = False
            question_number = user[3]
            question = code_questions[int(question_number[0])][int(question_number[1])][int(question_number[2])-1]
            try:
                x = process_code_answer(data["message"]["text"])
                print(x)
            except ValueError as err:
                print(err)
                x = 0
            if question.correct_answer == x: #ESTO HAY QUE CAMBIAR
                user[7][int(question_number[1])].append(question.number)
                user[2] += 1
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": "Correct!"
                }
                
                if user[2] > 3:
                    user[0] += 1
                    user[2] = 1
                    user[1] = 0
                    send_message(json_data)
                    json_data = {
                        "chat_id": data['message']['chat']['id'],
                        "text": "You passed to the next level!"
                    }
            else:
                if user[2] == 1:
                    if user[8] is True:
                        user[1] = 40
                    else:
                        user[1] = 50
                elif user[2] == 2:
                    if user[8] is True:
                        user[1] = 60
                    else:
                        user[1] = 70
                else:
                    if user[8] is True:
                        user[1] = 80
                    else:
                        user[1] = 90
                user[2] = 1
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": "Incorrect"
                }
            user[8] = False
            send_message(json_data)
            save_db()
        
        elif user[4] is True and data["message"]["text"] in ["A", "B", "C", "D"]:
            user[4] = False
            question_number = user[3]
            question = mChoice_questions[int(question_number[0])][int(question_number[1])][int(question_number[2])-1]
            if question.correct_answer == data["message"]["text"]:
                user[6][int(question_number[1])].append(question.number)
                if user[8] is True:
                    user[1] += 8
                else:
                    user[1] += 10
                if user[1] > 100:
                    user[1] = 100
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": "Correct!"
                }
            else:
                user[1] -= 5
                if user[1] < 0:
                    user[1] = 0
                json_data = {
                    "chat_id": data['message']['chat']['id'],
                    "text": "Incorrect"
                }
            user[8] = False
            send_message(json_data)
            json_data = {
                "chat_id": data['message']['chat']['id'],
                "text": "Your stats are:\n Level: {0}\n Points: {1}".format(user[0],user[1])
            }
            send_message(json_data)
            save_db()

def process_code_answer(answer):
    x = 0
    exec("global x; " + answer)
    return x

def check_chat_id(chat_id):
    global db
    if str(chat_id) not in db:
        db[str(chat_id)] = [1, 0, 1, "000", False, False, [[], [] ,[]], [[], [], []], False] 
                      #Nivel, Puntaje, Pregunta Desarollo, Codigo Pregunta, Esta respondiendo, Alternativa/Codigo, preguntadas alternativa, codigo, hint
    return db[str(chat_id)]

def refactor_question(question):
    lineas = question.split('\\')
    question_final = ""
    for linea in lineas:
        question_final+=linea
        question_final+="\n"
    print(question_final)
    return question_final

def save_db():
    global db
    with open(os.path.join(current_directory, "database.txt"), "w") as jsonfile:
        json.dump(db, jsonfile)

def load_db():
    global db
    with open(os.path.join(current_directory, "database.txt"), "r") as file:
        db = json.load(file)

def load_questions():
    for i in range(1, 6):
        for j in range(1, 6):
            question_file = open(os.path.join(current_directory, "questions", str(i), "mChoice", "beginner", str(j)), "r")
            mChoice_questions[i-1][0].append(
                MChoiceQuestion("{1}0{0}".format(j, i-1), refactor_question(question_file.readline()[:-1]), question_file.readline()[:-1],
                                [question_file.readline()[:-1], question_file.readline()[:-1],
                                 question_file.readline()[:-1], question_file.readline()[:-1]], question_file.readline()))
            question_file.close()
            question_file = open(os.path.join(current_directory, "questions", str(i), "mChoice", "intermediate", str(j)), "r")
            mChoice_questions[i-1][1].append(
                MChoiceQuestion("{1}1{0}".format(j, i-1), refactor_question(question_file.readline()[:-1]), question_file.readline()[:-1],
                                [question_file.readline()[:-1], question_file.readline()[:-1],
                                 question_file.readline()[:-1], question_file.readline()[:-1]], question_file.readline()))
            question_file.close()
            question_file = open(os.path.join(current_directory, "questions", str(i), "mChoice", "advanced", str(j)), "r")
            mChoice_questions[i-1][2].append(
                MChoiceQuestion("{1}2{0}".format(j, i-1), refactor_question(question_file.readline()[:-1]), question_file.readline()[:-1],
                                [question_file.readline()[:-1], question_file.readline()[:-1],
                                 question_file.readline()[:-1], question_file.readline()[:-1]], question_file.readline()))
            question_file.close()

    for i in range(1, 6):
        for j in range(1, 4):
            question_file = open(os.path.join(current_directory, "questions", str(i), "code", "beginner", str(j)), "r")
            code_questions[i-1][0].append(
                CodeQuestion("{1}0{0}".format(j, i-1), refactor_question(question_file.readline()[:-1]), question_file.readline()[:-1], question_file.readline()))
            question_file.close()
            question_file = open(os.path.join(current_directory, "questions", str(i), "code", "intermediate", str(j)), "r")
            code_questions[i-1][1].append(
                CodeQuestion("{1}1{0}".format(j, i-1), refactor_question(question_file.readline()[:-1]), question_file.readline()[:-1], question_file.readline()))
            question_file.close()
            question_file = open(os.path.join(current_directory, "questions", str(i), "code", "advanced", str(j)), "r")
            code_questions[i-1][2].append(
                CodeQuestion("{1}2{0}".format(j, i-1), refactor_question(question_file.readline()[:-1]), question_file.readline()[:-1], question_file.readline()))
            question_file.close()


@post('/')
def main():
    data = bottle_request.json
    process_data(data)

    return response

if __name__ == '__main__':
    load_db()
    load_questions()
    run(host='localhost', port=8080, debug=True)
