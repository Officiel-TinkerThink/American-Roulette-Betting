# import important libraries
import copy
import random  # we use this to spin the wheel
from tabulate import tabulate
from anchor import * # anchor file for the program

# reward multiplier for each bet type
price_for_bets = {
                "single": 36,
                "double_vertical": 18,
                "double_horizontal": 18,
                "quadruple": 9,
                "row": 12,
                "column": 3,
                "a_third": 3,
                "a_half_number": 2,
                "a_half_color": 2,
                "odd_even_number": 2
                } #  format is (boolean(true=1)for the bet, price)

# user initial bets by default at every start of the game
user_initial_bets = {
                "single": [[], []],
                "double_vertical": [[], []],
                "double_horizontal": [[], []],
                "quadruple": [[], []],
                "row": [[], []],
                "column": [[], []],
                "a_third": [[], []],
                "a_half_number": [[], []],
                "a_half_color": [[], []],
                "odd_even_number": [[], []]
                } #  format is (indexofbetting, token_amount)


spin_result = {
            "single": [],
            "double_vertical": [],
            "double_horizontal": [],
            "quadruple": [],
            "row": [],
            "column": [],
            "a_third": [],
            "a_half_number": [],
            "a_half_color": [],
            "odd_even_number": []
            }

betting_result_template = {
                "single": [0, 0, 0],
                "double_vertical": [0, 0, 0],
                "double_horizontal": [0, 0, 0],
                "quadruple": [0, 0, 0],
                "row": [0, 0, 0],
                "column": [0, 0, 0],
                "a_third": [0, 0, 0],
                "a_half_number": [0, 0, 0],
                "a_half_color": [0, 0, 0],
                "odd_even_number": [0, 0, 0]
                } #  format is token_win_amount, price_per_token, total_price)


# making wheel database
color_dict = {"Green" : [0], "Red": list(a_half_color[0]), "Black" : list(a_half_color[1])}
number_dict = {i : "red" for i in list(a_half_color[0])}
addition_dict = {j : "black" for j in list(a_half_color[1])}
addition_dict_2 = {0 : "green"} # this line should become consideration to be implemented {int("00") produce 0 by computer}

# make number_dict_contain all the possible values and color pair
number_dict.update(addition_dict)
number_dict.update(addition_dict_2)

wheel_values = [str(x) for x in range(0,37)] + ["00"]


# SUB-3-MAIN FUNCTIONS

def slot_to_index(bet_type, value, reverse=False):
    """
    this will return the index of the slot placed when choosing slot
    and vice versa
    """
    # get the variable from the string
    bet_type = get_variable(bet_type)

    if reverse == True:
        slot = bet_type[value]
        return slot
    else:
        index = bet_type.index(value)
        return index
    
def input_slot_index(bet_type, pord):
    """
    prompt user for what index of slot they want to put
    return the user input
    """
    while True:
        try:
            user_input = int(input(f"Enter the index number of slot you want to {pord} bet :"))
        except ValueError:
            print("Invalid Input")
            continue
        if user_input >= slot_amount_dict[bet_type]:
            print("The number you enter is not available, it is too big")
        else:
            return user_input
    
def show_slot(bet_type):
    """
    This will show the slot available for each bet type. with format {index. slot}
    prompt user for what index of slot they want to put
    return the user input
    """
    print(f"Here is the list of slots available for {bet_type} bet type :")
    for i, v in enumerate(get_variable(bet_type)):
        if bet_type in four_item_in_row:
            if (i + 1)%4 != 0:
                print(f"{i}. {v}", end="  ")
            else:
                print(f"{i}. {v}")
        else:
            print(f"{i}. {v}")


def token_amount_input(available_token, prod):
    '''
    this will input the token for place and discard bet,
    it cannot be more than the amount user has
    
    '''
    while True:
        try:
            token_input = int(input("Enter the amount of token you want to place :"))
        except ValueError:
            print("Invalid Input")
            continue
        if token_input <= 0:
            print("The number you input have to be positive number")
        else:
            if prod == "place":
                if token_input > available_token:
                    print("You don't have enough tokens to place bet")
                else:
                    return token_input
            else:
                return token_input

def stop_or_continue(key):
    user_input = input(f"Type 'stop' to stop finish {key} session, others will make this to continue : ")
    if user_input.lower() == "stop":
        return True
    else:
        return False
            

# SUB-2-MAIN FUNCTION
def get_index(bet_type, num):
    '''
    this will return the index of the given num based on the given bet_type.
    return the list of possible indexes
    '''
    # make an empty list to store index value
    indexes = []
    # looping through all slots
    for i, slot in enumerate(get_variable(bet_type)):
        # if the number is in that slot, save the slot index into the indexes list
        if num in slot:
            indexes.append(i)
    return indexes

