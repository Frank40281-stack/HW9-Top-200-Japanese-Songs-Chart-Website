import urllib.request
from bs4 import BeautifulSoup

SONG_URL = "https://www.marumaru-x.com/japanese-song/play-1zn42zjre4"

def check():
    try:
        req = urllib.request.Request(
            SONG_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        print("Fetching page statically...")
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        
        soup = BeautifulSoup(html, "html.parser")
        ul = soup.find("ul", class_="google-anno-skip")
        if ul:
            print("SUCCESS! ul.google-anno-skip found in static HTML!")
            print(f"Number of lines: {len(ul.find_all('li', class_='mr-lyrics-list'))}")
        else:
            print("FAILURE: ul.google-anno-skip not found in static HTML. Playwright is required.")
    except Exception as e:
        print("Error during static fetch:", e)

if __name__ == "__main__":
    check()
