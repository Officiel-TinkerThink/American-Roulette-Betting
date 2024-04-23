# import important libraries
from tabulate import tabulate
from game import *

## SHOW DATABASE
def show_user_database(key="account", user_id=None):
	headers = list(user_database[0].keys())#.insert(0, "Index")
	if key == "account":
		headers = headers[0:3]
	elif key == "balance":
		indexes = [1, 3]
		headers = [headers[index] for index in indexes]
	row_format ="|{:<20} " * len(headers) + "|"
	print(row_format.format(*headers))
	if user_id != None:
		index = [user["id"] for user in user_database].index(user_id)
		print(row_format.format(*[user_database[index][header] for header in headers]))
	else:
		for user in user_database:
			print(row_format.format(*[user[header] for header in headers]))


def account_change(index, key="both", user_id=None):
	print("change from :")
	show_user_database(user_id=user_id)
	if key=="both":
		edit_user(key="username", index=index)
		edit_user(key="password", index=index)
	else:
		edit_user(key=key, index=index)
	print("to :")
	show_user_database(user_id=user_id)



## LOGIN HELPER FUNCTION
def edit_user(key, index):
	new_key = input(f"Enter The new proposed {key}: ")
	old_key = user_database[index][key]
	if old_key == new_key:
		print(f"The new {key} is the same with the old one")
	elif new_key in [user[key] for user in user_database]:
		print(f"There already another account with that {key}")
	else:
		user_database[index][key] = new_key
	

def user_login():
	verification = False
	for i in range(3):
		username = input("username : ")
		usernames = [user["username"] for user in user_database]
		if username in usernames:
			password = input("password : ")
			index = usernames.index(username)
			if user_database[index]["password"] == password:
				verification = True
				break
			else:
				print("Sorry, You entered wrong password, please try again")
		else:
			print("Sorry, there is no such username. Please try again")
	if verification == True:
		return user_database[index]["id"]
	else:
		print("You already given 3 chances but still failed to login, so move you back to frontier menu")
		return False


def admin_login():
	verification = False
	for i in range(3):
		password = input("password : ")
		if admin["password"] == password:
			verification = True
			break
		else:
			print("Sorry, You entered wrong password, please try again")
	if verification == True:
		return True
	else:
		print("You already given 3 chances but still failed to login, so move you back to frontier menu")
		return False
	

def user_id_check():
	"""
	This function cover the prompt for user_id and transaction_id, and screening it
	return the id and index
	"""
	while True:
		try:
			id = int(input("Enter id of the account: "))
		except ValueError:
			print("Invalid input")
			continue
		user_ids = [user["id"] for user in user_database]
		if not id in user_ids:
			print("There is no user with such id")
		else:
			return id, user_ids.index(id)
		

def admin_menu():
	# loop admin menu prompt
	while True:
		# display admin menu and asking for user input for what option to choose
		user_input = menu_display("admin_menu_welcoming", out_of_num=True)
		if user_input == 1:
			show_user_database()
		elif user_input == 2:
			while True:
				new_username = input("Enter username for new account: ")
				usernames = [user["username"] for user in user_database]
				if new_username in usernames:
					print("There is already user with that username, please enter novel username")
				else:
					new_password = input("Enter username password: ")
					if new_password in [user["password"] for user in user_database]:
						print("There already account with that password")
					else:
						new_id =user_database[-1]["id"] + 1
						new_user = {"id": new_id, "username": new_username, "password": new_password, "balance": 1000, "logs": []}
						user_database.append(new_user)
						print("Succesfully added new users")
						show_user_database(user_id=new_id)
						break
		elif user_input == 3:
			show_user_database()
			# ask user to input user_id and screening it
			user_id, index = user_id_check()
			edit_option = menu_display("edit_user_option", out_of_num=True)
			if edit_option == 1:
				account_change(key="username", user_id=user_id, index=index)
			elif edit_option == 2:
				account_change(key="password", user_id=user_id, index=index)
			elif edit_option == 3:
				account_change(user_id=user_id, index=index)
			else:
				print("You Enter the wrong input, automatically exit ")
		elif user_input == 4:
			show_user_database()
			user_id, index = user_id_check()
			user_database.pop(index)
			print("account has been removed")
			show_user_database()
		elif user_input == 5:
			break


## MAIN MENU HELPER FUNCTION
def quit_prompt():
	user_input = menu_display("quit_prompt_option")
	if user_input == 1:
		return False
	elif user_input == 2:
		return True
	else:
		print("Sorry, you enter the wrong input, it leads the program to ended")
		return True


