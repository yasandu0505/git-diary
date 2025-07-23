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
