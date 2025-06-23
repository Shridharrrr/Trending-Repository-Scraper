import requests
from bs4 import BeautifulSoup
import csv

url = "https://github.com/trending"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    repos = soup.find_all('article', class_='Box-row')[:5]  # Get only top 5
    
    data = []
    for repo in repos:
        name_tag = repo.find('h2', class_='h3 lh-condensed')
        name = name_tag.get_text(strip=True).replace('\n', '').replace(' ', '') # Cleaning
        
        relative_link = name_tag.find('a')['href']
        link = "https://github.com{}".format(relative_link)
        
        data.append({'repository name': name, 'link': link})
    
    with open('Top5_TrendingRepos.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['repository name', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)
        
    print("Successfully saved top 5 trending repositories to 'Top5_TrendingRepos.csv'")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

