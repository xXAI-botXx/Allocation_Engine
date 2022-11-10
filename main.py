import os
import sys
import random
from datetime import datetime as dt

from replit import db

# create db
#db['password'] = ""
#db['history'] = ""
#db['access_token'] = []
#db['allocations'] = []
#exit()

################
# Constants
################
HEX = "0123456789ABCDEF"
LENGTH = 5

# load secrets
password = db['password']


################
# Functions
################
def check_and_take_access_token(check_code: str):
    # load tokens
    access_token = db['access_token']

    if check_code in access_token:
        del access_token[access_token.index(check_code)]
        # save new tokens
        db['access_token'] = access_token
        return True
    else:
        return False


def get_allocations():
    return db['allocations']


def check_master():
    user_input = input("Type Password:")
    #if user_input == os.environ['Master-Password']:
    if user_input == password:
        return True
    else:
        return False


def create_access_token():
    if check_master() == True:
        # get old codes
        access_token = db['access_token']

        # get new codes
        amount = int(input("Amount of access codes:"))
        print("The new access-codes are:")
        for i in range(amount):
            new_token = random.choices(HEX, k=LENGTH)
            print(f"{''.join(new_token) + ','}")
            access_token += [''.join(new_token)]

        # save all codes
        db['access_token'] = access_token

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
                for i in [
                        'tobia', 'matteo', 'alex', 'rosa', 'niklas', 'luisa',
                        'sebi', 'alena'
                ]:
                    names[i] = ""
                break
            else:
                names[user_input] = ""
        presenter = list(names.keys())
        giving = list(names.keys())

        # allocate names
        is_wrong_allocation = True
        while is_wrong_allocation:
            for i in giving:
                rand_ = random.choice(presenter)
                #while rand_ == i:
                #rand_ = random.choice(presenter)
                names[i] = presenter.pop(presenter.index(rand_))
            # check allocation
            alright = True
            keys = []
            values = []
            for key, value in names.items():
                if key == value or key in keys or value in values:
                    alright = False
                    break

                keys += [key]
                values += [value]

            if alright == True:
                is_wrong_allocation = False
            else:
                presenter = list(names.keys())
                giving = list(names.keys())

        # save all allocation
        #allocations = ""
        #for key, value in names.items():
        #    allocations += f"{key}:{value},"

        db['allocations'] = names

        # create empty history file
        db['history'] = ""

        input("\nIt's finished. Press enter to continue.")


def remove_access_token():
    if check_master() == True:
        db['access_token'] = []


def show_access_token():
    if check_master() == True:
        print(db['access_token'])


def show_history():
    print(db['history'])
    input("\nDrücke Enter um fortzufahren.")


################
# Main Logic
################
commands = {
    'new allocation': lambda: create_new_allocation(),
    'new access': lambda: create_access_token(),
    'remove access': lambda: remove_access_token(),
    'show access': lambda: show_access_token(),
    'exit': lambda: sys.exit(),
    'history': lambda: show_history()
}

while True:
    user_input = input("Gib deinen Code ein:")
    if user_input in commands.keys():
        commands[user_input]()
    else:
        if check_and_take_access_token(user_input) == True:
            access_token_ = user_input
            allocations = get_allocations()

            is_false_name = True
            while is_false_name:
                name = input("Gib deinen Vornamen ein:").lower()
                if name in allocations.keys():
                    print(
                        f"Hey {name.title()}, du hast {allocations[name].title()} gezogen.\n\nMerke dir die Person gut! Und sag niemanden,wer die gezogene Person ist."
                    )
                    db['history'] += f"\n- {dt.now().day}.{dt.now().month}.{dt.now().year} {dt.now().hour}:{dt.now().minute} Uhr {access_token_} {name.title()}"
                    input("\nDu kannst die Website einfach schließen.")
                    break
                else:
                    print(
                        "Der Name wurde leider nicht gefunden. Versuche es erneut oder kontaktiere meinen Programmierer -> Tobia."
                    )
