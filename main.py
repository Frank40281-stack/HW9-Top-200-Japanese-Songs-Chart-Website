import os
import csv
import sys
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, Query, Header
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure stdout handles unicode in Windows
sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI(
    title="MaruMaru-X Top 200 Japanese Songs API",
    description="FastAPI backend serving the Top 200 most-liked Japanese songs from marumaru-x.com",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE = "top200_songs.csv"

# Global scraper status tracker
scraper_status = {
    "status": "idle",       # idle, running, completed, failed
    "last_run": None,
    "error": None
}

def parse_numeric_value(val_str):
    """Convert metric suffix representation (e.g. 9.5K) to integer."""
    if not val_str:
        return 0
    val_str = str(val_str).strip().upper()
    if not val_str or val_str == '0':
        return 0
    try:
        if 'K' in val_str:
            return int(float(val_str.replace('K', '')) * 1000)
        if 'M' in val_str:
            return int(float(val_str.replace('M', '')) * 1000000)
        return int(float(val_str))
    except Exception:
        return 0

def load_songs_from_csv():
    """Load song data from top200_songs.csv."""
    songs = []
    if not os.path.exists(CSV_FILE):
        return songs
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("排名"):
                    row["排名"] = int(row["排名"])
                songs.append(row)
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return songs

# Background scraping runner
def run_scraper_task():
    global scraper_status
    scraper_status["status"] = "running"
    scraper_status["error"] = None
    try:
        from scraper import scrape_songs, save_to_csv, generate_readme, generate_html
        from scrape_lyrics import scrape_all_lyrics
        print("Starting background scraper task...")
        songs = scrape_songs()
        if songs:
            save_to_csv(songs)
            generate_readme(songs)
            generate_html(songs)
            print("Starting background lyrics scraper task...")
            scrape_all_lyrics(force=False, max_workers=6)
            scraper_status["status"] = "completed"
        else:
            scraper_status["status"] = "failed"
            scraper_status["error"] = "Scraper returned empty song list."
    except Exception as e:
        print(f"Scraper task failed: {e}")
        scraper_status["status"] = "failed"
        scraper_status["error"] = str(e)
    finally:
        scraper_status["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Endpoints
@app.get("/")
def read_index():
    """Serve the single-page application dashboard."""
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return JSONResponse(
        status_code=404, 
        content={"error": "index.html not found. Run scraper first or create index.html"}
    )

@app.get("/sakura_forest.png")
def read_sakura_forest():
    """Serve the background image."""
    if os.path.exists("sakura_forest.png"):
        return FileResponse("sakura_forest.png")
    return JSONResponse(status_code=404, content={"error": "Background image not found"})

@app.get("/api/songs")
def get_songs(
    search: str = Query(None, description="Search term matching Title, Artist, or Tags"),
    sort_by: str = Query("rank", description="Sorting field: rank, likes, plays, date, duration"),
    tag: str = Query(None, description="Filter by exact tag")
):
    """Retrieve the song list with server-side filtering and sorting."""
    songs = load_songs_from_csv()
    
    # Filter by exact tag
    if tag:
        tag_lower = tag.lower().strip()
        songs = [
            s for s in songs 
            if s.get("標籤") and tag_lower in [t.strip().lower() for t in s["標籤"].split(",")]
        ]
        
    # Search filter (matches title, singer, or tags)
    if search:
        search_lower = search.lower().strip()
        songs = [
            s for s in songs
            if search_lower in s.get("歌名", "").lower() 
            or search_lower in s.get("歌手", "").lower()
            or (s.get("標籤") and search_lower in s["標籤"].lower())
        ]
        
    # Sort
    if sort_by == "rank":
        songs.sort(key=lambda x: x.get("排名", 999))
    elif sort_by == "likes-desc":
        songs.sort(key=lambda x: parse_numeric_value(x.get("愛心數量")), reverse=True)
    elif sort_by == "plays-desc":
        songs.sort(key=lambda x: parse_numeric_value(x.get("播放次數")), reverse=True)
    elif sort_by == "date-desc":
        # Handle empty/missing dates
        songs.sort(key=lambda x: x.get("發佈日期") or "1970-01-01", reverse=True)
    elif sort_by == "duration-desc":
        def get_seconds(duration_str):
            if not duration_str:
                return 0
            parts = duration_str.split(":")
            if len(parts) == 2:
                try:
                    return int(parts[0]) * 60 + int(parts[1])
                except ValueError:
                    return 0
            return 0
        songs.sort(key=lambda x: get_seconds(x.get("時長")), reverse=True)
        
    return songs

@app.get("/api/stats")
def get_stats():
    """Retrieve aggregated dataset statistics."""
    songs = load_songs_from_csv()
    if not songs:
        return {
            "total_songs": 0,
            "total_likes": 0,
            "total_plays": 0,
            "top_singer": "--",
            "tag_distribution": {}
        }
        
    total_likes = 0
    total_plays = 0
    singer_counts = {}
    tag_counts = {}
    
    for song in songs:
        total_likes += parse_numeric_value(song.get("愛心數量"))
        total_plays += parse_numeric_value(song.get("播放次數"))
        
        singer = song.get("歌手")
        if singer:
            singer_counts[singer] = singer_counts.get(singer, 0) + 1
            
        tags_str = song.get("標籤")
        if tags_str:
            for t in tags_str.split(","):
                t_clean = t.strip()
                if t_clean:
                    tag_counts[t_clean] = tag_counts.get(t_clean, 0) + 1
                    
    # Find top artist
    top_singer = "--"
    if singer_counts:
        top_singer_name = max(singer_counts, key=singer_counts.get)
        top_singer = f"{top_singer_name} ({singer_counts[top_singer_name]}首)"
        
    # Get top 10 tags
    top_tags = dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
    return {
        "total_songs": len(songs),
        "total_likes": total_likes,
        "total_plays": total_plays,
        "top_singer": top_singer,
        "tag_distribution": top_tags
    }

@app.get("/api/lyrics/{rank}")
def get_lyrics(rank: int):
    """Retrieve lyrics for a specific song by its rank."""
    import json
    path = os.path.join("lyrics", f"{rank}.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to read lyrics file: {e}"}
            )
    return JSONResponse(
        status_code=404,
        content={"error": f"Lyrics for rank {rank} not found."}
    )

@app.post("/api/scrape")
def trigger_scrape(background_tasks: BackgroundTasks):
    """Trigger background scraper task."""
    global scraper_status
    if scraper_status["status"] == "running":
        return JSONResponse(
            status_code=400, 
            content={"status": "running", "message": "Scraper is already running."}
        )
    background_tasks.add_task(run_scraper_task)
    return {"status": "started", "message": "Background scrape started."}

@app.get("/api/scrape/status")
def get_scrape_status():
    """Retrieve current background scraping status."""
    global scraper_status
    return scraper_status

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.post("/api/chat")
def chat_with_llm(request: ChatRequest, x_gemini_api_key: str = Header(None)):
    """Interact with Gemini model using provided context and chat history."""
    api_key = x_gemini_api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return JSONResponse(
            status_code=400,
            content={"error": "缺少 API Key。請在聊天室設定中輸入您的 Gemini API Key，或在後端環境變數中設定 GEMINI_API_KEY。"}
        )

    # 1. Compile context
    songs = load_songs_from_csv()
    catalog_text = ""
    if songs:
        catalog_text = "以下是本站的最受歡迎日文歌排行前 150 名的資料資料 (包含 排名, 歌名, 歌手, 愛心數量, 播放次數, 時長, 發佈日期, 標籤):\n"
        for s in songs[:150]:
            catalog_text += f"#{s.get('排名')}: {s.get('歌名')} - {s.get('歌手')} (愛心: {s.get('愛心數量')}, 播放: {s.get('播放次數')}, 時長: {s.get('時長')}, 日期: {s.get('發佈日期')}, 標籤: {s.get('標籤')})\n"

    # 2. System Prompt
    system_instruction = (
        "你是 'MaruMaru-X 日語熱門歌曲排行榜 (Top 200)' 網站的 AI 助手。\n"
        "你擁有網站上熱門日文歌曲的完整數據庫（前150首）。請善加利用這些資訊回答使用者關於歌曲推薦、熱門歌手、播放量、發佈日期、時長、標籤篩選等問題。\n"
        "如果使用者問及排行榜外的歌，請委婉告知你只專注於 Top 200 排行榜，但能推薦排行榜內相似風格的歌。\n"
        "請一律使用『繁體中文』回答，語氣要親切、專業、客氣。回答內容請用 Markdown 格式進行條列與粗體標示，以便閱讀。\n"
        f"{catalog_text}\n"
    )

    # Compile prompt content
    contents = []
    
    # Restructure history
    for item in request.history:
        role = "user" if item.get("role") == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": item.get("text", "")}]
        })
        
    # Append new message
    user_message = request.message
    if not contents:
        # Prepend system instruction on first load
        prompt = f"{system_instruction}\n使用者問題: {user_message}"
    else:
        prompt = f"系統提示：請一律依據網站歌曲庫回答。使用者問題: {user_message}"
        
    contents.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    req_body = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.95,
            "maxOutputTokens": 1024
        }
    }

    try:
        import urllib.request
        import json
        req = urllib.request.Request(
            url,
            data=json.dumps(req_body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            
        candidates = res_data.get("candidates", [])
        if candidates:
            text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return {"response": text}
        else:
            return JSONResponse(status_code=500, content={"error": "API 回傳格式不正確。"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"呼叫 Gemini API 失敗：{e}"})
