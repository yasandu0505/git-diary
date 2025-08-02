from github import Github
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from .load_config import load_config_file


load_dotenv()
gh = Github(os.getenv("GITHUB_TOKEN"))

def get_repo_metadata(username: str):
    user = gh.get_user(username)
    commits_summary = []
    
    config = load_config_file()

    time_zone = config["time"]["time_zone"]
    
    repos = sorted(user.get_repos(), key=lambda r: r.updated_at, reverse=True)
    
    for repo in repos:
        try:
            local_created = repo.created_at.astimezone(ZoneInfo(time_zone))
            local_updated = repo.updated_at.astimezone(ZoneInfo(time_zone))
            commit_count = repo.get_commits(sha="main").totalCount
            commits_summary.append({
                "repo": repo.name,
                "created_at": local_created.isoformat(),
                "update_at": local_updated.isoformat(),
                "commit_count_on_main": commit_count
            })
        except:
            continue
    return commits_summary



def get_commits_from_repo(username: str, reponame: str):
    try:
        user = gh.get_user(username)
        repo = user.get_repo(reponame)
        
        config = load_config_file()
        
        time_zone = config["time"]["time_zone"]
        
        # Get all commits from main branch
        commits = repo.get_commits(sha="main")
        commits_list = []
        
        for commit in commits:
            commit_data = commit.commit
            local_date = commit_data.author.date.astimezone(ZoneInfo(time_zone))
            
            commits_list.append({
                "sha": commit.sha,
                "message": commit_data.message,
                "author": commit_data.author.name,
                "author_email": commit_data.author.email,
                "date": local_date.isoformat(),
                "url": commit.html_url
            })
        
        return {
            "repository": repo.name,
            "total_commits": commits.totalCount,
            "commits": commits_list
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch commits: {str(e)}"}


def get_commits_from_repo_with_date_filters(username: str, reponame: str):
    print("1")
    repo_commits_metadata = get_commits_from_repo(username,reponame)
    print("2")
    
    return repo_commits_metadata