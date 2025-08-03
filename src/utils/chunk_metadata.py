import json
from datetime import datetime, timedelta
from collections import defaultdict

def chunk_commits_by_business_weeks(commits_data, internship_start_date):
    """
    Chunk commits by business weeks starting from internship start date.
    
    Args:
        commits_data (dict): Dictionary with repo names as keys and commit lists as values
        internship_start_date (str): Start date in format 'YYYY-MM-DD'
    
    Returns:
        dict: Chunked commits by business weeks
    """
    
    # Parse the start date
    start_date = datetime.strptime(internship_start_date, '%Y-%m-%d').date()
    
    # Flatten all commits with repository info
    all_commits = []
    for repo_name, commits in commits_data.items():
        for commit in commits:
            # Parse the ISO date string
            commit_date = datetime.fromisoformat(commit['date'].replace('Z', '+00:00')).date()
            
            all_commits.append({
                **commit,
                'repository': repo_name,
                'date_obj': commit_date
            })
    
    # Sort commits by date (ascending)
    all_commits.sort(key=lambda x: x['date_obj'])
    
    # Filter commits from internship start date onwards
    relevant_commits = [c for c in all_commits if c['date_obj'] >= start_date]
    
    if not relevant_commits:
        return {}
    
    # Group commits by business weeks
    weeks = {}
    week_number = 1
    
    # Calculate first week boundaries
    current_week_start = start_date
    current_week_end = get_week_end_date(current_week_start, start_date)
    
    # Process commits
    i = 0
    while i < len(relevant_commits):
        week_commits = []
        
        # Collect commits for current week
        while i < len(relevant_commits) and relevant_commits[i]['date_obj'] <= current_week_end:
            # Only include commits on business days (Monday=0 to Friday=4)
            if relevant_commits[i]['date_obj'].weekday() < 5:
                commit_copy = relevant_commits[i].copy()
                # Remove the date_obj as it's not needed in output
                del commit_copy['date_obj']
                week_commits.append(commit_copy)
            i += 1
        
        # Add week to results if it has commits
        if week_commits:
            weeks[f"week_{week_number}"] = {
                "period": f"{current_week_start.strftime('%Y-%m-%d')} to {current_week_end.strftime('%Y-%m-%d')}",
                "commits": week_commits
            }
        
        # Move to next week
        week_number += 1
        current_week_start = get_next_monday(current_week_end)
        current_week_end = current_week_start + timedelta(days=4)  # Friday
        
        # Break if no more commits to process
        if i >= len(relevant_commits):
            break
    
    return weeks

def get_week_end_date(week_start, actual_start):
    """
    Get the end date of a business week.
    If starting mid-week, end on Friday of that week.
    """
    # Find the Friday of the week containing week_start
    days_until_friday = (4 - week_start.weekday()) % 7
    if week_start.weekday() > 4:  # If weekend, go to next Friday
        days_until_friday = (4 - week_start.weekday()) % 7 + 7
    
    friday = week_start + timedelta(days=days_until_friday)
    return friday

def get_next_monday(current_date):
    """Get the next Monday after the given date."""
    days_until_monday = (7 - current_date.weekday()) % 7
    if days_until_monday == 0:  # If current_date is Monday
        days_until_monday = 7
    return current_date + timedelta(days=days_until_monday)

