# GitHub User and Repository Data in Beijing

- This project scrapes GitHub profiles of users in Beijing with more than 500 followers, along with details on their public repositories.
- After analyzing the data, we found that a significant portion of active developers in Beijing focus on open-source projects in Python and JavaScript.
- Developers targeting a Beijing-based audience should consider tailoring content in these languages to maximize engagement with this community.

## Data Collection Process

This script collects data using the GitHub API. It first fetches users in Beijing with over 500 followers, then retrieves detailed information about each user and their repositories, respecting rate limits and paginated API requests.

### Key Features

- **User Data**: Extracts user details including name, company, location, bio, number of followers, and public repositories.
- **Repository Data**: Retrieves details of each repository such as language, license, and popularity metrics (stars and watchers).
- **Rate Limiting**: The code includes delays between requests to respect GitHub’s API rate limits.

## Usage

1. Clone the repository and install required dependencies:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   pip install -r requirements.txt
