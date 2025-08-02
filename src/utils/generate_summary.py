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
    
    # Format commits for the AI prompt - they're simple strings
    commit_details = []
    for i, commit in enumerate(commits, 1):
        commit_details.append(f"{i}. {commit}")
    
    commits_text = "\n".join(commit_details)
    
    # Create the prompt for Gemini
    prompt = f"""
    As a developer's coding diary assistant, analyze the following git commits and create a personal diary entry summary. 
    
    Write in a reflective, personal tone as if the developer is writing in their diary about their coding day. 
    Focus on:
    - What was accomplished today
    - Key features or improvements made
    - Any challenges or interesting solutions
    - Overall progress and feelings about the work
    
    Commits from today:
    {commits_text}
    
    Create a diary entry that starts with "Dear Diary," and summarizes the coding session in a personal, reflective manner. 
    Keep it concise but meaningful (2-3 paragraphs). Make it sound human and personal, not technical.
    """
    
    try:
        # Generate the summary using Gemini
        response = model.generate_content(prompt)
        
        # Add date header to the diary entry
        today = datetime.now().strftime("%B %d, %Y")
        diary_entry = f"# Coding Diary - {today}\n\n{response.text}"
        
        return diary_entry
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return f"Error generating diary summary: {str(e)}"
