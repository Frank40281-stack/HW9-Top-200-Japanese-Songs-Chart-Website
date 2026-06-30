import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def parse():
    with open("song_detail.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    
    # Check for ruby tags
    ruby_tags = soup.find_all("ruby")
    print(f"Found {len(ruby_tags)} ruby tags.")
    
    # Check for sections that look like lyrics lines
    # Usually lyrics are inside a container. Let's find tags containing ruby and print their parents.
    if ruby_tags:
        parent = ruby_tags[0].parent
        print("First ruby parent tag:", parent.name)
        print("First ruby parent classes:", parent.get("class"))
        print("First ruby parent text:", parent.get_text(strip=True))
        
        # Let's search for parents that might contain lines
        # Let's print the outer structure of the first lyrics line
        grandparent = parent.parent
        print("\nGrandparent tag:", grandparent.name)
        print("Grandparent classes:", grandparent.get("class"))
        
        # Let's inspect sibling tags or search for Chinese translation
        # Let's find some Chinese characters or tags near the parent
        siblings = list(parent.next_siblings)
        print(f"\nParent has {len(siblings)} siblings.")
        for i, sib in enumerate(siblings[:10]):
            if sib.name:
                print(f"Sibling {i} tag: {sib.name}, classes: {sib.get('class')}, text: {sib.get_text(strip=True)}")
                
    # Search for other structures
    # Let's search for class names containing 'lyric'
    for tag in soup.find_all(class_=True):
        classes = tag.get("class", [])
        if any("lyric" in c.lower() for c in classes):
            print(f"\nFound tag with lyric class: <{tag.name} class='{classes}'>")
            print("Text preview:", tag.get_text(strip=True)[:100])
            break

if __name__ == "__main__":
    parse()
