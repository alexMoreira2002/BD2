import os
import uuid
import pymongo
import bcrypt
import json
from pathlib import Path
from lxml import etree
from datetime import date
from BD2app.database import MongoConn
# Connect to the MongoDB database
mongo_client = pymongo.MongoClient(MongoConn.ConnString)['BD2Project']


def insertUser(name, username, password, role):
    if not mongo_client['Users'].find_one({'username': username}):
        doc_id = str(uuid.uuid4())  # Generate a random ID
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        doc = {"_id": doc_id, 'name': name, 'username': username,
               'password': hashed_password, 'role': role}
        mongo_client['Users'].insert_one(doc)
        return True
    else:
        print('User already exists')
        return False


def login(username, password):
    user = mongo_client['Users'].find_one({'username': username})
    hashed_password = user['password']
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False


def logout():
    return True


def getUsers():
    if mongo_client['Users'].find():
        return True
    else:
        return False


def getUserByID(userID):
    user = mongo_client['Users'].find_one({'_id': userID})
    return user


def getUser(username, password):
    user = mongo_client['Users'].find_one({'username': username})
    if user is None:
        print('User does not exist')
        return False
    elif bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user['_id']
    else:
        print('Invalid password')
        return False


def getUserRole(userID):
    user = mongo_client['Users'].find_one({'_id': userID})
    return user['role']


def updateUser(userID, username, newPassword):
    if not mongo_client['Users'].find_one({'username': username}):
        hashed_password = bcrypt.hashpw(
            newPassword.encode('utf-8'), bcrypt.gensalt())
        mongo_client['Users'].update_one(
            {'_id': userID}, {'$set': {'username': username, 'password': hashed_password}})
        return True
    else:
        print('User already exists')
        return False

def updateUserPassword(userID, newPassword):
    hashed_password = bcrypt.hashpw(
        newPassword.encode('utf-8'), bcrypt.gensalt())
    mongo_client['Users'].update_one(
        {'_id': userID}, {'$set': {'password': hashed_password}})
    return True

def deleteUser(username):
    mongo_client['Users'].delete_one({'username': username})
    return True


def getUsersByRole(role):
    users = mongo_client['Users'].find({'role': role})
    return users

def exportUsersToJson():
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    product = mongo_client['Users'].find({}, {'password': 0})
    cur_path = os.path.dirname(__file__)
    file_path = os.path.join(cur_path, '..\\static\\json\\Users_'+d1+'.json')
    print(f"Current ---->{cur_path}")
    print(f"Final ---->{file_path}")
    try:
        with open(file_path, 'w') as f:
            json.dump(list(product), f)
        return file_path
    except:
        return False

def exportUsersToXML():
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    product = mongo_client['Users'].find({}, {'password': 0})
    cur_path = os.path.dirname(__file__)
    file_path = os.path.join(cur_path, '..\\static\\xml\\Users_' + d1 + '.xml')
    print(f"Current ---->{cur_path}")
    print(f"Final ---->{file_path}")
    with open(file_path, 'w') as f:
        root = etree.Element('Users')
        for doc in product:
            product = etree.SubElement(root, 'User')
            for key, value in doc.items():
                child = etree.SubElement(product, key)
                child.text = str(value)
        tree = etree.ElementTree(root)
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding='utf-8')
    return file_path
