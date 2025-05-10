import requests
import re

USERNAME = "aghazakhtar"
URL = f"https://www.artstation.com/users/{USERNAME}/projects.json"
LIMIT = 3  # number of projects

def fetch_latest_projects():
    response = requests.get(URL)
    projects = response.json()['data'][:LIMIT]
    lines = []
    for proj in projects:
        title = proj['title']
        link = proj['permalink']
        thumb = proj['cover']['small_image_url']
        lines.append(f"[![{title}]({thumb})]({link})")
    return "\n".join(lines)

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
