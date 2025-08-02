COMMIT_PREPROCESSING_PROMPT = """
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
    