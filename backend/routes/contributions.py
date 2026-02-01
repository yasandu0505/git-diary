from fastapi import APIRouter, Depends
from clients import GithubClient
from services import ContributionService
from models import GitHubTokenRequest

router = APIRouter()

@router.post("/contributed-repositories")
def get_contributed_repositories(
    payload: GitHubTokenRequest,
    service: ContributionService = Depends(),
    github_client: GithubClient = Depends()
):
    return service.get_contributed_repositories(
        token=payload.token,
        start_date=payload.start_date,
        end_date=payload.end_date,
        github_client=github_client
    )
