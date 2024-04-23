from message import *
from roulette_database import *

# CREATE DATABASE FOR USERS AND ADMIN
user_database = [
	   			{"id": 1,"username": "a", "password": "a", "balance": 1000, "logs": []},
				{"id": 2, "username": "sadiomane", "password": "allhailsenegal", "balance": 1000, "logs": []},
				{"id": 3, "username": "mosalah", "password": "youllneverwalkalone", "balance": 1000, "logs": []},
				{"id": 4,"username": "mesutoezil", "password": "comeonyougunners", "balance": 1000, "logs": []},
				]

admin = {"username": "godofgamble", "password": "go"}

# this dict is for message option num, you have to update this every time you add something to the message file
message_option_num_dict = {"login_welcoming": 3, "main_menu_welcoming": 5, "admin_menu_welcoming": 4, "transaction_option" : 3, "history_display": 5, "sort_option": 4, "asc_desc": 2, "filter_option": 4,
								"filter_spec_num": 6, "filter_spec_cat": 4, "transaction_option": 3, "edit_user_option": 3, "quit_prompt_option": 2, "transaction_option": 3, "place_or_stop_option": 2,
								"place_or_discard_option": 2, "betting_type_option": 10, "game_manual_or_play": 3, "stop_slot_option": 3,
								}

# Global variable for transaction_ID to increment time by time
transaction_id = 0

# INCREMENT THE GLOBAL VARIABLE FUNCTIONS
def increment_transaction_id():
    global transaction_id
    transaction_id += 1

# GET THE VARIABLE NAME FROM STRING
def get_variable(string_input):
    """
    this will return the variable from the string input
    """
    variable = globals()[string_input]
    return variable

## MENU DISPLAY HELPER FUNCTION
def menu_display(message: str, out_of_num=False):
	while True:
	# print welcoming message and menu list
		print(get_variable(message))
		# asking for user input for menu list
		try:
			user_input = int(input("Enter the option number you want to run : "))
		except ValueError:
			print("Invalid Input")
			continue
		if user_input > message_option_num_dict[message] or user_input <= 0:
			if out_of_num == False:
				return False
			else:
				print("The number you enter is not in the option, please enter the correct one")
		else:
			return user_input
