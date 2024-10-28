import requests
import csv
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

HEADERS = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
USER_SEARCH_URL = 'https://api.github.com/search/users'
USER_DETAILS_URL = 'https://api.github.com/users/{username}'
REPOS_URL = 'https://api.github.com/users/{username}/repos'
GITHUB_PROFILE_URL = 'https://github.com/{username}'
GITHUB_PROFILE_REPOS_URL = "https://github.com/{username}?tab=repositories"
USER_REPO_URL = "https://api.github.com/repos/{owner}/{repo}"

def fetch_users_in_beijing():

    response = requests.get("https://api.github.com/search/users?q=location:beijing+followers:>500",headers=HEADERS)
    return response.json().get('items', [])

def fetch_user_details(user):
    response = requests.get(GITHUB_PROFILE_URL.format(username=user), headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    user_response = requests.get(USER_DETAILS_URL.format(username=user), headers=HEADERS)
    user_response_json = user_response.json()

    user_data = {
        'login': user,
        'name': soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden').get_text(strip=True) if soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden') else '',
        'company': soup.find('span', class_='p-org').get_text(strip=True) if soup.find('span', class_='p-org') else '',
        'location': soup.find('span', class_='p-label').get_text(strip=True) if soup.find('span', class_='p-label') else '',
        'email': soup.find('a', href='mailto:').get_text(strip=True) if soup.find('a', href='mailto:') else '',
        'hireable': user_response_json['hireable'],  
        'bio': soup.find('div', class_='p-note user-profile-bio').get_text(strip=True) if soup.find('div', class_='p-note user-profile-bio') else '',
        'public_repos': int(soup.find('span', class_='Counter').get_text(strip=True)) if soup.find('span', class_='Counter') else 0,
        'followers': user_response_json['followers'],  
        'following': user_response_json['following'],  
        'created_at': user_response_json['created_at'],  
        'blog_url': user_response_json['blog'] 
    }

    return user_data
def transform_company(company):
    company = company.strip()
    company = company.lstrip('@')
    company = company.upper()

    return company

def save_users_csv(users):
    with open('users.csv','w', newline='') as csvfile:
        fieldnames = ['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at', 'blog_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            user_data = fetch_user_details(user['login'])
            writer.writerow({
                'login': user_data['login'],
                'name' : user_data['name'],
                'company' : transform_company(user_data['company']),
                'location' : user_data['location'],
                'email' : user_data['email'],
                'hireable' : user_data['hireable'],
                'bio' : user_data['bio'],
                'public_repos' : user_data['bio'],
                'followers' : user_data['followers'],
                'following' : user_data['following'],
                'created_at' : user_data['created_at'],
                'blog_url' : user_data['blog_url']
            })

def fetch_user_repositories(user):
    repos = []
    page = 1

    while len(repos) < 500:
        print("PAGE",page)
        url = GITHUB_PROFILE_REPOS_URL.format(username=user) + f"&page={page}"
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    
        repo_items = soup.find_all('li', class_='col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source', itemprop="owns")
        if not repo_items:
            break  

        for item in repo_items:
            repo_name = item.find('a', itemprop='name codeRepository').get_text(strip=True)
            print(repo_name)
            api_response = requests.get(USER_REPO_URL.format(owner=user,repo=repo_name),headers=HEADERS)
            api_response_json = api_response.json()

            star_html = soup.find('a', {'href': f'/{user}/{repo_name}/stargazers'})
            star_count_tag = None
            if(star_html):
                star_count_tag = soup.find('a', {'href': f'/{user}/{repo_name}/stargazers'}).get_text(strip=True)
            star_count = 0
            if star_count_tag:
                star_count = star_count_tag
            repo_stars = star_count
            repo_language = item.find('span', itemprop='programmingLanguage').get_text(strip=True) if item.find('span', itemprop='programmingLanguage') else 'N/A'
            repo_created_date = item.find('relative-time')['datetime'] if item.find('relative-time') else 'N/A'
            watchers_count = item.find('svg', class_='octicon-eye').text if item.find('svg', class_='octicon-eye') else '0'

            license_name = None
            license_span = item.find_all('span', class_='mr-3')
            for span in license_span:
                if span.find('svg', class_='octicon octicon-law mr-1'):
                    license_name = span.get_text(strip=True)
            repos.append({
                'login': user,
                'full_name': repo_name,
                'stargazers_count': repo_stars,
                'language': repo_language,
                'created_at': repo_created_date,
                'watchers_count': watchers_count,
                'license_name' : license_name,
                "has_projects": api_response_json['has_projects'], 
                "has_wiki": api_response_json['has_wiki'],
            })

        page += 1

    return repos[:500]


def save_repositories_csv(users):
    print("inside  save repository")
    with open('repositories.csv', 'w', newline='') as csvfile:
        fieldnames = ['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            repos = fetch_user_repositories(user['login'])
            for repo in repos:
                writer.writerow(repo)
            break
        

def main():
    users = fetch_users_in_beijing()
    # save_users_csv(users)
    save_repositories_csv(users)

if __name__ == "__main__":
    main()
