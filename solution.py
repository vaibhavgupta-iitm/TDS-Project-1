import pandas as pd
from scipy.stats import pearsonr, linregress

# Load data
users_df = pd.read_csv('users.csv')
repos_df = pd.read_csv('repositories.csv')

# Question 1
top_5_followers = users_df.nlargest(5, 'followers')['login'].tolist()
print("Users:", ", ".join(top_5_followers))

# Question 2
earliest_5_users = users_df.sort_values(by='created_at').head(5)['login'].tolist()
print("Users:", ", ".join(earliest_5_users))

# Question 3
top_3_licenses = repos_df['license_name'].dropna().value_counts().nlargest(3).index.tolist()
print("Licenses:", ", ".join(top_3_licenses))

# Question 4
majority_company = users_df['company'].dropna().value_counts().idxmax()
print("Company:", majority_company)

# Question 5
most_popular_language = repos_df['language'].dropna().value_counts().idxmax()
print(repos_df['language'].dropna().value_counts())
print("Language:", most_popular_language)

# Question 6
post_2020_df = users_df[users_df['created_at'] >= '2020-01-01']
second_most_popular_language_post_2020 = repos_df[repos_df['login'].isin(post_2020_df['login'])]['language'].dropna().value_counts().nlargest(2).index[1]
print("Language:", second_most_popular_language_post_2020)

# Question 7
average_stars_language = repos_df.groupby('language')['stargazers_count'].mean().idxmax()
print("Language:", average_stars_language)

# Question 8
users_df['leader_strength'] = users_df['followers'] / (1 + users_df['following'])
top_5_leader_strength = users_df.nlargest(5, 'leader_strength')['login'].tolist()
print("User login:", ", ".join(top_5_leader_strength))

# Question 9
followers_repos_corr, _ = pearsonr(users_df['followers'], users_df['public_repos'])
print("Correlation between followers and repos:", f"{followers_repos_corr:.3f}")

# Question 10
slope, _, _, _, _ = linregress(users_df['public_repos'], users_df['followers'])
print("Regression slope of followers on repos:", f"{slope:.3f}")

# Question 11
projects_wiki_corr, _ = pearsonr(repos_df['has_projects'].astype(int), repos_df['has_wiki'].astype(int))
print("Correlation between projects and wiki enabled:", f"{projects_wiki_corr:.3f}")

# Question 12
hireable_following_diff = users_df.groupby('hireable')['following'].mean().diff().iloc[-1]
print("Average following difference:", f"{hireable_following_diff:.3f}")

# Question 13
users_df['bio_word_count'] = users_df['bio'].fillna('').apply(lambda x: len(x.split()))
slope_bio_followers, _, _, _, _ = linregress(users_df[users_df['bio_word_count'] > 0]['bio_word_count'], users_df[users_df['bio_word_count'] > 0]['followers'])
print("Regression slope of followers on bio word count:", f"{slope_bio_followers:.3f}")

# Question 14
repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])
repos_df['is_weekend'] = repos_df['created_at'].dt.weekday >= 5
weekend_repos = repos_df[repos_df['is_weekend']].groupby('login').size().nlargest(5).index.tolist()
print("Users login:", ", ".join(weekend_repos))

# Question 15
hireable_email_ratio = users_df[users_df['hireable']]['email'].notna().mean() - users_df[~users_df['hireable']]['email'].notna().mean()
print("Email fraction difference:", f"{hireable_email_ratio:.3f}")

# Question 16
users_df['surname'] = users_df['name'].fillna('').apply(lambda x: x.split()[-1] if x else None)
most_common_surnames = users_df['surname'].value_counts().nlargest(1)
most_common_surname = most_common_surnames[most_common_surnames == most_common_surnames.max()].index.sort_values().tolist()
print("Surname:", ", ".join(most_common_surname))
print("Number of users with the most common surname:", most_common_surnames.max())