def money_token_conversion(amount: int, reverse=False):
    if reverse == True:
        amount = amount*10
    else:
        amount = amount//10
    return amount

def input_money_betting(index):
    '''
    this will allow user to input money to buy tokens, maximum 100 tokens (1000 money)
    return amount of tokens
    '''
    while True:
        try:
            message =\
            """Enter amount of money you want to traded with token
            Token price is $10.
            Money inputted should be multiple of 10 (cannot be: 19, 23, etc)
            the money inputted should be : 0 < amount < 1000"""
            print(message)
            user_input = int(input("Enter amount : "))
        except ValueError:
            print("Invalid Input")
            continue
        # check if meet the requirements
        if user_database[index]["balance"] < user_input:
            print("You don't have enough money in balance as much as the one you enter")
        elif user_input <= 0 or user_input > 1000 or user_input % 10 != 0:
            print("The amount you enter violates the requirement")
        else:
            # update balance
            user_database[index]["balance"] -= user_input
            return user_input

def show_current_slot(token, user_bets):
    '''
    this will show the current slots where user placing their bet on every slot and every bet_type
    it also count all the amount of placing token, and then substact it from user token
    return remaining_token
    '''
    placing_token = 0
    for bet_type in spin_result.keys():
        betting_amount_list = user_bets[bet_type][1]
        betting_amount_set = set(betting_amount_list)
        if len(betting_amount_list) != 0 or (len(betting_amount_set) == 1 and (0 in betting_amount_set)):
            print(f"In the {bet_type} bet type, user placing token :\n")
            for slot_index, num in zip(user_bets[bet_type][0], user_bets[bet_type][1]):
                if num != 0:
                    slot = slot_to_index(bet_type, slot_index, reverse=True)
                    print(f"User put {num} token in {slot}")
                    placing_token += num
    remaining_token = token - placing_token
    return remaining_token

def placing_bet(pord, remaining_token, user_bets):
    """
    in this function, display will direct users on placing a bet,
    including showing all the possible option for bet type,
    and displaying all the index for each slot that user can place.
    return remaining token
    """
    # looping for each placing or discard session
    pord_session = True
    while pord_session:
        # prompt all possible options for bet type and ask for user input what type of bet type to place
        betting_type_index = menu_display("betting_type_option", out_of_num=True)
        betting_type = bet_types[betting_type_index - 1]
        show_slot(betting_type)
        # looping for each slot choosing session
        choosing_slot_session = True
        while choosing_slot_session:
            # prompt all possible option for slot based on bet type, ask for user input where to bet
            bet_slot = input_slot_index(betting_type, pord)
            token_amount = token_amount_input(remaining_token, pord)
            # for placing case
            if pord == "place":
                if bet_slot in user_bets[betting_type][0]:
                    # if bet is already in user_bets list, just append the amount of it
                    index_sequence = user_bets[betting_type][0].index(bet_slot)
                    user_bets[betting_type][1][index_sequence] += token_amount
                else:
                    # if bet is not in user_bets list, add it to user_bets list
                    user_bets[betting_type][0].append(bet_slot)
                    user_bets[betting_type][1].append(token_amount)
                remaining_token -= token_amount
            # for discard case
            else:
                if bet_slot in user_bets[betting_type][0]:
                    # if bet is already in user_bets list
                    index_sequence = user_bets[betting_type][0].index(bet_slot)
                    # in case the available token is not enough to discard, so it's not possible to discard it
                    if token_amount > user_bets[betting_type][1][index_sequence]:
                        print("The amount you discard is more than the current available amount")
                    # in case it's possible to discard
                    else:
                        user_bets[betting_type][1][index_sequence] -= token_amount
                        remaining_token += token_amount
                else:
                    print("You cannot reap what you don't sow")

            print(f"You have {remaining_token} tokens left")
            # directly discard user from placing session
            if remaining_token == 0:
                choosing_slot_session = False
                pord_session = False
                continue
            # give user a chance to choose whether to continue or stop
            stop_slot_session = menu_display("stop_slot_option", out_of_num=True)
            if stop_slot_session == 2:
                choosing_slot_session = False
            elif stop_slot_session == 3:
                choosing_slot_session = False
                pord_session = False

    return remaining_token
        

# SUB-1-MAIN FUNCTION
def display_game(index):
    """Show the game welcoming page"""

    username = user_database[index]["username"]
    print(f"Welcome {username}, let's play the roullete")
    # it should be showing the roullete board picture from here


def spin_the_wheel():
    result = random.choice(wheel_values)
    num = int(result)
    color = number_dict[num]
    pair = [[result], [color]]
    print("The result of spinning the wheel is")
    print(tabulate(pair, tablefmt="grid"))
    return num

