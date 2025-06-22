import argparse as ap
import requests

parser = ap.ArgumentParser(description="helps you retrieve github user info")
parser.add_argument("username", help="github username")
args = parser.parse_args()

# Keeping track of repos
repos = {}
repos['pushed'] = {}
repos['starred'] = []
repos['issues'] = []
repos['other_events'] = {}

def display_output(repos: dict):
    """
    Displays grouped infomation

    Args:
        repos (dict): Grouped information to display
    """

    if len(repos) == 0:
        print("User has no events in the last 30 days")
        return
    
    try:
        if repos:
            print("Output:")

            for event, content in repos.items():
                
                if len(content) == 0:
                    print(f"\t- {event} has no content in the last 30 days")
                
                if event == 'pushed':
                    for repo, count in content.items():
                        print(f"\t- Pushed {count} commit(s) to {repo}")
                
                if event == 'starred':
                    for repo in content:
                        print(f"\t- Starred {repo}")
                
                if event == 'other_events':
                    for repo in content:
                        print(f"\t- Other events: {repo}")

    except:
        print("Something went wrong")

def group_info(user_info: dict | list):
    """
    Groups retrived info of a given username

    Args:
        user_info (dict | list): Retrieved information to group
    """ 
    try:
        for data in user_info:

            event_name = data['type']
            repo_name = data['repo']['name']
            payload = data['payload']

            if event_name == 'PushEvent':
                if repo_name in repos['pushed']:
                    repos['pushed'][repo_name] += 1
                else:
                    repos['pushed'][repo_name] = 1
            elif event_name == 'WatchEvent':
                repos['starred'].append(repo_name)
            elif event_name == 'IssuesEvent':
                repos['issues'].append(repo_name)
            else:
                if repo_name in repos['other_events']:
                    repos['other_events'][event_name] += 1
                else:
                    repos['other_events'][event_name] = 1
            
        display_output(repos)
    except:
        print("Something went wrong")


def get_user_info(username: str):
    """
    Retrieves information for a given username

    Args:
        username (str): Username to retrieve information for
    """
    
    url = f"https://api.github.com/users/{username}/events"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            user_data = response.json()
            group_info(user_data)
        elif response.status_code == 404:
            print(f'{username} not found.')
        elif response.status_code == 502:
            print("Service is down, try again later")
    except:
        print("Something went wrong. Try again later")

try:
    if args:
        get_user_info(args.username)
except:
    print("Something went wrong")