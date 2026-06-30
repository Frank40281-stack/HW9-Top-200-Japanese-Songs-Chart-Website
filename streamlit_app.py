import streamlit as st
import pandas as pd
import os
import json
import urllib.request

# Page Config
st.set_page_config(
    page_title="日語熱門歌曲排行榜 - Streamlit Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sakura ambient and styling
st.markdown(
    """
    <style>
    .reportview-container {
        background: #0d0e12;
    }
    .stat-card-st {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .lyric-box {
        text-align: center;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

CSV_FILE = "top200_songs.csv"

# Load song data
@st.cache_data
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        # Parse numeric columns
        def parse_numeric(val):
            if pd.isna(val):
                return 0
            val_str = str(val).strip().upper()
            try:
                if 'K' in val_str:
                    return float(val_str.replace('K', '')) * 1000
                if 'M' in val_str:
                    return float(val_str.replace('M', '')) * 1000000
                return float(val_str)
            except ValueError:
                return 0
        df["排名"] = df["排名"].astype(int)
        df["愛心(數值)"] = df["愛心數量"].apply(parse_numeric)
        df["播放(數值)"] = df["播放次數"].apply(parse_numeric)
        return df
    return None

df = load_data()

# Lyrics Dialog
@st.dialog("歌曲詳情與歌詞")
def show_lyrics_dialog(song):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(song["封面"] if pd.notna(song["封面"]) else "https://via.placeholder.com/320x180", use_container_width=True)
    with col2:
        st.write(f"### #{song['排名']} {song['歌名']}")
        st.write(f"**歌手**: {song['歌手']}")
        st.write(f"**發佈日期**: {song['發佈日期']} | **時長**: {song['時長']}")
        st.write(f"❤️ 愛心數: {song['愛心數量']} | 播放次數: {song['播放次數']}")
        if pd.notna(song.get("標籤")):
            st.write(f"**標籤**: {song['標籤']}")
        st.markdown(f"[前往 MaruMaru 原網頁]({song['歌曲連結']})")
        
    st.divider()
    st.markdown("#### 歌詞 Lyrics")
    
    # Load lyrics file
    rank = song["排名"]
    lyrics_path = os.path.join("lyrics", f"{rank}.json")
    if os.path.exists(lyrics_path):
        try:
            with open(lyrics_path, "r", encoding="utf-8") as f:
                lyrics = json.load(f)
            
            if lyrics:
                for line in lyrics:
                    ja_html = line.get("ja_html", "")
                    zh_text = line.get("zh_text", "")
                    
                    st.markdown(
                        f"""
                        <div style="text-align: center; margin-bottom: 15px;">
                            <div style="font-size: 1.2rem; line-height: 2.2; color: #ffffff; font-family: sans-serif;">{ja_html}</div>
                            <div style="font-size: 0.95rem; color: #ffb7d5; margin-top: 4px;">{zh_text}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("此歌曲暫無歌詞內容。")
        except Exception as e:
            st.error(f"載入歌詞發生錯誤: {e}")
    else:
        st.warning("找不到此歌曲的歌詞檔案，請確認已在本地執行過歌詞爬取程式。")

# LLM Chat helper
def get_llm_response(message, history, api_key):
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        return "❌ 缺少 API Key。請在側邊欄輸入您的 Gemini API Key 或設定 GEMINI_API_KEY 環境變數。"
        
    # Compile database context
    catalog_text = ""
    if df is not None:
        catalog_text = "以下是本站的最受歡迎日文歌排行前 150 名的資料資料 (包含 排名, 歌名, 歌手, 愛心數量, 播放次數, 時長, 發佈日期, 標籤):\n"
        for idx, row in df.head(150).iterrows():
            catalog_text += f"#{row['排名']}: {row['歌名']} - {row['歌手']} (愛心: {row['愛心數量']}, 播放: {row['播放次數']}, 時長: {row['時長']}, 日期: {row['發佈日期']}, 標籤: {row['標籤']})\n"
    else:
        catalog_text = "（無法載入歌曲資料庫，請以您的歌曲知識回答。）"

    system_instruction = (
        "你是 'MaruMaru-X 日語熱門歌曲排行榜 (Top 200)' 網站的 AI 助手。\n"
        "你擁有網站上熱門日文歌曲的完整數據庫（前150首）。請善加利用這些資訊回答使用者關於歌曲推薦、熱門歌手、播放量、發佈日期、時長、標籤篩選等問題。\n"
        "如果使用者問及排行榜外的歌，請委婉告知你只專注於 Top 200 排行榜，但能推薦排行榜內相似風格的歌。\n"
        "請一律使用『繁體中文』回答，語氣要親切、專業、客氣。回答內容請用 Markdown 格式進行條列與粗體標示，以便閱讀。\n"
        f"{system_instruction}\n"
    )

    contents = []
    for item in history:
        role = "user" if item["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": item["content"]}]
        })
        
    if not contents:
        prompt = f"{system_instruction}\n使用者問題: {message}"
    else:
        prompt = f"系統提示：請一律依據網站歌曲庫回答。使用者問題: {message}"
        
    contents.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    req_body = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.95,
            "maxOutputTokens": 1024
        }
    }

    try:
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
            return text
        else:
            return "❌ 錯誤：API 回傳格式不正確。"
    except Exception as e:
        return f"❌ 呼叫 Gemini API 失敗：{e}"


