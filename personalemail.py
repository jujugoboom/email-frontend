"""
   DESCRIPTION

   file: 
   author: Justin Covell
   created: 11/28/2015
"""
import requests
import json
import time
import configparser
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
Config = configparser.ConfigParser()
Config.read('config.ini')
API_KEY = Config.get('MailGun', 'api_key')
MAIL_URL = Config.get('MailGun', 'url')
EMAIL = Config.get('MailGun', 'email')
HEROKU_URL = Config.get('Heroku', 'url')
USERNAME = Config.get('Heroku', 'username')
PASSWORD = Config.get('Heroku', 'password')

def send_message():
    to = str(input("To: "))
    subject = str(input("Subject: "))
    message = str(input("Message: "))
    requests.post(
        MAIL_URL,
        auth=("api", API_KEY),
        data={"from": EMAIL,
              "to": to,
              "subject": subject,
              "text": message})
    print("Message Sent!")


def get_stored(id):
    return requests.get(HEROKU_URL, auth=(USERNAME , PASSWORD), headers = {'id' : id})

def delete_message(id):
    return requests.delete(HEROKU_URL, auth=(USERNAME , PASSWORD), headers = {'id' : id})

def print_message(j):
    print()
    print('--------------------------------------------')
    print('From: ' + j['fields']['sender'])
    print('Subject: ' + j['fields']['subject'])
    print('Received: ' + time.strftime('%m-%d-%Y %H:%M:%S',time.localtime(j['fields']['timestamp'])))
    print('Attachments: ' + bytes(str(j['fields']['attachments']).encode('ascii', 'ignore')).decode('ascii'))
    print()
    print(j['fields']['message'])
    input('Press ENTER to continue')

def print_messages(messagedict):
    print()
    print("Recieved Messages")
    print('--------------------------------------------')
    i = 1
    for item in messagedict:
        print(str(i) + ' ', end='')
        print("From: ", end='')
        print(item['fields']['sender'],end='')
        print(" Subject: ", end='')
        print(item['fields']['subject'])
        i += 1
    print()

def print_message_data(messagedict, i):
    print("From: ", end='')
    print(messagedict[i]['fields']['sender'],end='')
    print(" Subject: ", end='')
    print(messagedict[i]['fields']['subject'])

def get_messages():
    id = 0
    response = get_stored(id).text
    if response == 'No Messages':
        print("No Messages")
        print()
        return
    j = json.loads(json.loads(response))
    while True:
        print_messages(j)
        k = str(input("Message Number, (N)ext Page, (P)revious Page, (D)elete Message or (E)xit: ")).lower()
        if k.isdigit():
            i = int(k) - 1
            if i in range(len(j)):
                print_message(j[i])
            else:
                print('Invalid Selection')
        elif k == 'n':
            id += 50
            j = json.loads(get_stored(id).text)
        elif k == 'p':
            if id >= 50:
                id -= 50
            else:
                id=0
            j = json.loads(get_stored(id).text)
        elif k == 'd':
            i = int(input('Which message: '))
            print('Are you sure you want to delete: ')
            print_message_data(j, i-1)
            selection = str(input('Y/N: ')).lower()
            if selection == 'y':
                delete_message(i-1)
                response = get_stored(id).text
                if response == 'No Messages':
                    print("No Messages")
                    print()
                    return
            j = json.loads(json.loads(response))
        elif k == 'e':
            break
        else:
            print('Invalid Selection')

def main():
    while True:
        k = str(input('(S)end New Email, (V)iew Recieved Emails, or (E)xit: ')).lower()
        if k == 's':
            send_message()
        elif k == 'v':
            get_messages()
        elif k == 'e':
            break
        else:
            print('Invalid Selection')


if __name__ == '__main__':
    main()
