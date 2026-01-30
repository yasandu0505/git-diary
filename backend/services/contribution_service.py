class ContributionService:
    def __init__(self):
        self.contributions = {}
    
    def get_contributed_repositories(self, token: str, github_client, start_date=None, end_date=None):
        contributed_repositories = github_client.fetch_contributed_repositories(token, "yasandu0505")
        return contributed_repositories

        


    

    
   