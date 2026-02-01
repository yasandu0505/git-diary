import logging
from datetime import datetime
from utils import normalize_created_date

logger = logging.getLogger(__name__)

class ContributionService:
    def __init__(self):
        self.contributions = {}
    
    def get_contributed_repositories(self, token: str, github_client, start_date=None, end_date=None):
        contributed_repositories = github_client.fetch_contributed_repositories(token, "yasandu0505")
        repositories = contributed_repositories["data"]["user"]["contributionsCollection"]["commitContributionsByRepository"]
        
        if start_date and end_date:
            start = datetime.strptime(str(start_date), "%Y-%m-%d").date()
            end = datetime.strptime(str(end_date), "%Y-%m-%d").date()

            logger.info(f"Filtering repositories between {start} and {end}")

            normalized_repos = normalize_created_date(repositories)

            filtered_repos = [
                repo for repo in normalized_repos
                if start <= repo["repository"]["createdAt"] <= end
            ]
            logger.info(f"Successfully filtered repositories")
            return filtered_repos
        
        logger.info("Fetching contributions for all time")
        return repositories
    


        


    

    
   