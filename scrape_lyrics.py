import os
import csv
import json
import urllib.request
import sys
import time
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ensure stdout handles unicode in Windows console
sys.stdout.reconfigure(encoding='utf-8')

CSV_FILE = "top200_songs.csv"
LYRICS_DIR = "lyrics"

def parse_lyrics_from_url(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        soup = BeautifulSoup(html, "html.parser")
        ul = soup.find("ul", class_="google-anno-skip")
        if not ul:
            return []
            
        lyrics = []
        items = ul.find_all("li", class_="mr-lyrics-list")
        for li in items:
            source_p = li.find("p", class_="lyrics-source")
            if not source_p:
                continue
            
            # Keep <ruby> structures
            source_html = "".join([str(c) for c in source_p.contents]).strip()
            
            zh_p = li.find("p", class_="lyrics-translate-zh")
            zh_text = zh_p.get_text(strip=True) if zh_p else ""
            
            en_p = li.find("p", class_="lyrics-translate-en")
            en_text = en_p.get_text(strip=True) if en_p else "" # Wait, let's fix typo: en_p not e_p!
            
            lyrics.append({
                "ja_html": source_html,
                "zh_text": zh_text,
                "en_text": en_text
            })
        return lyrics
    except Exception as e:
        print(f"Error fetching lyrics for {url}: {e}")
        return []

def scrape_single_song_lyrics(song, force=False):
    rank = song.get("排名")
    url = song.get("歌曲連結")
    title = song.get("歌名", "未知")
    
    if not url:
        print(f"[{rank}] 無歌曲連結，跳過。")
        return False
        
    out_path = os.path.join(LYRICS_DIR, f"{rank}.json")
    
    # Check if cached and valid
    if not force and os.path.exists(out_path):
        try:
            with open(out_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    # File exists and is valid, skip
                    return True
        except Exception:
            pass # Re-scrape if file is corrupt
            
    print(f"[{rank}] 正在爬取歌詞: {title}...")
    # Add a small random delay to avoid hitting the server too hard
    time.sleep(random.uniform(0.2, 0.8))
    
    lyrics = parse_lyrics_from_url(url)
    
    if lyrics:
        with open(out_path, "w", encoding="utf-8") as out:
            json.dump(lyrics, out, ensure_ascii=False, indent=2)
        print(f"[{rank}] 歌詞爬取成功，共 {len(lyrics)} 句。")
        return True
    else:
        print(f"[{rank}] 歌詞爬取失敗或為空: {title}")
        return False

def scrape_all_lyrics(force=False, max_workers=5):
    if not os.path.exists(CSV_FILE):
        print(f"找不到 CSV 檔案 {CSV_FILE}。請先執行 scraper.py。")
        return
        
    os.makedirs(LYRICS_DIR, exist_ok=True)
    
    songs = []
    with open(CSV_FILE, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(row)
            
    print(f"開始爬取共 {len(songs)} 首歌曲的歌詞...")
    
    success_count = 0
    skipped_count = 0
    failed_count = 0
    
    # Run concurrently using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks
        future_to_song = {}
        for song in songs:
            rank = song.get("排名")
            out_path = os.path.join(LYRICS_DIR, f"{rank}.json")
            if not force and os.path.exists(out_path):
                # Check cache fast before scheduling
                try:
                    with open(out_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list) and len(data) > 0:
                            skipped_count += 1
                            continue
                except Exception:
                    pass
            
            future = executor.submit(scrape_single_song_lyrics, song, force=force)
            future_to_song[future] = song
            
        # Process results as they complete
        for future in as_completed(future_to_song):
            song = future_to_song[future]
            rank = song.get("排名")
            title = song.get("歌名")
            try:
                success = future.result()
                if success:
                    success_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                print(f"[{rank}] 執行緒處理 {title} 時發生例外: {e}")
                failed_count += 1
                
    print(f"\n歌詞爬取作業完成。")
    print(f"總計: 已存在/跳過 {skipped_count} 首, 成功爬取 {success_count} 首, 失敗 {failed_count} 首。")

def main():
    scrape_all_lyrics(force=False, max_workers=6)

if __name__ == "__main__":
    main()
