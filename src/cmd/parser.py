import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="DailyDev Programme")

    parser.add_argument('--username', type=str, required=True, help='Your Github username')
    parser.add_argument('--repo', type=str, required=False, help='Your Repo name (my-project)')

    return parser.parse_args()
