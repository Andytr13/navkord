from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Loads in the env file containing all secured tokens.
load_dotenv('know.env')

# MongoDB URI used to connect with Atlas cluster from the application
conn_str = os.getenv('MONGODB_URL')

# Creates the connection between the application and the Atlas database
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)

# Creates database
mydb = client["navkord"]

# Creates collection
user_col = mydb["users"]
etok_col = mydb["etok"]
ktoe_col = mydb["ktoe"]


# RPG Collection
# This is in the future, rpg collection will have a list of users, but this is an optional sign up meaning some users my not have data for this collection
# rpg_col = mydb["rpg"]

def add_user(user_data):
    user_col.insert_one(user_data)


def find_user(user):
    user_query = user_col.find({"user": str(user)}, {"_id": False})
    for x in user_query:
        return x
    else:
        return {}


def update_user(user, updated_data):
    user_col.update_one({"user": str(user)}, updated_data)


def add_ktoe(results):
    ktoe_col.insert_one(results)


def find_ktoe(word):
    for x in ktoe_col.find({"word": word}, {"_id": False}):
        return x
    return False


def add_etok(results):
    etok_col.insert_one(results)


def find_etok(word):
    for x in etok_col.find({"word": word}, {"_id": False}):
        dic_to_str = ""
        for key, value in x.items():
            dic_to_str += key + ": " + value + "\n"

    ret_dic = {"Word": "", "Adjective": [], "Noun": [], "Verb": [], "Interjection": [], "Other": []}
    for line in dic_to_str.splitlines():
        if line.find("word") >= 0:
            ret_dic["Word"] = line.split(": ")[1]
        elif line.find("Adjective") >= 0:
            ret_dic["Adjective"].append(line.split("Adjective ")[1] + "\n")
        elif line.find("Noun") >= 0:
            ret_dic["Noun"].append(line.split("Noun ")[1] + "\n")
        elif line.find("Verb") >= 0:
            ret_dic["Verb"].append(line.split("Verb ")[1] + "\n")
        elif line.find("Interjection") >= 0:
            ret_dic["Interjection"].append(line.split("Interjection ")[1] + "\n")
        else:
            ret_dic["Other"].append(line.split(": ")[1] + "\n")
    return ret_dic


def check_etok(word):
    print("Checking DB for " + word)
    for x in etok_col.find({"word": word}, {"_id": False}):
        for key, value in x.items():
            if value == word:
                return True
            else:
                return False
