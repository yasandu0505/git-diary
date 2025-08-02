from dotenv import load_dotenv
import os
import google.generativeai as genai
from datetime import datetime
import json
from src.LLM import COMMIT_PREPROCESSING_PROMPT

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
    prompt = COMMIT_PREPROCESSING_PROMPT.format(commits_text=commits_text)
    
    try:
        # Generate the summary using Gemini
        response = model.generate_content(prompt)
        
        # Return the formatted summary without additional date header
        return response.text
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return f"Error generating diary summary: {str(e)}"