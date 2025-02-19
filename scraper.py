import cloudscraper
from bs4 import BeautifulSoup

# Create a Cloudscraper session
scraper = cloudscraper.create_scraper()

def scrape_games():
    url = "https://apkcombo.com/en/category/games/"  # Corrected URL for APKCombo games
    response = scraper.get(url)

    if response.status_code != 200:
        print("Failed to retrieve data, Status Code:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    games = []
    for game in soup.select(".l_item .info .name"):  # Correct selector for game name
        title = game.text.strip()
        link = game.find_parent("a")["href"]  # Get link from the parent <a> tag
        games.append({"title": title, "link": link})

    return games

if __name__ == "__main__":
    game_list = scrape_games()
    
    if game_list:
        for game in game_list:
            print(f"Title: {game['title']}, Link: {game['link']}")
    else:
        print("No games found.")
