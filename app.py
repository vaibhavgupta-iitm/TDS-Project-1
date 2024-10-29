import requests
import csv
import os
from dotenv import load_dotenv
import time

load_dotenv()

HEADERS = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
USER_SEARCH_URL = 'https://api.github.com/search/users'
USER_DETAILS_URL = 'https://api.github.com/users/{username}'
REPOS_URL = 'https://api.github.com/users/{username}/repos'



def fetch_users_in_beijing(page=1, per_page=100):
    users = []
    try:
        response = requests.get(f"{USER_SEARCH_URL}?q=location:beijing+followers:>500&per_page={per_page}&page={page}", headers=HEADERS)
        response.raise_for_status()
        users = response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching users: {e}")
    return users

def fetch_user_details(username):
    try:
        response = requests.get(USER_DETAILS_URL.format(username=username), headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user details for {username}: {e}")
        return {}

def save_users_csv(users):
    with open('users.csv', 'w', newline='') as csvfile:
        fieldnames = ['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            user_data = fetch_user_details(user['login'])
            if user_data:
                writer.writerow({
                    'login': user_data['login'],
                    'name': user_data.get('name', 'null'),
                    'company': clean_company_name(user_data.get('company', 'null')),
                    'location': user_data.get('location', 'null'),
                    'email': user_data.get('email', 'null'),
                    'hireable': user_data.get('hireable', False),
                    'bio': user_data.get('bio', 'null'),
                    'public_repos': user_data.get('public_repos', 0),
                    'followers': user_data.get('followers', 0),
                    'following': user_data.get('following', 0),
                    'created_at': user_data.get('created_at', 'null')
                })

def clean_company_name(company):
    if company:
        company = company.strip().lstrip('@').upper()
    return company

def fetch_user_repositories(username, per_page=100):
    repos = []
    page = 1
    try:
        while True and len(repos) <=500:
            response = requests.get(f"{REPOS_URL.format(username=username)}?per_page={per_page}&page={page}", headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            repos.extend(data)
            if len(data) < per_page:  
                break
            time.sleep(1)

            page += 1
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories for {username}: {e}")
    return repos[:500]

def save_repositories_csv(users):
    with open('repositories.csv', 'w', newline='') as csvfile:
        fieldnames = ['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            repos = fetch_user_repositories(user['login'])
            for repo in repos:
                writer.writerow({
                    'login': user['login'],
                    'full_name': repo['full_name'].split('/')[1],
                    'created_at': repo['created_at'],
                    'stargazers_count': repo['stargazers_count'],
                    'watchers_count': repo['watchers_count'],
                    'language': repo.get('language', 'null'),
                    'has_projects': repo.get('has_projects', False),
                    'has_wiki': repo.get('has_wiki', False),
                    'license_name': (repo.get('license') if isinstance(repo.get('license'), dict) else {}).get('key', 'null'),
                })
                print(f'{repo['full_name'].split('/')[1]} saved')

def main():
    page = 1
    all_users = []
    while True:
        users = fetch_users_in_beijing(page=page)
        if not users:
            break
        all_users.extend(users)
        page += 1
        time.sleep(1)
    print("all user fetched")
    save_users_csv(all_users)
    print("all user saved to user csv")
    save_repositories_csv(all_users)
    print("All repo saved to repo csv")
    print("Finished")

if __name__ == "__main__":
    main()
