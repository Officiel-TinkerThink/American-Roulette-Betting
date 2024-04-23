from sub_main import *
# from anchor import * 


# loop for login prompt
while True:
    # display login prompt and asking for user input for what option to choose
    user_input = menu_display("login_welcoming", out_of_num=True)
    # if 1, try to login as user
    if user_input == 1:
        # user_login would return the username if successful, and return false if not
        user_id = user_login()
        if user_id:
            # after user quit from the main menu, it will return feedback (whether user want to quit from app, or just want to go back to login interface)
            feedback = main_menu(user_id)
            if feedback == True:
                break
    # if 2, try to login as admin
    elif user_input == 2:
        # 
        verification = admin_login()
        if verification == True:
            admin_menu()
    # if 3, try to quit the app
    elif user_input == 3:
        print("thank you for coming, see you next time")
        break
