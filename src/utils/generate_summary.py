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
    Analyze the following git commits and create a professional work summary in the exact format shown below. and do not hallucinate

    Format the response as:
    ✅ **Summary of Work Completed:**
    In this week, I focused on [brief overview]. Below is a breakdown of the work I completed:

    [Number each major area of work with detailed bullet points using * for sub-items]

    📌 **Key Focus Areas:**
    * [List 3-4 main categories of work done]

    Requirements:
    - Group related commits into logical sections
    - Use professional, clear language
    - Include specific technical details from commit messages
    - Start each major section with a numbered header
    - Use bullet points with * for sub-items
    - End with key focus areas summary
    - Be comprehensive but well-organized

    Commits to analyze:
    {commits_text}

    Generate a professional work summary following the exact format above.
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
