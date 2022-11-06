#from datetime import datetime as dt
#import pywhatkit as whatsapp
#numb = "+49 1575 XXXXXXX"
#whatsapp.sendwhatmsg(numb, "Message 2", dt.now().hour, dt.now().minute+1)

import os
import sys
import random
from cryptography.fernet import Fernet

################
# Constants
################
HEX = "0123456789ABCDEF"
LENGTH = 5
fernet = Fernet(os.environ['crypt-key'])


################
# Functions
################
def check_and_take_access_token(check_code:str):
    # load tokens
    with open('access_token.txt', "r") as f:
        lines = f.read()
    raw_access_token = str(fernet.decrypt(lines).decode())
    
    # transform tokens in dict
    access_token = raw_access_token.split(",")
    if access_token[-1] == '':
        access_token = access_token[:-1]
        
    result = dict()
    for i in access_token:
        result[i] = ""
        
    if check_code in result.keys():
        del result[check_code]
        # save new tokens
        with open("./access_token.txt", "w") as f:
            access_token = ','.join(list(result.keys()))+","
            f.write(str(fernet.encrypt(access_token.encode()))[2:-1])
        return True
    else:
        return False


def get_allocations():
    with open('secret.txt') as f:
        lines = f.read()
    raw_allocations = str(fernet.decrypt(lines).decode())
    elements_allocations = raw_allocations.split(",")
    if elements_allocations[-1] == '':
        elements_allocations = elements_allocations[:-1]
    allocations = dict()
    for i in elements_allocations:
        key, value = i.split(":")
        allocations[key] = value
    return allocations


def check_master():
    user_input = input("Type Password:")
    if user_input == os.environ['Master-Password']:
        return True
    else:
        return False


def create_access_token():
    if check_master() == True:
        # get old codes
        with open("access_token.txt", "r") as f:
            access_token = f.read()
        access_token = str(fernet.decrypt(access_token).decode())

        # get new codes
        amount = int(input("Amount of access codes:"))
        print("The new access-codes are:")
        for i in range(amount):
            new_token = random.choices(HEX, k=LENGTH)
            print(f"\n{''.join(new_token) + ','}")
            access_token += ''.join(new_token) + ","

        # save all codes
        with open("./access_token.txt", "w") as f:
            f.write(str(fernet.encrypt(access_token.encode()))[2:-1])

        input("\nIt's finished. Press enter to continue.")


def create_new_allocation():
    if check_master() == True:
        # get names
        names = dict()
        while True:
            user_input = input("Name (press enter to continue):").lower()
            if user_input == "" or user_input == "exit":
                break
            elif user_input == "family set":
                for i in ['tobia', 'matteo', 'alex', 'rosa', 'niklas', 'luisa', 'sebi', 'alena']:
                    names[i] = ""
                break
            else:
                names[user_input] = ""
        presenter = list(names.keys())
        giving = list(names.keys())

        # allocate names
        for i in giving:
            rand_ = random.choice(presenter)
            while rand_ == i:
                rand_ = random.choice(presenter)
            names[i] = presenter.pop(presenter.index(rand_))

        # save all allocation
        allocations = ""
        for key, value in names.items():
            allocations += f"{key}:{value},"
            
        with open("./secret.txt", "w") as f:
            f.write(str(fernet.encrypt(allocations.encode()))[2:-1])

        input("\nIt's finished. Press enter to continue.")

def remove_access_token():
    if check_master() == True:
        with open("access_token.txt", "w") as f:
            f.write(str(fernet.encrypt("".encode()))[2:-1])

def show_access_token():
    if check_master() == True:
        with open("access_token.txt", "r") as f:
            access_token = f.read()
        access_token = str(fernet.decrypt(access_token).decode())
        print(access_token)
        


################
# Main Logic
################
commands = {
    'new allocation': lambda: create_new_allocation(),
    'new access': lambda: create_access_token(),
    'remove access': lambda: remove_access_token(),
    'show access': lambda: show_access_token(),
    'exit': lambda: sys.exit()
}

while True:
    user_input = input("Gib deinen Code ein:")
    if user_input in commands.keys():
        commands[user_input]()
    else:
        if check_and_take_access_token(user_input) == True:
            allocations = get_allocations()
            
            is_false_name = True
            while is_false_name:
                name = input("Gib deinen Vornamen ein:").lower()
                if name in allocations.keys():
                    print(
                        f"Hey {name.title()}, du hast {allocations[name].title()} gezogen. Merke dir die Person gut! Und sag niemanden,wer die gezogene Person ist."
                    )
                    input("Du kannst die Website einfach schließen.")
                    break
                else:
                    print(
                        "Der Name wurde leider nicht gefunden. Versuche es erneut oder kontaktiere meinen Programmierer -> Tobia."
                    )
