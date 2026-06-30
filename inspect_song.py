import sys
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

SONG_URL = "https://www.marumaru-x.com/japanese-song/play-1zn42zjre4"

def inspect():
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Going to {SONG_URL}...")
        page.goto(SONG_URL, wait_until="domcontentloaded")
        
        # Wait a little bit for dynamic content if any
        page.wait_for_timeout(3000)
        
        html_content = page.content()
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Let's search for lyrics container
        # Let's save a portion of the HTML to inspect
        with open("song_detail.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
            
        print("HTML saved to song_detail.html")
        browser.close()

if __name__ == "__main__":
    inspect()
