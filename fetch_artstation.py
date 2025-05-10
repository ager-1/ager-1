import requests
from bs4 import BeautifulSoup
import re
import logging

USERNAME = "aghazakhtar"
URL = f"https://www.artstation.com/{USERNAME}"
LIMIT = 3  # number of projects

logging.basicConfig(level=logging.INFO)

def fetch_latest_projects():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        projects = soup.find_all('li', class_='gallery-item')[:LIMIT]
        lines = []
        for proj in projects:
            title = proj.find('a', class_='project-title').text.strip()
            link = proj.find('a', class_='project-title')['href']
            thumb = proj.find('img', class_='image')['src']
            lines.append(f"!{title}")
        logging.info("Successfully fetched projects")
        return "\n".join(lines)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching projects: {e}")
        return "Error fetching projects"

def update_readme(new_content):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    updated = re.sub(
        r"<!-- ARTSTATION:START -->(.*?)<!-- ARTSTATION:END -->",
        f"<!-- ARTSTATION:START -->\n{new_content}\n<!-- ARTSTATION:END -->",
        readme,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    content = fetch_latest_projects()
    update_readme(content)
