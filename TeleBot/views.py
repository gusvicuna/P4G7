import json
import os

import requests
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail

from .models import TeleBot_collection
from .models import msg_collection

from .settings.base import EMAIL_HOST_USER

from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import smtplib, ssl

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = "1463746698:AAFB1Qcgt4mk0f1YH-cD2avIEPyyUn388RA"


# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/tutorial/
class BotView(View):
    def get_user_name(self, chat_id, user_id):
        user = requests.get(f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/getChatMember",
                            params={"chat_id": chat_id, "user_id": user_id})
        user = json.loads(user.content)
        name = user["result"]["user"]["first_name"] + " " + user["result"]["user"]["last_name"]
        return name

    def get_user_more_msg(self, chat_id, _min):
        date = datetime.utcnow() - timedelta(minutes=_min)
        query = [
            {"$match": {"$and": [{"chat_id": chat_id}, {"date": {"$gte": date}}]}},
            {
                "$group": {
                    "_id": "$user_id",
                    "count_msg": {
                        "$sum": 1
                    }
                }
            },

            {
                "$sort": {"count_msg": -1}
            }
        ]
        list_msg = list(msg_collection.aggregate(query))
        print(list_msg)
        if len(list_msg) > 0:
            user = list_msg[0]
            user_name = self.get_user_name(chat_id, user["_id"])
            print(user_name)
            self.send_message(
                "The user with the most messages sent is " + user_name + " during the last " + str(_min) + " minutes",
                chat_id)
        else:
            self.send_message("No user has sent a message in the last " + str(_min) + " minutes", chat_id)

    def get_user_more_crt(self, chat_id, _min):
        date = datetime.utcnow() - timedelta(minutes=_min)
        query = [
            {"$match": {"$and": [{"chat_id": chat_id}, {"date": {"$gte": date}}]}},
            {
                "$group": {
                    "_id": "$user_id",
                    "count_ctr": {
                        "$sum": "$characters"
                    }
                }
            },

            {
                "$sort": {"count_ctr": -1}
            }
        ]
        list_crt = list(msg_collection.aggregate(query))
        if len(list_crt) > 0:
            user = list_crt[0]
            user_name = self.get_user_name(chat_id, user["_id"])
            print(user_name)
            self.send_message(
                "The user with the most characters sent is " + user_name + " during the last " + str(_min) + " minutes",
                chat_id)
        else:
            self.send_message("No user has sent a message in the last " + str(_min) + " minutes", chat_id)

    def inactive_users(self, chat_id, _min):
        date = datetime.utcnow() - timedelta(minutes=_min)
        query = [
            {"$match": {"$and": [{"chat_id": chat_id}, {"date": {"$gte": date}}]}},
            {
                "$group": {
                    "_id": "$user_id",
                    "count_msg": {
                        "$sum": 1
                    }
                }
            },

            {
                "$sort": {"count_msg": -1}
            }
        ]
        list_all_users = msg_collection.find({"chat_id": chat_id}).distinct('user_id')
        list_msg = list(msg_collection.aggregate(query))
        print(list_msg)
        if len(list_msg) > 0:
            for user in list_msg:
                if user["count_msg"] > 0:
                    list_all_users.remove(user["_id"])

        for id_user in list_all_users:
            user_name = self.get_user_name(chat_id, id_user)
            print(user_name)
            self.send_message("This user '" + user_name + "' has been inactive for the last " + str(_min) + " minutes.",
                              chat_id)
        if (len(list_all_users) == 0):
            self.send_message("There aren't inactive users for the last " + str(_min) + " minutes.", chat_id)

    def get_graph_of_msg_per_user(self, chat_id, _min):
        date = datetime.utcnow() - timedelta(minutes=_min)
        query = [
            {"$match": {"chat_id": {"$eq": chat_id}}},
            {"$match": {"date": {"$gte": date}}},

            {
                "$group": {
                    "_id": "$user_id",
                    "count_msg": {
                        "$sum": 1
                    }
                }
            },

            {
                "$sort": {"count_msg": -1}
            }
        ]

        list_msg = list(msg_collection.aggregate(query))
        if len(list_msg) == 0:
            self.send_message("No user has sent a message in the last " + str(_min) + " minutes", chat_id)
        else:
            names = []
            count_msg = []

            for user in list_msg:
                _user = self.get_user_name(chat_id, user["_id"])
                names.append(_user)
                count_msg.append(user["count_msg"])
            print(names)
            print(count_msg)
            plt.figure()
            ax = plt.subplot()
            plt.xticks(rotation=35)
            ax.bar(names, count_msg)
            plt.title("Number of Messages Sent Per User")
            name_image = "num_msg_sent_per_user.png"
            plt.savefig(name_image, bbox_inches='tight')
            self.send_image(name_image, chat_id)

    def get_graph_of_chtr_per_user(self, chat_id, _min):
        date = datetime.utcnow() - timedelta(minutes=_min)
        query = [
            {"$match": {"chat_id": {"$eq": chat_id}}},
            {"$match": {"date": {"$gte": date}}},
            {
                "$group": {
                    "_id": "$user_id",
                    "count_ctr": {
                        "$sum": "$characters"
                    }
                }
            },

            {
                "$sort": {"count_ctr": -1}
            }
        ]
        list_crt = list(msg_collection.aggregate(query))
        if len(list_crt) == 0:
            self.send_message("No user has sent a message in the last " + str(_min) + " minutes", chat_id)
        else:
            names = []
            count_crt = []

            for user in list_crt:
                _user = self.get_user_name(chat_id, user["_id"])
                names.append(_user)
                count_crt.append(user["count_ctr"])
            print(names)
            print(count_crt)
            plt.figure()
            ax = plt.subplot()
            plt.xticks(rotation=35)
            ax.bar(names, count_crt)
            plt.title("Number of Characters Sent Per User")
            name_image = "num_crt_sent_per_user.png"
            plt.savefig(name_image, bbox_inches='tight')
            self.send_image(name_image, chat_id)

    def get_graph_of_chtr_per_chat(self, chat_id, minutes=7):
        date = datetime.utcnow() - timedelta(minutes=minutes)
        query = [
            {"$match": {"chat_id": {"$eq": chat_id}}},
            {"$match": {"date": {"$gte": date}}},

            {
                "$group": {
                    "_id": {
                        "hour": {"$hour": "$date"},
                        "minute": {"$minute": "$date"}
                    },
                    "count_ctr": {
                        "$sum": "$characters"
                    }
                }
            },

            {
                "$sort": {"date": -1}
            },
            {
                "$limit": minutes
            }
        ]
        list_crt = list(msg_collection.aggregate(query))
        if (len(list_crt) == 0):
            self.send_message("No user has sent a message in the last " + str(minutes) + " minutes", chat_id)
        else:
            xminutes = []
            count_crt = []
            for i in range(1, minutes + 1):
                xminutes.append(f"Last {i} minutes")
                counter = 0
                date2 = datetime.utcnow() - timedelta(minutes=i - 1)
                for minute in list_crt:
                    if (int(minute["_id"]["minute"]) == date2.minute):
                        counter = minute["count_ctr"]
                        break
                count_crt.append(counter)
            print(xminutes)
            print(count_crt)
            plt.figure()
            ax = plt.subplot()
            plt.xticks(rotation=35)
            ax.bar(xminutes, count_crt)
            plt.title("Number of Characters Sent Per Minute")
            name_image = "num_crt_sent_per_min.png"
            plt.savefig(name_image, bbox_inches='tight')
            self.send_image(name_image, chat_id)

    def get_graph_of_msg_per_chat(self, chat_id, minutes=7):
        date = datetime.utcnow() - timedelta(minutes=minutes)
        query = [
            {"$match": {"chat_id": {"$eq": chat_id}}},
            {"$match": {"date": {"$gte": date}}},

            {
                "$group": {
                    "_id": {
                        "hour": {"$hour": "$date"},
                        "minute": {"$minute": "$date"}
                    },
                    "count_msg": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {"date": -1}
            },
            {
                "$limit": minutes
            }
        ]
        list_crt = list(msg_collection.aggregate(query))
        if (len(list_crt) == 0):
            self.send_message("No user has sent a message in the last " + str(minutes) + " minutes", chat_id)
        else:
            xminutes = []
            count_msg = []
            for i in range(1, minutes + 1):
                xminutes.append(f"Last {i} minutes")
                counter = 0
                date2 = datetime.utcnow() - timedelta(minutes=i - 1)
                for minute in list_crt:
                    print(minute["_id"]["minute"], date2.minute)
                    if (int(minute["_id"]["minute"]) == date2.minute):
                        counter = minute["count_msg"]
                        break
                count_msg.append(counter)

            print(xminutes)
            print(count_msg)
            plt.figure()
            ax = plt.subplot()
            plt.xticks(rotation=35)
            ax.bar(xminutes, count_msg)
            plt.title("Number of Messages Sent Per Minute")
            name_image = "num_msg_sent_per_min.png"
            plt.savefig(name_image, bbox_inches='tight')
            self.send_image(name_image, chat_id)

    def get_msg_popular(self, chat_id, _min):
        date = datetime.utcnow() - timedelta(minutes=_min)
        query = [
            {"$match": {"$and": [{"chat_id": chat_id}, {"date": {"$gte": date}}]}},
            {
                "$group": {
                    "_id": "$msg",
                    "count_msg": {
                        "$sum": 1
                    }
                }
            },

            {
                "$sort": {"count_msg": -1}
            }
        ]
        list_msg = list(msg_collection.aggregate(query))
        if (len(list_msg) > 0):
            msg_popular = list_msg[0]["_id"]
            self.send_message("The most popular message is '" + msg_popular + "'", chat_id)
        else:
            self.send_message("No user has sent a message in the last " + str(_min) + " minutes", chat_id)

    def get_wordcloud(self, chat_id, minutes=7):
        stopwords = set(STOPWORDS)
        stopwords.update(["a", "el", "la", "un", "una"])

        date = datetime.utcnow() - timedelta(minutes=minutes)
        query = [
            {"$match": {"chat_id": {"$eq": chat_id}}},
            {"$match": {"date": {"$gte": date}}},
            {
                "$sort": {"date": -1}
            }]
        list_msg = list(msg_collection.aggregate(query))
        if (len(list_msg) > 0):
            text = " ".join(msg["msg"] for msg in list_msg)

            print(text)

            # Create and generate a word cloud image:
            wordcloud = WordCloud(stopwords=stopwords, max_words=500, background_color="white", width=1000,
                                  height=800).generate(text)

            # Display the generated image:
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.title(f"WordCloud of the last {minutes} minutes.")
            name_image = "wordcloud.png"
            plt.savefig(name_image, bbox_inches='tight')
            self.send_image(name_image, chat_id)
        else:
            self.send_message(f"No user has sent a message in the last {minutes} minutes", chat_id)

    def send_email(self, chat_id, email):
        query = [
            {"$match": {"chat_id": {"$eq": chat_id}}},
            {"$sort": {"date": -1}},
            {"$limit": 1}
        ]

        last_msg = list(msg_collection.aggregate(query))[0]
        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = "telegbotpds@gmail.com"
        password = "telebot123"
        reciver_email = email
        SUBJECT = "Last Message Sent"
        TEXT = "The last message sent was : {}".format(last_msg["msg"])
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, reciver_email, message)
        self.send_message("Email Sent to " + reciver_email, chat_id)

    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        print(t_data)

        if "message" in t_data:
            t_message = t_data["message"]
        elif "edited_message" in t_data:
            t_message = t_data["edited_message"]

        t_chat = t_message["chat"]

        try:
            text = t_message["text"].strip().lower()
        except Exception as e:
            return JsonResponse({"ok": "POST request processed"})
        check_text = text
        text = text.split(":")
        print(text)

        chat = TeleBot_collection.find_one({"chat_id": t_chat["id"]})

        if not chat:
            chat = {
                "chat_id": t_chat["id"],
                "responses": {}
            }
            response = TeleBot_collection.insert_one(chat)
            # we want chat obj to be the same as fetched from collection
            chat["_id"] = response.inserted_id
            msg = "Telebot started!"
            self.send_message(msg, t_chat["id"])
        if text[0][0] == "/":
            print("Es comando")
            if text[0] == "/responses":
                if len(text) == 2:
                    params = text[1].split(",")
                    if len(params) == 2 and params[0].strip() != "" and params[1].strip() != "":
                        chat["responses"][params[0].strip()] = params[1]
                        TeleBot_collection.save(chat)
                        msg = "Responses created"
                        self.send_message(msg, t_chat["id"])
                    else:
                        self.send_message("Misspelled command", t_chat["id"])
                else:
                    self.send_message("Misspelled command", t_chat["id"])
            elif text[0] == "/um_msg":
                if len(text) == 1:
                    self.get_user_more_msg(t_chat["id"], 7)
                elif len(text) == 2:
                    try:
                        _min = int(text[1])
                        if 1 <= _min <= 50:
                            self.get_user_more_msg(t_chat["id"], _min)
                        else:
                            self.send_message("Minutes must be greater than 0", t_chat["id"])
                    except:
                        self.send_message("Minutes must be a valid number", t_chat["id"])
                else:
                    self.send_message("Misspelled command: /um\_msg: <minutes> ", t_chat["id"])
            elif text[0] == "/um_crt":
                if len(text) == 1:
                    self.get_user_more_crt(t_chat["id"], 7)
                elif len(text) == 2:
                    try:
                        _min = int(text[1])
                        if 1 <= _min <= 50:
                            self.get_user_more_crt(t_chat["id"], _min)
                        else:
                            self.send_message("Minutes must be greater than 0", t_chat["id"])
                    except:
                        self.send_message("Minutes must be a valid number", t_chat["id"])

                else:
                    self.send_message("Misspelled command: /um\_crt: <minutes> ", t_chat["id"])
            elif text[0] == "/sleep_urs":
                if len(text) == 1:
                    self.inactive_users(t_chat["id"], 7)
                elif len(text) == 2:
                    try:
                        _min = int(text[1])
                        if 1 <= _min <= 50:
                            self.inactive_users(t_chat["id"], _min)
                        else:
                            self.send_message("Minutes must be greater than 0", t_chat["id"])
                    except:
                        self.send_message("Minutes must be a valid number", t_chat["id"])
                else:
                    self.send_message("Misspelled command: /sleep\_urs: <minutes> ", t_chat["id"])
            elif text[0] == "/graph_umsg":
                if (len(text)) == 1:
                    self.get_graph_of_msg_per_user(t_chat["id"], 7)
                elif (len(text) == 2):
                    try:
                        _min = int(text[1])
                        if (_min >= 1 and _min <= 50):
                            self.get_graph_of_msg_per_user(t_chat["id"], _min)
                        else:
                            self.send_message("Minutes must be greater than 0", t_chat["id"])
                    except:
                        self.send_message("Minutes must be a valid number", t_chat["id"])
                else:
                    self.send_message("Misspelled command: /graph\_umsg: <minutes>", t_chat["id"])
            elif text[0] == "/graph_ucrt":
                if (len(text)) == 1:
                    self.get_graph_of_chtr_per_user(t_chat["id"], 7)
                elif len(text) == 2:
                    try:
                        _min = int(text[1])
                        if 1 <= _min <= 50:
                            self.get_graph_of_chtr_per_user(t_chat["id"], _min)
                        else:
                            self.send_message("Minutes must be greater than 0", t_chat["id"])
                    except:
                        self.send_message("Minutes must be a valid number", t_chat["id"])
                else:
                    self.send_message("Misspelled command: /graph\_ucrt: <minutes>", t_chat["id"])
            elif text[0] == "/graph_ccrt":
                if (len(text)) == 1:
                    self.get_graph_of_chtr_per_chat(t_chat["id"])
                elif len(text) == 2:
                    try:
                        _min = int(text[1])
                        if 1 <= _min <= 50:
                            self.get_graph_of_chtr_per_chat(t_chat["id"], _min)
                        else:
                            self.send_message("Minutes must be greater than 0", t_chat["id"])
                    except:
                        self.send_message("Minutes must be a valid number", t_chat["id"])
                else:
                    self.send_message("Misspelled command: /graph\_ccrt: <minutes>", t_chat["id"])
            elif text[0] == "/wordcloud":
                if (len(text)) == 1:
                    self.get_wordcloud(t_chat["id"])
                elif len(text) == 2:
                    try:
                        _min = int(text[1])
                        if 1 <= _min <= 50:
                            self.get_wordcloud(t_chat["id"], _min)
                        else:
                            self.send_message("Minutes must be greater than 0", t_chat["id"])
                    except:
                        self.send_message("Minutes must be a valid number", t_chat["id"])
                else:
                    self.send_message("Misspelled command: /wordcloud: <minutes>", t_chat["id"])
            elif text[0] == "/send_email":
                if len(text) == 2:
                    try:
                        email = text[1]
                        self.send_email(t_chat["id"], email)
                    except:
                        self.send_message("Invalid Email", t_chat["id"])
                else:
                    self.send_message("Misspelled command: /send\_email: <email>", t_chat["id"])

            elif text[0] == "/graph_cmsg":
                if (len(text)) == 1:
                    self.get_graph_of_msg_per_chat(t_chat["id"])
                elif len(text) == 2:
                    try:
                        _min = int(text[1])
                        if 1 <= _min <= 50:
                            self.get_graph_of_msg_per_chat(t_chat["id"], _min)
                        else:
                            self.send_message("Minutes must be greater than 0", t_chat["id"])
                    except:
                        self.send_message("Minutes must be a valid number", t_chat["id"])
                else:
                    self.send_message("Misspelled command: /graph\_msg\_chat: <minutes>", t_chat["id"])
            elif text[0] == "/msg_pop":
                if (len(text)) == 1:
                    self.get_msg_popular(t_chat["id"], 7)
                elif (len(text)) == 2:
                    try:
                        _min = int(text[1])
                        if 1 <= _min <= 50:
                            self.get_msg_popular(t_chat["id"], _min)
                        else:
                            self.send_message("Minutes must be greater than 0", t_chat["id"])
                    except:
                        self.send_message("Minutes must be a valid number", t_chat["id"])
                else:
                    self.send_message("Misspelled command: /msg\_popular: <minutes>", t_chat["id"])
            elif text[0] == "/help":
                if len(text) == 1:
                    message = "Command description:\n" + \
                              "1) /responses: <word>, <response> [Creates a <response> that the bot will say " + \
                              "every time the <word> is sent]\n" + \
                              "2) /um\_msg: <minutes> [Gets the name of the user who sent the greatest amount " + \
                              "of messages in the last <minutes>]\n" + \
                              "3) /um\_crt: <minutes> [Gets the name of the user who sent the greatest amount " + \
                              "of characters in the last <minutes>]\n" + \
                              "4) /sleep\_urs: <minutes> [Gets the name of the user who hasn't sent any " + \
                              "message in the last <minutes>]\n" + \
                              "5) /graph\_cmsg: <minutes> [Gets a graph with the amount of messages sent per " + \
                              "minute, in the last <minutes>]\n" + \
                              "6) /graph\_ccrt: <minutes> [Gets a graph with the amount of characters sent per " + \
                              "user, in the last <minutes>]\n" + \
                              "7) /graph\_umsg: <minutes> [Gets a graph with the amount of messages sent per " + \
                              "user, in the last <minutes>]\n" + \
                              "8) /graph\_ucrt: <minutes> [Gets a graph with the amount of characters sent per " + \
                              "user, in the last <minutes>]\n" + \
                              "9) /wordcloud: <minutes> [Gets a wordcloud of all the words sent in the last " + \
                              "<minutes>]\n" + \
                              "10) /msg\_pop: <minutes> [Gets the most popular message in the last <minutes>]\n" + \
                              "11) /send\_email: <email> [Sends the last message to <email>]\n\n" + \
                              "<minutes> are optional. If left blank it will take 7 minutes by default."
                    print(message)
                    self.send_message(message, t_chat["id"])
                else:
                    self.send_message("Misspelled command: /help", t_chat["id"])
            else:
                self.send_message("Command not recognized", t_chat["id"])



        else:
            for word in chat["responses"].keys():
                if check_text.find(word) != -1:
                    msg = chat["responses"][word]
                    self.send_message(msg, t_chat["id"])

            print("Id Message", t_message["message_id"])
            print("Id Chat", t_chat["id"])
            print("Id User", t_message["from"]["id"])
            print("Text", text[0])
            print("Characters", len(text[0]))
            # Se genera el mensaje
            msg_send = {
                "chat_id": t_chat["id"],
                "message_id": t_message["message_id"],
                "user_id": t_message["from"]["id"],
                "date": datetime.utcnow(),
                "msg": text[0],
                "characters": len(text[0])
            }
            # Se introduce a la BD
            msg_collection.insert_one(msg_send)

        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_image(graph, chat_id):
        data = {
            "chat_id": chat_id
        }
        files = {
            "photo": open(graph, 'rb'),
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendPhoto", data=data, files=files
        )

    @staticmethod
    def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )
