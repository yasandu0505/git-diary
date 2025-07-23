from fastapi import FastAPI
from github import Github
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
import yaml

load_dotenv()
app = FastAPI()
gh = Github(os.getenv("GITHUB_TOKEN"))

@app.get("/commits/{username}")
def get_commits(username: str):
    
    user = gh.get_user(username)
    commits_summary = []
    
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

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

@app.get("/commits/{username}/{reponame}")
def get_commits(username: str, reponame: str):
    try:
        user = gh.get_user(username)
        repo = user.get_repo(reponame)
        
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
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
