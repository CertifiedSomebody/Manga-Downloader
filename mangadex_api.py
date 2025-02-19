import requests

# Authentication token
auth_token = 'jWBg2kxqaLgGsrHQyGYX8cTBYIg2zBDA'

# MangaDex API base URL
base_url = 'https://api.mangadex.org'

# Headers with authentication
headers = {
    'Authorization': f'Bearer {auth_token}'
}

# Function to get manga ID from a chapter
def get_manga_id(chapter_id):
    url = f'{base_url}/chapter/{chapter_id}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        for relation in data['data']['relationships']:
            if relation['type'] == 'manga':
                return relation['id']  # Return the manga ID
    else:
        print(f'Error {response.status_code}: {response.text}')
        return None

# Function to get the latest English chapter ID of a manga
def get_latest_chapter_id(manga_id, language='en'):
    url = f'{base_url}/manga/{manga_id}/feed?translatedLanguage[]={language}&order[chapter]=desc&limit=1'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            return data['data'][0]['id']  # Return the latest chapter ID
    else:
        print(f'Error {response.status_code}: {response.text}')
    
    return None

# Function to get all chapter details
def get_chapter_info(chapter_id):
    url = f'{base_url}/at-home/server/{chapter_id}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return chapter details
    else:
        print(f'Error {response.status_code}: {response.text}')
        return None

# Example Usage:
if __name__ == "__main__":
    sample_chapter_id = 'ec660b6b-765f-4f31-b2c1-42596ef60b62'

    manga_id = get_manga_id(sample_chapter_id)
    if manga_id:
        latest_chapter = get_latest_chapter_id(manga_id)
        print(f'Latest English Chapter ID: {latest_chapter}')
