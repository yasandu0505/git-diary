from src.utils import get_repo_metadata, get_commits_from_repo
from src.cmd import parse_args, user_input_type
import sys

def main():
    
    user_input = parse_args()
    
    user_input_typee = user_input_type(user_input)
    
    if user_input_typee == "Invalid":
        print("Invalid input, try --help")
        sys.exit(1)
    
    if user_input_typee == "username":
        repo_metadata = get_repo_metadata(user_input.username)
        for repo in repo_metadata:
            print(repo)
            print("\n")
        sys.exit(1)
        
    if user_input_typee == "username-repo":
        repo_commits_metadata = get_commits_from_repo(user_input.username, user_input.repo)
        print(repo_commits_metadata)
        sys.exit(1)

if __name__ == "__main__":
    main()