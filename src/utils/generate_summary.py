from dotenv import load_dotenv
import os
import google.generativeai as genai
from datetime import datetime, timedelta
import json
from collections import defaultdict
from src.LLM import COMMIT_PREPROCESSING_PROMPT

load_dotenv()
api_key = os.environ.get("API_KEY")

# Configure Gemini AI
genai.configure(api_key=api_key)

def generate_summary_from_commits(chunked_commits_data):
    """
    Generate a weekly diary summary from chunked commits data organized by business days
    
    Args:
        chunked_commits_data (dict): Dictionary containing weekly commit data
            Expected format: {"week_X": {"period": "date_range", "commits": [...]}}
    
    Returns:
        dict: Dictionary with daily summaries for each business day
    """
    print(f"Processing weekly commits data...")
    
    if not chunked_commits_data:
        return {"error": "No commits data provided."}
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    weekly_diary = {}
    
    for week_key, week_data in chunked_commits_data.items():
        print(f"Processing {week_key}...")
        
        commits = week_data.get('commits', [])
        if not commits:
            continue
            
        # Group commits by date (business days only)
        daily_commits = defaultdict(list)
        
        for commit in commits:
            commit_date = commit.get('date', '')
            if commit_date:
                try:
                    # Parse the date from ISO format
                    date_obj = datetime.fromisoformat(commit_date.replace('Z', '+00:00'))
                    date_str = date_obj.strftime('%Y-%m-%d')
                    
                    # Only include business days (Monday=0 to Friday=4)
                    if date_obj.weekday() < 5:
                        daily_commits[date_str].append(commit)
                        
                except ValueError:
                    print(f"Error parsing date: {commit_date}")
                    continue
        
        # Generate summary for each business day
        week_diary = {}
        
        for date_str in sorted(daily_commits.keys()):
            day_commits = daily_commits[date_str]
            
            # Format commits for the AI prompt
            commit_details = []
            for i, commit in enumerate(day_commits, 1):
                message = commit.get('message', 'No message')
                repository = commit.get('repository', 'Unknown repo')
                author = commit.get('author', 'Unknown author')
                commit_details.append(f"{i}. [{repository}] {message} (by {author})")
            
            commits_text = "\n".join(commit_details)
            
            # Create the prompt for Gemini
            prompt = COMMIT_PREPROCESSING_PROMPT.format(
                commits_text=commits_text,
                date=date_str,
                commit_count=len(day_commits)
            )
            
            try:
                # Generate the summary using Gemini
                response = model.generate_content(prompt)
                
                # Parse date for day name
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                day_name = date_obj.strftime('%A')
                formatted_date = date_obj.strftime('%B %d, %Y')
                
                week_diary[date_str] = {
                    'day_name': day_name,
                    'formatted_date': formatted_date,
                    'commit_count': len(day_commits),
                    'summary': response.text.strip(),
                    'repositories': list(set([commit.get('repository', 'Unknown') for commit in day_commits]))
                }
                
                print(f"Generated summary for {day_name}, {formatted_date}")
                
            except Exception as e:
                print(f"Error generating summary for {date_str}: {str(e)}")
                week_diary[date_str] = {
                    'day_name': datetime.strptime(date_str, '%Y-%m-%d').strftime('%A'),
                    'formatted_date': datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y'),
                    'commit_count': len(day_commits),
                    'summary': f"Error generating summary: {str(e)}",
                    'repositories': []
                }
        
        weekly_diary[week_key] = {
            'period': week_data.get('period', ''),
            'daily_summaries': week_diary
        }
    
    return weekly_diary

def generate_formatted_weekly_report(weekly_diary):
    """
    Generate a formatted markdown report from the weekly diary data
    
    Args:
        weekly_diary (dict): Dictionary containing weekly diary data
    
    Returns:
        str: Formatted markdown report
    """
    report_lines = ["# 📅 Weekly Development Diary", ""]
    
    for week_key, week_data in weekly_diary.items():
        if 'daily_summaries' not in week_data:
            continue
            
        report_lines.extend([
            f"## {week_key.replace('_', ' ').title()} ({week_data.get('period', 'Unknown period')})",
            ""
        ])
        
        daily_summaries = week_data['daily_summaries']
        
        # Sort by date
        for date_str in sorted(daily_summaries.keys()):
            day_data = daily_summaries[date_str]
            
            report_lines.extend([
                f"### {day_data['day_name']}, {day_data['formatted_date']}",
                "",
                day_data['summary'],
                "",
                f"**📊 Commits:** {day_data['commit_count']} commits",
                f"**📁 Repositories:** {', '.join(day_data['repositories'])}",
                "",
                "---",
                ""
            ])
    
    return "\n".join(report_lines)