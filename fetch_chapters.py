import requests

BASE_URL = "https://api.mangadex.org"

# ✅ Function to fetch all chapters in the selected language
def fetch_chapters(manga_id, language):
    url = f"{BASE_URL}/manga/{manga_id}/feed"
    params = {"translatedLanguage[]": language, "order[chapter]": "asc", "limit": 500}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ Failed to fetch chapters: {response.status_code}")
        return []

    chapters = response.json().get("data", [])

    # ✅ Return (chapter_id, formatted title, chapter number)
    return [
        (
            chapter["id"],
            f"Chapter {chapter['attributes'].get('chapter', 'N/A')}",
            chapter["attributes"].get("chapter", "N/A"),
        )
        for chapter in chapters
    ]


if __name__ == "__main__":
    manga_id = input("Enter Manga ID: ")
    language = input("Enter language code: ") or "en"
    chapters = fetch_chapters(manga_id, language)
    
    if chapters:
        for index, (chapter_id, chapter_title, chapter_num) in enumerate(chapters, start=1):
            print(f"[{index}] {chapter_title} (ID: {chapter_id}, Number: {chapter_num})")
