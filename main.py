from fastapi import FastAPI
from github import Github
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
gh = Github(os.getenv("GITHUB_TOKEN"))

@app.get("/commits/{username}")
def get_commits(username: str):
    user = gh.get_user(username)
    commits_summary = []
    for repo in user.get_repos():
        try:
            # commits = repo.get_commits()
            # for commit in commits[:5]:
            #     commits_summary.append({
            #         "repo": repo.name,
            #         "message": commit.commit.message,
            #         "date": commit.commit.author.date.isoformat()
            #     })
            commits_summary.append({
                "repo": repo.name,
                 "created_at": repo.created_at.isoformat()
            })
        except:
            continue
    return commits_summary
