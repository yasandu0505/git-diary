from dotenv import load_dotenv
import os
import google.generativeai as genai
from datetime import datetime
import json

load_dotenv()
api_key = os.environ.get("API_KEY")

# Configure Gemini AI
genai.configure(api_key=api_key)

def generate_summary_from_commits(commits):
    """
    Generate a diary page summary from an array of commit messages using Gemini AI
    
    Args:
        commits (list): Array of commit message strings
        
    Returns:
        str: A diary-style summary of the commits
    """
    print(f"Processing {len(commits)} commits...")
    
    if not commits:
        return "No commits found for today."
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Format commits for the AI prompt - they're dict objects with date and message
    commit_details = []
    for i, commit in enumerate(commits, 1):
        date = commit.get('date', 'Unknown date')
        message = commit.get('message', 'No message')
        commit_details.append(f"{i}. [{date}] {message}")
    
    commits_text = "\n".join(commit_details)
    
    # Create the prompt for Gemini
    prompt = f"""
    Analyze the following git commits and create a summary organized by date. 

    Format the response as:
    
    # 📅 Development Summary by Date

    For each date found in the commits, create a section like this:
    ## [Day Name], [Date] (e.g., "Tuesday, July 23, 2025")
    
    ✅ **Work Completed:**
    - [Brief summary of what was accomplished]
    - [Group related commits into logical points]
    - [Include specific features/changes made]

    📊 **Commits:** [number] commits

    ---

    Requirements:
    - Group commits by their date (extract date from timestamp)
    - Show the day name (Monday, Tuesday, etc.) and full date
    - Provide a concise summary for each day's work
    - List 3-5 key accomplishments per day
    - Use bullet points for easy reading
    - Include commit count for each day
    - Sort dates chronologically (oldest first)

    Commits to analyze:
    {commits_text}

    Create a date-organized summary following the exact format above.
    """
    
    try:
        # Generate the summary using Gemini
        response = model.generate_content(prompt)
        
        # Return the formatted summary without additional date header
        return response.text
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return f"Error generating diary summary: {str(e)}"