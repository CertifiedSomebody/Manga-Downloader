import requests

BASE_URL = "https://api.mangadex.org"

# ✅ Function to search manga by title
def search_manga(title=None, language="en"):
    if not title:
        title = input("Enter manga title: ").strip()
    if not language:
        language = input("Enter language code (default 'en' for English): ").strip() or "en"

    search_url = f"{BASE_URL}/manga"
    params = {
        "title": title,
        "limit": 10,
        "contentRating[]": ["safe", "suggestive", "erotica"],
        "includes[]": ["title", "description"],
    }

    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        print(f"❌ Failed to fetch manga list: {response.status_code}")
        return [], language

    manga_data = response.json()
    manga_list = manga_data.get("data", [])

    if not manga_list:
        print("❌ No manga found with that title.")
        return [], language

    # ✅ Extracting correct titles
    formatted_results = []
    for manga in manga_list:
        attributes = manga.get("attributes", {})
        titles = attributes.get("title", {})
        
        # Get the English title or fallback to any available title
        manga_title = titles.get("en") or list(titles.values())[0] if titles else "Unknown Title"
        manga_id = manga.get("id", "")

        formatted_results.append((manga_id, manga_title))

    return formatted_results, language


if __name__ == "__main__":
    manga_list, language = search_manga()
    if manga_list:
        print("\n🔍 Search Results:")
        for index, (manga_id, manga_title) in enumerate(manga_list, start=1):
            print(f"[{index}] {manga_title} (ID: {manga_id})")
