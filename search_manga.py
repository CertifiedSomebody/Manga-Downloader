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
        "includes[]": ["cover_art"],  # ✅ Correct field for additional data
        "availableTranslatedLanguage[]": [language]  # ✅ Searches only for translated titles
    }

    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        print(f"❌ Failed to fetch manga list: {response.status_code}")
        return {}, language

    manga_data = response.json()
    manga_list = manga_data.get("data", [])

    if not manga_list:
        print("❌ No manga found with that title.")
        return {}, language

    # ✅ Extracting correct titles safely and mapping manga titles to their IDs
    formatted_results = {}
    for manga in manga_list:
        attributes = manga.get("attributes", {})
        titles = attributes.get("title", {})

        # ✅ Improved title extraction logic: prioritize different languages
        manga_title = titles.get("en") or titles.get("ja-ro") or titles.get("jp") or titles.get("kr") 
        if not manga_title and titles:
            manga_title = list(titles.values())[0]  # Fallback to first available title
        manga_title = manga_title or "Unknown Title"

        manga_id = manga.get("id", "")

        formatted_results[manga_title] = manga_id

    # ✅ Return results sorted alphabetically by title
    sorted_results = dict(sorted(formatted_results.items()))

    return sorted_results, language

# ✅ Test the function if run directly
if __name__ == "__main__":
    title = input("Enter manga title: ").strip()
    manga_dict, language = search_manga(title)
    if manga_dict:
        print("\n🔍 Search Results:")
        for index, (manga_title, manga_id) in enumerate(manga_dict.items(), start=1):
            print(f"[{index}] {manga_title} (ID: {manga_id})")
