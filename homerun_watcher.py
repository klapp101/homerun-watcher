# Requests / Wrangling and MLB API
import requests
from bs4 import BeautifulSoup
import statsapi # https://github.com/toddrob99/MLB-StatsAPI/wiki
import pandas as pd

# Web Scraping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Interacting with Browser for HRs
import asyncio
from pyppeteer import launch

# Dates
from datetime import datetime


params = {
    'recordID': 'Klapp Daddy',
}

response = requests.get('https://mlb.pointsderby.com/entryDetail.php', params=params)

r = response.text
soup = BeautifulSoup(r, 'html.parser')

rows = soup.find_all('tr')

player_names = []

for row in rows:
    td = row.find('td')
    if td:
        link = td.find('a')
        if link:
            name = link.get_text().strip()
            if name and not name.startswith("("):
                player_names.append(name)

unique_players = []

for item in player_names:
    if item not in unique_players:
        unique_players.append(item)

player_ids = []

for i in unique_players:
    player = statsapi.lookup_player(i)
    player_ids.append(player[0]['id'])

print(player_ids)

solo_date = "2023-04-26"
# solo_date_today = datetime.today().strftime('%Y-%m-%d')
base_url = "https://mlb.com"



async def main():
    browser = await launch()
    page = await browser.newPage()

    videos_by_player = {}

    for player_name, player_id in zip(unique_players, player_ids):
        try:
            solo_date_url = f"https://www.mlb.com/video/?q=Date+%3D+%5B%22{solo_date}%22%5D+AND+HitResult+%3D+%5B%22Home+Run%22%5D+AND+BatterId+%3D%3D+%5B{player_id}%5D+Order+By+Timestamp+DESC&of=1"

            await page.goto(solo_date_url)

            # Add a waiting mechanism to ensure that the content is fully loaded
            await page.waitFor(3000)

            await page.waitForSelector(".gridstyle__GridWrapper-sc-1irow18-0.cCMZdo a", timeout=5000)

            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")

            a_tags = soup.select(".gridstyle__GridWrapper-sc-1irow18-0.cCMZdo a")
            titles = [tag.find("h3", class_="ContentCard__Title-sc-189fu57-7 hhLdbB").text for tag in a_tags]
            hrefs = [tag['href'] for tag in a_tags if 'href' in tag.attrs]
            full_urls = [base_url + href.split("?")[0] for href in hrefs]

            videos_by_player[player_id] = {"name": player_name, "urls": [{"title": title, "url": url} for title, url in zip(titles, full_urls)]}

            print(player_id)
            print(full_urls)

        except Exception as e:
            print(f"Player ID {player_id}: NO HRs")
            videos_by_player[player_id] = {"name": player_name, "urls": []}

    await browser.close()
    data = []
    for player_id, player_info in videos_by_player.items():
        for video_info in player_info["urls"]:
            data.append({"player_id": player_id, "player_name": player_info["name"], "video_title": video_info["title"], "video_url": video_info["url"]})

    data = [{"player_id": player_id, "player_name": player_info["name"], "video_title": video_info["title"], "video_url": video_info["url"]} for player_id, player_info in videos_by_player.items() for video_info in player_info["urls"]]
    df = pd.DataFrame(data)
    df = df[['player_name', 'player_id', 'video_title', 'video_url']]
    print(df)

df = asyncio.get_event_loop().run_until_complete(main())