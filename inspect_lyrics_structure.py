import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def parse():
    with open("song_detail.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find("ul", class_="google-anno-skip")
    
    if ul:
        print("Found ul.google-anno-skip!")
        items = ul.find_all("li", recursive=False)
        print(f"Number of direct li items: {len(items)}")
        if items:
            for i, li in enumerate(items[:3]):
                print(f"\n--- Item {i+1} HTML ---")
                print(li.prettify())
    else:
        print("Could not find ul.google-anno-skip")

if __name__ == "__main__":
    parse()
