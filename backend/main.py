from fastapi import FastAPI
from clients import GithubClient
from services import ContributionService
from models import GitHubTokenRequest
import logging
from settings import setup_logging

setup_logging()
github_client = GithubClient()
contribution_service = ContributionService()

app = FastAPI(title="Git Diary")

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Application started")

@app.post("/contributed-repositories")
def get_contributed_repositories(payload: GitHubTokenRequest):
    return contribution_service.get_contributed_repositories(
        token=payload.token,
        start_date=payload.start_date,
        end_date=payload.end_date,
        github_client=github_client
    )