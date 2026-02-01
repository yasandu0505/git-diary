from datetime import datetime

def normalize_created_date(repos):
    """
    Normalizes the created date of repositories to a datetime object.
    """
    for item in repos:
        repo = item["repository"]
        repo["createdAt"] = datetime.fromisoformat(
            repo["createdAt"].replace("Z", "")
        ).date()
    return repos
