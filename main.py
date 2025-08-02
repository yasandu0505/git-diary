from src.utils import get_repo_metadata, get_commits_from_repo, get_commits_from_repo_with_date_filters, generate_summary_from_commits
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
        
    if user_input_typee == "username-repo-date-range":
        commits = []
        
        repo_commits_metadata_with_date_range = get_commits_from_repo_with_date_filters(user_input.username, user_input.repo, user_input.from_date, user_input.to_date)
        
        for commit in repo_commits_metadata_with_date_range['commits']:
            commit_message = commit['message'].replace('\n\n', ' - ')
            commit_date = commit['date']
            commits.append({
                'date': commit_date,
                'message': commit_message
                })
        
        diary_entry = generate_summary_from_commits(commits)
        print(diary_entry)
        
        sys.exit(1)
    
    
if __name__ == "__main__":
    main()