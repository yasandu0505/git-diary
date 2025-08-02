def user_input_type(user_input):
    if user_input.username and user_input.repo and user_input.from_date and user_input.to_date:
        return "username-repo-date-range"
    elif user_input.username and user_input.repo:
        return "username-repo"
    elif user_input.username:
        return "username"
    else:
        return "Invalid"   