# Sidebar Layout (AI Chatbot)
with st.sidebar:
    st.header("🎵 MaruMaru-X AI 助理")
    
    st.subheader("API 設定")
    gemini_key = st.text_input("Gemini API Key", type="password", help="請輸入您的 Gemini API Key。如果不輸入，系統將使用後端環境變數。")
    
    st.divider()
    st.subheader("💬 對話聊天室")
    
    # Manage session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "哈囉！我是您的 AI 歌曲小幫手。我可以為您推薦 Top 200 的日文歌曲、分析歌手或提供歌曲類型建議。\n\n請在上方設定您的 **Gemini API Key** 即可開始與我對談喔！"}
        ]
        
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Chat prompt suggestions
    st.caption("您可以快速點選以下問題：")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("推薦米津玄師", key="sugg_1"):
            st.session_state.temp_input = "推薦 3 首米津玄師的歌曲"
    with col2:
        if st.button("推薦動漫歌曲", key="sugg_2"):
            st.session_state.temp_input = "有哪些標籤是 #ANM (動漫) 的熱門歌？"
            
    # Input box
    user_input = st.chat_input("問問我關於排行榜的歌...")
    
    # Handle suggestion click
    if "temp_input" in st.session_state and st.session_state.temp_input:
        user_input = st.session_state.temp_input
        st.session_state.temp_input = None
        
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("*正在思考中...*")
            
            response = get_llm_response(user_input, st.session_state.messages[:-1], gemini_key)
            
            message_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


# Main Dashboard Area
if df is None:
    st.title("日語熱門歌曲排行榜 - Top 200")
    st.error(f"找不到歌曲資料庫 {CSV_FILE}。請先在本地執行 scraper.py 爬取資料！")
