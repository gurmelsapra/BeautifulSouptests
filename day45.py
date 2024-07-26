import requests
from bs4 import BeautifulSoup

# Fetch the HTML content of the Hacker News front page
response = requests.get("https://news.ycombinator.com/news")
yc_web_page = response.text

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(yc_web_page, "html.parser")

# Extract titles and scores
titles = soup.find_all("td", class_="title")
scores = soup.find_all("span", class_="score")

# Initialize lists to store extracted information
title_links = []
title_scores = []

# Extract titles and links
for title in titles:
    titleline = title.find("span", class_="titleline")
    if titleline:
        link = titleline.find("a")
        if link:
            title_text = link.get_text()
            href = link['href']
            title_links.append((title_text, href))

# Extract scores (scores appear in reverse order compared to titles)
score_elements = soup.find_all("span", class_="score")
for i, score in enumerate(score_elements):
    if i < len(title_links):  # Ensure we don't go out of bounds
        title_text, href = title_links[i]
        print(f"{title_text} ({href}) - {score.get_text()}")

# In case there are titles without scores or scores without titles, we can handle them here:

if len(score_elements) > len(title_links):
    print("\nScores without titles:")
    for i in range(len(title_links), len(score_elements)):
        print(f"Score: {score_elements[i].get_text()} - No title available")
