from github import Github
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from .load_config import load_config_file
from datetime import datetime
import inquirer
import json
import os

load_dotenv()
gh = Github(os.getenv("GITHUB_TOKEN"))

def get_repo_metadata(username: str):
   user = gh.get_user(username)
   commits_summary = []
   
   config = load_config_file()
   time_zone = config["time"]["time_zone"]
   start_date_of_internship = config["user_data"]["start_date"]
   
   # Parse start date (assuming it's a string in ISO format)
   if isinstance(start_date_of_internship, str):
       start_date = datetime.fromisoformat(start_date_of_internship).replace(tzinfo=ZoneInfo(time_zone))
   else:
       start_date = start_date_of_internship
   
   repos = user.get_repos()
   
   for repo in repos:
       try:
           local_created = repo.created_at.astimezone(ZoneInfo(time_zone))
           local_updated = repo.updated_at.astimezone(ZoneInfo(time_zone))
           
           # Filter repos created since internship start
           if local_created >= start_date:
               commit_count = repo.get_commits(sha="main").totalCount
               commits_summary.append({
                   "repo": repo.name,
                   "created_at": local_created.isoformat(),
                   "update_at": local_updated.isoformat(),
                   "commit_count_on_main": commit_count
               })
       except:
           continue
   
   # Sort ascending by created date
   commits_summary.sort(key=lambda x: x["created_at"])
   
   # Interactive repo selection
   if commits_summary:
       repo_choices = [f"{repo['repo']} ({repo['commit_count_on_main']} commits)" for repo in commits_summary]
       
       questions = [
           inquirer.Checkbox(
               'selected_repos',
               message="Select repos to track for diary (use SPACE to select, ENTER to confirm)",
               choices=repo_choices,
           ),
       ]
       
       answers = inquirer.prompt(questions)
       selected_repo_names = [choice.split(' (')[0] for choice in answers['selected_repos']]
       
       # Filter commits_summary to only selected repos
       selected_repos_metadata = [repo for repo in commits_summary if repo['repo'] in selected_repo_names]
       
       # Save to JSON file
       tracking_data = {
           "tracked_repos": selected_repos_metadata,
           "last_updated": datetime.now(ZoneInfo(time_zone)).isoformat(),
           "internship_start": start_date.isoformat()
       }
       
       # create metadata dir if not exists
       commits_dir = 'metadata'
       os.makedirs(commits_dir, exist_ok=True)
       
       with open('metadata/tracked_repos.json', 'w') as f:
           json.dump(tracking_data, f, indent=2)
       
       print(f"\nSaved {len(selected_repos_metadata)} tracked repos to metadata/tracked_repos.json")
       fetch_and_save_commits_for_tracked_repos(username)
       
       return selected_repos_metadata
   
   else:
       print("No repos found since internship start date")
       return []



def get_commits_from_repo(username: str, reponame: str):
    try:
        user = gh.get_user(username)
        repo = user.get_repo(reponame)
        
        config = load_config_file()
        
        time_zone = config["time"]["time_zone"]
        
        # Get all commits from main branch
        commits = repo.get_commits(sha="main")
        commits_list = []
        my_commits = 0
        
        for commit in commits:
            commit_data = commit.commit
            author_name = commit_data.author.name
            
            if author_name == username:
                my_commits += 1
            else:
                continue
            
            local_date = commit_data.author.date.astimezone(ZoneInfo(time_zone))
            
            commits_list.append({
                "sha": commit.sha,
                "message": commit_data.message,
                "author": commit_data.author.name,
                "author_email": commit_data.author.email,
                "date": local_date.isoformat(),
                "url": commit.html_url
            })
        
        return {
            "repository": repo.name,
            "total_commits": commits.totalCount,
            "my_commits": my_commits,
            "commits": commits_list
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch commits: {str(e)}"}




def fetch_and_save_commits_for_tracked_repos(username: str):    
    # Load tracked repos from metadata file
    try:
        with open('metadata/tracked_repos.json', 'r') as f:
            tracking_data = json.load(f)
        tracked_repos = tracking_data.get('tracked_repos', [])
    except FileNotFoundError:
        print("No tracked repos found. Please run get_repo_metadata first.")
        return
    except json.JSONDecodeError:
        print("Error reading tracked repos file.")
        return
    
    if not tracked_repos:
        print("No tracked repositories found.")
        return
    
    # Create commits directory if it doesn't exist
    commits_dir = 'commits'
    os.makedirs(commits_dir, exist_ok=True)
    
    successful_fetches = 0
    failed_fetches = 0
    
    print(f"Fetching commits for {len(tracked_repos)} repositories...")
    
    for repo_metadata in tracked_repos:
        repo_name = repo_metadata['repo']
        print(f"Fetching commits for {repo_name}...")
        
        # Get commits for this repository
        commits_data = get_commits_from_repo(username, repo_name)
        
        if 'error' in commits_data:
            print(f"❌ Failed to fetch commits for {repo_name}: {commits_data['error']}")
            failed_fetches += 1
            continue
        
        # Add metadata to the commits data
        commits_data['metadata'] = {
            'fetched_at': datetime.now(ZoneInfo('UTC')).isoformat(),
            'repo_created_at': repo_metadata['created_at'],
            'repo_updated_at': repo_metadata['update_at'],
            'username': username
        }
        
        # Save commits to separate JSON file for each repo
        filename = f"{commits_dir}/{repo_name}_commits.json"
        try:
            with open(filename, 'w') as f:
                json.dump(commits_data, f, indent=2)
            print(f"✅ Saved {commits_data['my_commits']} commits for {repo_name} to {filename}")
            successful_fetches += 1
        except Exception as e:
            print(f"❌ Failed to save commits for {repo_name}: {str(e)}")
            failed_fetches += 1
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Successfully processed: {successful_fetches} repositories")
    print(f"   ❌ Failed: {failed_fetches} repositories")
    
    return {
        'successful': successful_fetches, 
        'failed': failed_fetches,
        'total': len(tracked_repos)
    }


def get_commits_from_repo_with_date_filters(username: str, reponame: str, from_date: str, to_date: str):
    
    repo_commits_metadata = get_commits_from_repo(username,reponame)
    
    # Convert filter dates to datetime objects
    from_datetime = datetime.strptime(from_date, '%Y-%m-%d')
    to_datetime = datetime.strptime(to_date, '%Y-%m-%d')
    
    filtered_commits = []
    
    for commit in repo_commits_metadata['commits']:
        # Extract just the date part from commit date string
        # '2025-07-23T18:13:08+05:30' -> '2025-07-23'
        commit_date_only = commit['date'].split('T')[0]
        commit_datetime = datetime.strptime(commit_date_only, '%Y-%m-%d')
        
        # Compare dates (including both from_date and to_date)
        if from_datetime <= commit_datetime <= to_datetime:
            filtered_commits.append(commit)
    
    return {
        'repository': repo_commits_metadata['repository'],
        'total_commits': len(filtered_commits),
        'commits': filtered_commits
    }