else:
    st.title("日語熱門歌曲排行榜 🎵")
    st.write("MaruMaru-X Most Liked Japanese Songs Top 200 - Streamlit 互動儀表板")
    
    # Stats Cards (Widget Removal Applied)
    total_likes = int(df["愛心(數值)"].sum())
    total_plays = int(df["播放(數值)"].sum())
    
    def format_val(val, is_plays=False):
        if is_plays:
            return f"{val/1000000:.1f}M" if val >= 1000000 else (f"{val/1000:.1f}K" if val >= 1000 else str(val))
        return f"{val/1000:.1f}K" if val >= 1000 else str(val)
        
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown(
            f"""
            <div class="stat-card-st">
                <div style="font-size: 1.8rem; font-weight: 700; color: #7c4dff;">200</div>
                <div style="font-size: 0.85rem; color: #a9abb6;">歌曲總數</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with sc2:
        st.markdown(
            f"""
            <div class="stat-card-st">
                <div style="font-size: 1.8rem; font-weight: 700; color: #ff4081;">{format_val(total_likes)}</div>
                <div style="font-size: 0.85rem; color: #a9abb6;">點讚總數</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with sc3:
        st.markdown(
            f"""
            <div class="stat-card-st">
                <div style="font-size: 1.8rem; font-weight: 700; color: #00e5ff;">{format_val(total_plays, True)}</div>
                <div style="font-size: 0.85rem; color: #a9abb6;">觀看次數</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.divider()
    
    # Controls Panel
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])
    with ctrl_col1:
        search_query = st.text_input("搜尋歌名、歌手或標籤...", "").strip().lower()
    with ctrl_col2:
        sort_by = st.selectbox(
            "排序方式",
            options=["按排名 (1-200)", "按愛心數量 (多到少)", "按播放次數 (多到少)", "按發佈時間 (新到舊)", "按歌曲時長 (長到短)"]
        )
    with ctrl_col3:
        # Collect all tags
        all_tags = set()
        for tags in df["標籤"].dropna():
            for t in tags.split(","):
                all_tags.add(t.strip())
        sorted_tags = ["所有標籤"] + sorted(list(all_tags))
        selected_tag = st.selectbox("標籤篩選", options=sorted_tags)
        
    # Apply Filtering
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df["歌名"].str.lower().str.contains(search_query) |
            filtered_df["歌手"].str.lower().str.contains(search_query) |
            filtered_df["標籤"].fillna("").str.lower().str.contains(search_query)
        ]
        
    if selected_tag != "所有標籤":
        filtered_df = filtered_df[
            filtered_df["標籤"].fillna("").apply(lambda x: selected_tag in [t.strip() for t in x.split(",")])
        ]
        
    # Apply Sorting
    if sort_by == "按排名 (1-200)":
        filtered_df = filtered_df.sort_values("排名")
    elif sort_by == "按愛心數量 (多到少)":
        filtered_df = filtered_df.sort_values("愛心(數值)", ascending=False)
    elif sort_by == "按播放次數 (多到少)":
        filtered_df = filtered_df.sort_values("播放(數值)", ascending=False)
    elif sort_by == "按發佈時間 (新到舊)":
        filtered_df = filtered_df.sort_values("發佈日期", ascending=False)
    elif sort_by == "按歌曲時長 (長到短)":
        def get_seconds(d_str):
            if pd.isna(d_str):
                return 0
            pts = str(d_str).split(":")
            return int(pts[0]) * 60 + int(pts[1]) if len(pts) == 2 else 0
        filtered_df["seconds"] = filtered_df["時長"].apply(get_seconds)
        filtered_df = filtered_df.sort_values("seconds", ascending=False)
        
    # Display Options
    layout_mode = st.radio("檢視模式", ["網格卡片", "資料列表"], horizontal=True)
    
    if filtered_df.empty:
        st.warning("沒有找到符合條件的歌曲。")
    else:
        if layout_mode == "網格卡片":
            # Display songs in grid cards
            # We will render in 2 columns
            grid_cols = st.columns(2)
            for idx, (_, song) in enumerate(filtered_df.iterrows()):
                target_col = grid_cols[idx % 2]
                with target_col:
                    with st.container(border=True):
                        c1, c2 = st.columns([1, 2])
                        with c1:
                            st.image(song["封面"] if pd.notna(song["封面"]) else "https://via.placeholder.com/320x180", use_container_width=True)
                        with c2:
                            st.markdown(f"##### #{song['排名']} **{song['歌名']}**")
                            st.markdown(f"**歌手**: {song['歌手']}")
                            st.markdown(f"時長: {song['時長']} | 日期: {song['發佈日期']}")
                            st.markdown(f"❤️ {song['愛心數量']} | 播放: {song['播放次數']}")
                            if pd.notna(song["標籤"]):
                                st.caption(f"標籤: {song['標籤']}")
                            
                            # Dialog Button
                            if st.button("查看歌詞 & 詳情", key=f"btn_grid_{song['排名']}"):
                                show_lyrics_dialog(song)
        else:
            # Display songs in Table List
            # Streamlit dataframe or manual HTML table
            display_df = filtered_df[["排名", "歌名", "歌手", "愛心數量", "播放次數", "時長", "發佈日期", "標籤"]].copy()
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            st.write("請使用下表快速選擇並查看歌詞：")
            # Selectbox list to choose lyric
            selected_song_title = st.selectbox(
                "選擇歌曲查看歌詞...",
                options=filtered_df.apply(lambda r: f"#{r['排名']} - {r['歌名']} ({r['歌手']})", axis=1)
            )
            if selected_song_title:
                rank_str = selected_song_title.split(" - ")[0].replace("#", "")
                song_row = filtered_df[filtered_df["排名"] == int(rank_str)].iloc[0]
                if st.button("彈出歌詞視窗", key="btn_table_lyric"):
                    show_lyrics_dialog(song_row)