def process_result(user_bets, num):#user_bets):  # add user bets after the completion of the code
    # get all the bet_type
    bet_types = list(spin_result.keys())
    # looping through each bet type
    for bet_type in bet_types:
        # get the indexes of the winning slot based on the lucky number and save it to spin result
        indexes = get_index(bet_type, num)
        spin_result[bet_type] = indexes
    # initialize the betting result list
    betting_result = copy.deepcopy(betting_result_template)
    for bet_type in bet_types:
        # looping through each index of the winning slot
        for spin_index in spin_result[bet_type]:
            # initialize number of token that slot got right to zero
            right = 0
            # if spin_index is in user bets
            if spin_index in user_bets[bet_type][0]:
                # get the index of index of user_bet list
                bet_index = user_bets[bet_type][0].index(spin_index)
                # look for the token amount and increment right by that amount
                right += user_bets[bet_type][1][bet_index]
            # add the token win amount and price per token to the betting result list
            betting_result[bet_type][0] = right
            betting_result[bet_type][1] = price_for_bets[bet_type]
    # initialize bet amount token and payout token to zero
    bet_amount_token = 0
    payout_token = 0 
    for bet_type in bet_types:
        # get the total_price token and save it to betting_result, also increment the payout token
        outcome = betting_result[bet_type][0]*betting_result[bet_type][1]
        betting_result[bet_type][2] = outcome
        payout_token += outcome
        # get the total amount of bet token by summing all the token of each slot
        bet_amount_token += sum(user_bets[bet_type][1])
    return (bet_amount_token, payout_token, betting_result)



def betting(index):
    # initialize user bet
    user_bets = copy.deepcopy(user_initial_bets)
    # input money to bet and convert it to tokens, and update balance
    money_input = input_money_betting(index)
    start_token = money_token_conversion(money_input)
    print(f"You get {start_token} tokens from inputting ${money_input}")
    while True:
        # display the most update placing bet and amount
        # display current remaining tokens
        remaining_token = show_current_slot(start_token, user_bets)
        # ask whether user want to place bet or stop here
        user_input = menu_display("place_or_stop_option", out_of_num=True)
        if user_input == 1:
            # if user has no token left, user cannot place bet
            # if yes then show the place bet menu (place or discard)
            user_pord = menu_display("place_or_discard_option", out_of_num=True)
            if user_pord == 1:
                if remaining_token == 0:
                    print("You don't have any token left, you cannot place any bet anymore")
                    continue
                pord = "place"
            else:
                pord = "discard"
            remaining_token = placing_bet(pord, remaining_token, user_bets)
        # if no then stop here, and count the remaining tokens to be converted to money and give back to balance
        else:
            if remaining_token > 0:
                money = money_token_conversion(remaining_token)
                print(f"{remaining_token} tokens left to be converted into money: {money}, and send back to your wallet")
                user_database[index]["balance"] += money
            # to stop looping the betting because user say so
            return user_bets


# MAIN FUNCTION OF THE GAME
def play_game(user_id):
    # convert user_id into index to access user item from database
    users = [user["id"] for user in user_database]
    index = users.index(user_id)
    # looping for game session
    game_session = True
    while game_session == True:
        # welcome display(option to read the manual or just play game)
        user_input = menu_display("game_manual_or_play", out_of_num=True)
        if user_input == 1:
            print("click this link to go to game walktrough\n\n\n\n\n")
            continue
        elif user_input == 3:
            break
        # game display
        display_game(index)
        # betting session
        user_bets = betting(index)
        # spin the wheel
        lucky_number = spin_the_wheel()
        # process result, count the betting win based on the result
        bet_amount_token, payout_token, betting_result = process_result(user_bets, lucky_number)
        # print the betting detail (struck) in this session
        # create header for the bet detail nota
        headers_column = ["Token Win Amount", "Price per token", "Total Price"]
        headers_row = list(betting_result.keys())
        data = []
        for header in headers_row:
            data.append(betting_result[header])
        # print the betting detail (struck) in this session
        print(tabulate(data, headers=headers_column, showindex=headers_row, tablefmt="grid"))
        # show user how much they bet, and how much the payout in token
        print(f"in this session, You bet {bet_amount_token} tokens and get payout {payout_token} tokens")
        # print the betting detail (struck) in this session
        # convert the token into money
        payout_money = money_token_conversion(payout_token, reverse=True)
        bet_amount_money = money_token_conversion(bet_amount_token, reverse=True)
        # update user balance
        user_database[index]["balance"] += payout_money
        # update user transaction logs
        logs = user_database[index]["logs"]
        if len(logs) == 0:
            transaction_id = 0
        else:
            transaction_id = logs[-1]["id"] + 1
        item = {"id": transaction_id, "type": "bet", "amount": bet_amount_money, "payout": payout_money}
        user_database[index]["logs"].append(item)


