def user_input_type(user_input):
    if user_input.username and user_input.repo:
        return "username-repo"
    elif user_input.username:
        return "username"
    else:
        return "Invalid"   
