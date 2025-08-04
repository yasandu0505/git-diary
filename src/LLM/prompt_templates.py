COMMIT_PREPROCESSING_PROMPT = """
Analyze the following git commits for a single day and create a concise daily summary.

Date: {date}
Total Commits: {commit_count}

Format the response as a brief daily work summary:

✅ **Work Completed:**
- [Brief summary of main accomplishments - 2-4 bullet points max]
- [Group related commits into logical work items]
- [Focus on features, fixes, or improvements made]

🔧 **Technical Focus:**
- [Key technical areas worked on]
- [Technologies or components modified]

💡 **Key Changes:**
- [Most significant changes or additions]
- [Any notable debugging or optimization work]

Requirements:
- Keep it concise and professional
- Focus on the business value of the work done
- Group similar commits together
- Highlight the most important accomplishments
- Use clear, action-oriented language
- Maximum 6-8 bullet points total across all sections

Commits to analyze:
{commits_text}

Create a focused daily summary following the format above.
"""