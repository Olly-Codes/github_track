import argparse as ap
import requests

parser = ap.ArgumentParser(description="helps you retrieve github user info")
parser.add_argument("username", help="github username")
args = parser.parse_args()

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
            return user_data
        else:
            return f"Failed to retrieve data for: {username}"
    except:
        print("Something went wrong")

try:
    if args:
        user_info = get_user_info(args.username)
        if user_info:
            display_info(user_info)
except:
    print("Something went wrong")

