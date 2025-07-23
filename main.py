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
            # commits = repo.get_commits()
            # for commit in commits[:5]:
            #     commits_summary.append({
            #         "repo": repo.name,
            #         "message": commit.commit.message,
            #         "date": commit.commit.author.date.isoformat()
            #     })
            
            local_created = repo.created_at.astimezone(ZoneInfo(time_zone))
            local_updated = repo.updated_at.astimezone(ZoneInfo(time_zone))
            commits_summary.append({
                "repo": repo.name,
                "created_at": local_created.isoformat(),
                "update_at": local_updated.isoformat()
            })
        except:
            continue
    return commits_summary
