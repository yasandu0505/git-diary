import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="DailyDev")

    parser.add_argument('--username', type=str, required=True, help='Your Github username')
    parser.add_argument('--repo', type=str, required=False, help='Your Repo name (my-project)')
    parser.add_argument('--from', dest='from_date', type=str, required=False, 
                   help='Start date for filtering commits (format: YYYY-MM-DD, e.g., 2024-01-01)')
    parser.add_argument('--to', dest='to_date', type=str, required=False, 
                   help='End date for filtering commits (format: YYYY-MM-DD, e.g., 2024-01-31)')
    

    return parser.parse_args()
