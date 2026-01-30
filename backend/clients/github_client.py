import requests
import logging

logger = logging.getLogger(__name__)

class GithubClient:
    # github graphql api endpoint
    GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

    # graphQL query to fetch commits authored by a user across repositories
    GRAPHQL_QUERY = """
    query($username: String!) {
    user(login: $username) {
        contributionsCollection {
        commitContributionsByRepository(maxRepositories: 100) {
            repository {
            name
            fullName: nameWithOwner
            url
            owner {
                login
            }
            isPrivate
            createdAt
            updatedAt
            }
        }
        }
    }
    }
    """

    def __init__(self):
        pass


    def _headers(self, token: str):
        return {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def _payload(self, username: str):
        return {
            "query": self.GRAPHQL_QUERY,
            "variables": {"username": username}
        }
    
    def fetch_contributed_repositories(self, token: str, username: str):
        logger.info(f"Fetching contributed repositories for user '{username}'")
        contributions = requests.post(self.GITHUB_GRAPHQL_URL, json=self._payload(username), headers=self._headers(token))
        if contributions.status_code != 200:
            logger.error(f"Failed to fetch contributed repositories for user '{username}'")
            logger.error(f"Status Code: {contributions.status_code}")
            raise HTTPException(status_code=contributions.status_code, detail=contributions.text)
        logger.info(f"Successfully fetched contributed repositories for user '{username}'") 
        logger.info(f"Status Code: {contributions.status_code}")
        return contributions.json()