def transact(user_id, key="deposit"):
	while True:
		try:
			transaction_amount = int(input(f"Enter the amount you want to {key}, it should be positive integer between 0 and 100000: "))
		except ValueError:
			print("Sorry, you entered the wrong input")
			continue
		# notes: further development should consider to only accept whole amount, not float conversion to int. it's two different thing
		if transaction_amount <= 0 or transaction_amount > 100000:
			print("the amount you enter doesn't meet the requirement. it either too small or too big")
		else:
			user_ids = [user["id"] for user in user_database]
			index = user_ids.index(user_id)
			if key == "withdraw":
				if transaction_amount > user_database[index]["balance"] - 1000:
					print("You don't have enough money to withdraw, you minimally have to had 1000 dollars left after you withdraw")
					break
				else:
					transaction_amount = -transaction_amount
			user_database[index]["balance"] += transaction_amount
			print(f"Succesfully Process the {key}")
			show_user_database(key="balance", user_id=user_id)
			logs = user_database[index]["logs"]
			if len(logs) == 0:
				transaction_id = 0
			else:
				transaction_id = logs[-1]["id"] + 1
			item = {"id": transaction_id, "type": key, "amount": abs(transaction_amount), "payout" : None }
			transaction_id += 1
			#increment_transaction_id()
			user_database[index]["logs"].append(item)
			break


def transaction(user_id):

	# looping the session
	while True:
		# display transaction option
		user_input = menu_display("transaction_option", out_of_num=True)
		if user_input == 1:
			transact(user_id)
		elif user_input == 2:
			transact(user_id, key="withdraw")
		elif user_input == 3:
			break
	
def search_transaction_by_id(user_id):
	user_ids = [user["id"] for user in user_database]
	index = user_ids.index(user_id)
	logs = user_database[index]["logs"]
	if len(logs) == 0:
		print("You have no logs yet, so you apply search by id")
		return
	while True:
		try:
			user_input = (input("Please enter the target transaction id, or enter 'd' to abrupt stop: "))
			transaction_id = int(user_input)
		except ValueError:
			if user_input in ["d", "D"]:
				return
			print("Invalid input, please try again")
			continue
		if transaction_id > logs[-1]["id"]:
			print("There is no transaction with such id")
		else:
			headers = {"id":"id", "type":"type", "amount":"amount", "payout":"payout"}
			print(tabulate([logs[transaction_id]], headers=headers, tablefmt="grid"))
			return


def show_history(user_id, key=None, parameter=None, reverse=False):
	user_ids = [user["id"] for user in user_database]
	index = user_ids.index(user_id)
	logs = user_database[index]["logs"]
	if key == "filter":
		logs = filter()
	elif key == "sort":
		logs = sorted(logs, key=lambda x: x[parameter], reverse=reverse)
	headers = {"id":"id", "type":"type", "amount":"amount", "payout":"payout"}
	print(tabulate(logs, headers=headers, tablefmt = "grid"))


def history_interface(user_id):
	while True:
		user_input = menu_display("history_display", out_of_num=True)
		if user_input == 1:
			show_history(user_id)
		elif user_input == 2:
			sort = menu_display("sort_option",out_of_num=True)
			sequence_input = menu_display("asc_desc", out_of_num=True)
			if sequence_input == 1:
				reverse = False
			elif sequence_input == 2:
				reverse = True
			# else:
			# 	print("Sorry, you enter the wrong input, your sequence are automatically selected to ascending order")
			# 	reverse = False
			if sort == 1:
				show_history(user_id, key="sort", parameter="id", reverse=reverse)
			elif sort == 2:
				show_history(user_id, key="sort", parameter="type", reverse=reverse)
			elif sort == 3:
				show_history(user_id, key="sort", parameter="amount", reverse=reverse)
			elif sort == 4:
				show_history(user_id, key="sort", parameter="payout", reverse=reverse)
			# else:
			# 	print("Sorry, you input the wrong input, automatically send you the previous page")
		elif user_input == 3:
			print("This feature is not implemented yet")
		elif user_input == 4:
			search_transaction_by_id(user_id)
		elif user_input == 5:
			break
            

## MAIN MENU MAIN FUNCTION
def main_menu(user_id):
    # loop main menu prompt
	while True:
		# display main menu and asking for user input for what option to choose
		user_input = menu_display("main_menu_welcoming", out_of_num=True)
		# if 1 then show the dashboard
		if user_input == 1:
			show_user_database(key="balance", user_id=user_id)
		# if 2 then process the transaction, which is deposit and withdrawal
		elif user_input == 2:
			transaction(user_id)
		# if 3 then play the Game
		elif user_input == 3:
			play_game(user_id)
		# if 4 process the walkthrough
		elif user_input == 4:
			history_interface(user_id)
		# if 5 exit the main menu.
		elif user_input == 5:
			user_feedback = quit_prompt()
			return user_feedback