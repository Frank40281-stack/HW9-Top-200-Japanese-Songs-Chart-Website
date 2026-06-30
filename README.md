# MaruMaru-X Most Liked Japanese Songs (Top 200)

此專案收集了 [MaruMaru 日語音樂網](https://www.marumaru-x.com/japanese-song/most-liked) 上最受歡迎的 200 首日文歌曲資訊，包含 YouTube 封面圖、播放量、愛心數、時長、發佈日期及標籤等資訊。並自動生成了此 README 文件與一個精美的互動式網頁 [index.html](index.html)。

## 專案功能
- **多功能爬蟲**：使用 Playwright 與 BeautifulSoup 動態抓取 MaruMaru-X 排行榜資料，避開自動化檢測。
- **數據導出**：自動輸出完整的 [top200_songs.csv](top200_songs.csv) 檔案，包含完整的中日文字型支援與 BOM 設定，便於後續分析與使用。
- **互動式網頁**：自動生成 [index.html](index.html) 網頁，支援即時搜尋、標籤篩選、多欄位排序（愛心數、播放次數、發佈時間、時長），並包含網格卡片與列表視圖的切換。**並內建櫻花飄落背景動效！**

## 快速開始

### 1. 安裝環境需求
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 2. 本地預覽網頁
本專案為純靜態前端應用，您無須啟動任何後端 Python 伺服器，直接在瀏覽器按兩下開啟專案根目錄的 **`index.html`** 即可瀏覽！

### 3. GitHub Pages 線上展示（推薦）
本專案已成功部署至 GitHub Pages，您可以直接點擊連結瀏覽線上展示版：
👉 **[MaruMaru-X Top 200 線上儀表板](https://frank40281-stack.github.io/HW9-Top-200-Japanese-Songs-Chart-Website/)**

*(在線上展示版中，您可以使用側邊欄的 AI 助理，輸入您的 Gemini API Key 來直接查詢、分析 Top 200 歌曲庫，且點擊歌曲即可流暢載入 Furigana 注音歌詞！)*

### 4. 執行爬蟲程式更新資料
如果您想在本地重新抓取排行榜或更新歌詞資料：
```bash
# 爬取排行榜歌曲資料 (輸出為 top200_songs.csv 及 index.html)
python scraper.py

# 爬取全數歌曲的日文平假名/中文翻譯歌詞 (儲存於 lyrics/ 資料夾下)
python scrape_lyrics.py
```

## 排行榜數據表 (Top 200)

| 排名 | 封面 | 歌名 | 歌手 | 愛心數量 | 播放次數 | 時長 | 發佈日期 | 標籤 |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| 1 | <img src="https://i.ytimg.com/vi/SX_ViT4Ra7k/sddefault.jpg" width="80" alt="封面"> | [Lemon](https://www.marumaru-x.com/japanese-song/play-1zn42zjre4) | 米津玄師 | 9.5K | 496.3K | 4:35 | 2018-03-14 | #JPOP, #米津玄師 |
| 2 | <img src="https://i.ytimg.com/vi/-tKVN2mAKRI/sddefault.jpg" width="80" alt="封面"> | [打上花火](https://www.marumaru-x.com/japanese-song/play-ywn12djr7l) | DAOKO×米津玄師 | 7.4K | 336.2K | 4:53 | 2017-08-16 | #ANM, #DAOKO, #米津玄師 |
| 3 | <img src="https://i.ytimg.com/vi/by4SYYWlhEs/sddefault.jpg" width="80" alt="封面"> | [夜に駆ける](https://www.marumaru-x.com/japanese-song/play-14o711xqok) | YOASOBI | 6.4K | 375.4K | 4:22 | 2019-12-15 | #JPOP, #YOASOBI |
| 4 | <img src="https://i.ytimg.com/vi/x1FV6IrjZCY/sddefault.jpg" width="80" alt="封面"> | [紅蓮華](https://www.marumaru-x.com/japanese-song/play-lvnw1830o7) | LiSA | 5.4K | 248K | 3:56 | 2019-07-03 | #ANM, #LiSA |
| 5 | <img src="https://i.ytimg.com/vi/jhOVibLEDhA/sddefault.jpg" width="80" alt="封面"> | [恋](https://www.marumaru-x.com/japanese-song/play-14o797drkq) | 星野源 | 4.9K | 228.7K | 4:53 | 2016-10-05 | #JPOP, #星野源 |
| 6 | <img src="https://i.ytimg.com/vi/GcpsTmDO9k0/sddefault.jpg" width="80" alt="封面"> | [First Love](https://www.marumaru-x.com/japanese-song/play-14o71dqokq) | 宇多田ヒカル | 4.8K | 226K | 4:16 | 1999-03-10 | #JPOP, #宇多田ヒカル |
| 7 | <img src="https://i.ytimg.com/vi/4DxL6IKmXx4/sddefault.jpg" width="80" alt="封面"> | [炎](https://www.marumaru-x.com/japanese-song/play-pynpv4k9nd) | LiSA | 4.4K | 210K | 5:02 | 2020-10-14 | #ANM, #LiSA |
| 8 | <img src="https://i.ytimg.com/vi/1Bk9YpwWEsg/sddefault.jpg" width="80" alt="封面"> | [世界が終るまでは…](https://www.marumaru-x.com/japanese-song/play-evr8qzxrm5) | WANDS | 4.4K | 233.4K | 5:18 | 1994-06-28 | #ANM, #WANDS |
| 9 | <img src="https://i.ytimg.com/vi/Y4nEEZwckuU/sddefault.jpg" width="80" alt="封面"> | [群青](https://www.marumaru-x.com/japanese-song/play-e4oy56lmn3) | YOASOBI | 4.3K | 192.6K | 4:23 | 2020-09-01 | #JPOP, #YOASOBI |
| 10 | <img src="https://i.ytimg.com/vi/o6wtDPVkKqI/sddefault.jpg" width="80" alt="封面"> | [残酷な天使のテーゼ](https://www.marumaru-x.com/japanese-song/play-60rm93y4np) | 高橋洋子 | 4K | 102.7K | 4:04 | 1995-10-25 | #ANM, #高橋洋子 |
| 11 | <img src="https://i.ytimg.com/vi/gJX2iy6nhHc/sddefault.jpg" width="80" alt="封面"> | [灰色と青 ( + 菅田将暉)](https://www.marumaru-x.com/japanese-song/play-72r9187oz3) | 米津玄師 | 4K | 179.1K | 5:43 | 2017-11-01 | #JPOP, #米津玄師, #菅田将暉 |
| 12 | <img src="https://i.ytimg.com/vi/kzZ6KXDM1RI/sddefault.jpg" width="80" alt="封面"> | [ドライフラワー](https://www.marumaru-x.com/japanese-song/play-dvol954do2) | 優里 | 4K | 193.1K | 4:48 | 2020-10-25 | #JPOP, #優里 |
| 13 | <img src="https://i.ytimg.com/vi/PDSkFeMVNFs/sddefault.jpg" width="80" alt="封面"> | [前前前世 (movie ver.)](https://www.marumaru-x.com/japanese-song/play-72r9qy9nz3) | RADWIMPS | 3.9K | 132.9K | 4:53 | 2016-08-24 | #ANM, #RADWIMPS |
| 14 | <img src="https://i.ytimg.com/vi/dy90tA3TT1c/sddefault.jpg" width="80" alt="封面"> | [怪物](https://www.marumaru-x.com/japanese-song/play-lvnw136qo7) | YOASOBI | 3.9K | 182.4K | 3:29 | 2021-01-06 | #ANM, #YOASOBI |
| 15 | <img src="https://i.ytimg.com/vi/B0GpxW8K0vY/sddefault.jpg" width="80" alt="封面"> | [secret base～君がくれたもの～ (10 years after Ver.)](https://www.marumaru-x.com/japanese-song/play-vxn5vywo9e) | 本間芽衣子(茅野愛衣)、安城鳴子(戸松遥)、鶴見知利子(早見沙織) | 3.8K | 79.4K | 5:53 | 2011-04-27 | #ANM, #茅野愛衣, #戸松遥, #早見沙織 |
| 16 | <img src="https://i.ytimg.com/vi/ZRtdQ81jPUQ/sddefault.jpg" width="80" alt="封面"> | [アイドル](https://www.marumaru-x.com/japanese-song/play-14o71qkqok) | YOASOBI | 3.7K | 200.1K | 3:46 | 2023-04-12 | #ANM, #YOASOBI |
| 17 | <img src="https://i.ytimg.com/vi/n89SKAymNfA/sddefault.jpg" width="80" alt="封面"> | [なんでもないや (movie ver.)](https://www.marumaru-x.com/japanese-song/play-evr845ppnm) | RADWIMPS | 3.7K | 120.6K | 5:45 | 2016-08-24 | #ANM, #RADWIMPS |
| 18 | <img src="https://i.ytimg.com/vi/JzurtO4yHrM/sddefault.jpg" width="80" alt="封面"> | [君が好きだと叫びたい](https://www.marumaru-x.com/japanese-song/play-1poxykxnyw) | BAAD | 3.7K | 140.8K | 3:48 | 1994-03-12 | #ANM, #BAAD |
| 19 | <img src="https://i.ytimg.com/vi/TQ8WlA2GXbk/sddefault.jpg" width="80" alt="封面"> | [Pretender](https://www.marumaru-x.com/japanese-song/play-q9oqljlmn4) | Official髭男dism | 3.3K | 132.5K | 5:36 | 2019-05-15 | #JPOP, #Official髭男dism |
| 20 | <img src="https://i.ytimg.com/vi/vjj16qog4vQ/sddefault.jpg" width="80" alt="封面"> | [明日晴れるかな](https://www.marumaru-x.com/japanese-song/play-wdr66mgr35) | 桑田佳祐 | 3.3K | 152.1K | 5:16 | 2007-05-16 | #JPOP, #サザンオールスターズ, #桑田佳祐 |
| 21 | <img src="https://i.ytimg.com/vi/mF5Qq2YheTg/sddefault.jpg" width="80" alt="封面"> | [雪の華](https://www.marumaru-x.com/japanese-song/play-v7n3kvkokw) | 中島美嘉 | 3.2K | 99.4K | 5:50 | 2004-06-21 | #JPOP, #中島美嘉 |
| 22 | <img src="https://i.ytimg.com/vi/6xZWW8ZQvVs/sddefault.jpg" width="80" alt="封面"> | [僕が死のうと思ったのは](https://www.marumaru-x.com/japanese-song/play-xqrd746rd4) | 中島美嘉 | 3.2K | 98.2K | 6:22 | 2013-08-28 | #JPOP, #中島美嘉 |
| 23 | <img src="https://i.ytimg.com/vi/kxs9Su_mbpU/sddefault.jpg" width="80" alt="封面"> | [カタオモイ](https://www.marumaru-x.com/japanese-song/play-1zn4wzjre4) | Aimer | 3.2K | 122.4K | 3:42 | 2016-09-21 | #JPOP, #Aimer |
| 24 | <img src="https://i.ytimg.com/vi/BEULybZnLO8/sddefault.jpg" width="80" alt="封面"> | [極楽浄土](https://www.marumaru-x.com/japanese-song/play-evr859lrm5) | GARNiDELiA | 3K | 95.1K | 3:46 | 2016-08-17 | #JPOP, #GARNiDELiA |
| 25 | <img src="https://i.ytimg.com/vi/_zqbQiCyFFo/sddefault.jpg" width="80" alt="封面"> | [Butter-fly](https://www.marumaru-x.com/japanese-song/play-g9r05k42nv) | 和田光司 | 3K | 72.6K | 4:19 | 1999-09-22 | #ANM, #和田光司 |
| 26 | <img src="https://i.ytimg.com/vi/7zBeQezaz4U/sddefault.jpg" width="80" alt="封面"> | [クリスマスソング](https://www.marumaru-x.com/japanese-song/play-lvnw6mqr7x) | back number | 2.9K | 133.2K | 5:43 | 2015-11-18 | #JPOP, #back number |
| 27 | <img src="https://i.ytimg.com/vi/DwTinTO0o9I/sddefault.jpg" width="80" alt="封面"> | [キセキ](https://www.marumaru-x.com/japanese-song/play-6xqrdj6rd4) | GReeeeN | 2.7K | 106.5K | 6:32 | 2008-05-28 | #JPOP, #GReeeeN |
| 28 | <img src="https://i.ytimg.com/vi/siQJhIp-UTU/sddefault.jpg" width="80" alt="封面"> | [手紙～拝啓十五の君へ～](https://www.marumaru-x.com/japanese-song/play-260rm20opz) | アンジェラ・アキ | 2.6K | 87.2K | 6:14 | 2008-09-17 | #JPOP, #アンジェラ・アキ |
| 29 | <img src="https://i.ytimg.com/vi/WWB01IuMvzA/hqdefault.jpg" width="80" alt="封面"> | [God knows...](https://www.marumaru-x.com/japanese-song/play-wzrv42lr3k) | 涼宮ハルヒ(平野綾) | 2.6K | 54.8K | 4:41 | 2006-06-21 | #ANM, #平野綾 |
| 30 | <img src="https://i.ytimg.com/vi/FXsGCieXm1E/sddefault.jpg" width="80" alt="封面"> | [恋愛サーキュレーション](https://www.marumaru-x.com/japanese-song/play-g9r0evgnv8) | 千石撫子(花澤香菜) | 2.6K | 81.8K | 4:14 | 2010-01-27 | #ANM, #花澤香菜 |
| 31 | <img src="https://i.ytimg.com/vi/WPl10ZrhCtk/sddefault.jpg" width="80" alt="封面"> | [悪魔の子](https://www.marumaru-x.com/japanese-song/play-y7okwdlvoq) | ヒグチアイ | 2.6K | 87.2K | 3:50 | 2022-01-10 | #ANM, #ヒグチアイ |
| 32 | <img src="https://i.ytimg.com/vi/1oMxrHXzOsY/sddefault.jpg" width="80" alt="封面"> | [ピースサイン](https://www.marumaru-x.com/japanese-song/play-vxn5pelo9e) | 米津玄師 | 2.5K | 106.4K | 4:17 | 2017-06-21 | #ANM, #米津玄師 |
| 33 | <img src="https://i.ytimg.com/vi/8iuLXODzL04/sddefault.jpg" width="80" alt="封面"> | [たぶん](https://www.marumaru-x.com/japanese-song/play-e4oy560kn3) | YOASOBI | 2.5K | 102.1K | 4:24 | 2020-07-31 | #JPOP, #YOASOBI |
| 34 | <img src="https://i.ytimg.com/vi/0xSiBpUdW4E/sddefault.jpg" width="80" alt="封面"> | [マリーゴールド](https://www.marumaru-x.com/japanese-song/play-60rm79drpz) | あいみょん | 2.4K | 115.4K | 5:22 | 2018-08-08 | #JPOP, #あいみょん |
| 35 | <img src="https://i.ytimg.com/vi/ony539T074w/sddefault.jpg" width="80" alt="封面"> | [白日](https://www.marumaru-x.com/japanese-song/play-xqrdz50od4) | King Gnu | 2.4K | 110.5K | 4:40 | 2019-02-22 | #JPOP, #King Gnu |
| 36 | <img src="https://i.ytimg.com/vi/mvkbCZfwWzA/sddefault.jpg" width="80" alt="封面"> | [Ref:rain](https://www.marumaru-x.com/japanese-song/play-g9r0p70ov8) | Aimer | 2.4K | 68.7K | 4:30 | 2018-02-21 | #ANM, #Aimer |
| 37 | <img src="https://i.ytimg.com/vi/E0d2uEQJbXs/sddefault.jpg" width="80" alt="封面"> | [晴る](https://www.marumaru-x.com/japanese-song/play-94oglyjpr0) | ヨルシカ | 2.4K | 70.7K | 4:43 | 2024-01-05 | #ANM, #ヨルシカ |
| 38 | <img src="https://i.ytimg.com/vi/c6rCRy6SrtU/sddefault.jpg" width="80" alt="封面"> | [光るなら](https://www.marumaru-x.com/japanese-song/play-v7n34jvrkw) | Goose house | 2.4K | 58K | 4:15 | 2014-11-19 | #ANM, #Goose house |
| 39 | <img src="https://i.ytimg.com/vi/lHWVOfC41L4/sddefault.jpg" width="80" alt="封面"> | [風になる](https://www.marumaru-x.com/japanese-song/play-2go28dq3o3) | つじあやの | 2.4K | 63.7K | 6:36 | 2002-06-26 | #ANM, #つじあやの |
| 40 | <img src="https://i.ytimg.com/vi/oZpYEEcvu5I/sddefault.jpg" width="80" alt="封面"> | [晩餐歌](https://www.marumaru-x.com/japanese-song/play-v7n3k6w7ok) | tuki. | 2.3K | 66.5K | 3:40 | 2023-09-29 | #JPOP, #tuki. |
| 41 | <img src="https://i.ytimg.com/vi/EqVoCfSwfUY/sddefault.jpg" width="80" alt="封面"> | [瞳をとじて](https://www.marumaru-x.com/japanese-song/play-9lkrz37oeq) | 平井堅 | 2.3K | 91.8K | 6:06 | 2004-04-28 | #JPOP, #平井堅 |
| 42 | <img src="https://i.ytimg.com/vi/iykAM_McguQ/sddefault.jpg" width="80" alt="封面"> | [優しい彗星](https://www.marumaru-x.com/japanese-song/play-q9oqlk3qn4) | YOASOBI | 2.3K | 108.4K | 3:36 | 2021-01-20 | #ANM, #YOASOBI |
| 43 | <img src="https://i.ytimg.com/vi/UhwHbSi4Z58/sddefault.jpg" width="80" alt="封面"> | [unravel](https://www.marumaru-x.com/japanese-song/play-e4oy5eymn3) | TK from 凛として時雨 | 2.2K | 45.4K | 4:27 | 2014-07-23 | #ANM, #凛として時雨 |
| 44 | <img src="https://i.ytimg.com/vi/rKsQ-3N-Bks/sddefault.jpg" width="80" alt="封面"> | [ひまわりの約束](https://www.marumaru-x.com/japanese-song/play-dvol9xdo2w) | 秦基博 | 2.2K | 86.4K | 5:17 | 2014-08-06 | #ANM, #秦基博 |
| 45 | <img src="https://i.ytimg.com/vi/Dx_fKPBPYUI/sddefault.jpg" width="80" alt="封面"> | [LOSER](https://www.marumaru-x.com/japanese-song/play-94og2d0n0j) | 米津玄師 | 2.2K | 87.1K | 4:03 | 2016-09-28 | #JPOP, #米津玄師 |
| 46 | <img src="https://i.ytimg.com/vi/zTPhw34V3rs/sddefault.jpg" width="80" alt="封面"> | [逢いたくていま](https://www.marumaru-x.com/japanese-song/play-v7n3klwkok) | MISIA | 2.2K | 88.1K | 5:59 | 2009-11-18 | #JPOP, #MISIA |
| 47 | <img src="https://i.ytimg.com/vi/T8y_RsF4TSw/sddefault.jpg" width="80" alt="封面"> | [ハッピーエンド](https://www.marumaru-x.com/japanese-song/play-g9r098grv8) | back number | 2.2K | 118.8K | 5:19 | 2016-11-16 | #JPOP, #back number |
| 48 | <img src="https://i.ytimg.com/vi/cbqvxDTLMps/sddefault.jpg" width="80" alt="封面"> | [ベテルギウス](https://www.marumaru-x.com/japanese-song/play-y7okwd6joq) | 優里 | 2.2K | 90.5K | 4:52 | 2021-11-01 | #JPOP, #優里 |
| 49 | <img src="https://i.ytimg.com/vi/HPkLvJn3rAI/sddefault.jpg" width="80" alt="封面"> | [only my railgun](https://www.marumaru-x.com/japanese-song/play-q9oqlm44n4) | fripSide | 2.1K | 50.3K | 4:22 | 2009-11-04 | #ANM, #fripSide, #南條愛乃 |
| 50 | <img src="https://i.ytimg.com/vi/l1ky3XPBdBE/sddefault.jpg" width="80" alt="封面"> | [猫](https://www.marumaru-x.com/japanese-song/play-94ogl5zxr0) | DISH// | 2.1K | 93.2K | 4:37 | 2017-08-16 | #JPOP, #DISH// |
| 51 | <img src="https://i.ytimg.com/vi/iw_1zU2MSc8/sddefault.jpg" width="80" alt="封面"> | [トリセツ](https://www.marumaru-x.com/japanese-song/play-q9oqlmqqn4) | 西野カナ | 2.1K | 75.1K | 4:29 | 2015-09-09 | #JPOP, #西野カナ |
| 52 | <img src="https://i.ytimg.com/vi/7940nuwCEYA/sddefault.jpg" width="80" alt="封面"> | [まちがいさがし](https://www.marumaru-x.com/japanese-song/play-wzrv40gyr3) | 菅田将暉 | 2.1K | 82.3K | 4:03 | 2019-05-14 | #JPOP, #菅田将暉 |
| 53 | <img src="https://i.ytimg.com/vi/UM9XNpgrqVk/sddefault.jpg" width="80" alt="封面"> | [怪獣の花唄](https://www.marumaru-x.com/japanese-song/play-y8rj9dxzn9) | Vaundy | 2.1K | 63.7K | 3:53 | 2020-05-11 | #JPOP, #Vaundy |
| 54 | <img src="https://i.ytimg.com/vi/KpsJWFuVTdI/sddefault.jpg" width="80" alt="封面"> | [ブルーバード](https://www.marumaru-x.com/japanese-song/play-14o7121zok) | いきものがかり | 2.1K | 41K | 3:37 | 2008-07-09 | #ANM, #いきものがかり |
| 55 | <img src="https://i.ytimg.com/vi/li6kSt3sb3k/sddefault.jpg" width="80" alt="封面"> | [好きだから。](https://www.marumaru-x.com/japanese-song/play-wdr6q9len3) | 『ユイカ』 | 2K | 84.1K | 5:06 | 2021-06-27 | #JPOP, #『ユイカ』 |
| 56 | <img src="https://i.ytimg.com/vi/w5OUAY1j3gQ/sddefault.jpg" width="80" alt="封面"> | [again](https://www.marumaru-x.com/japanese-song/play-2go28163o3) | YUI | 2K | 27.3K | 4:18 | 2009-06-03 | #ANM, #YUI |
| 57 | <img src="https://i.ytimg.com/vi/tLQLa6lM3Us/sddefault.jpg" width="80" alt="封面"> | [残響散歌](https://www.marumaru-x.com/japanese-song/play-72r9myl7oz) | Aimer | 2K | 74.5K | 3:02 | 2022-01-12 | #ANM, #Aimer |
| 58 | <img src="https://i.ytimg.com/vi/jpV5jeFlt_E/sddefault.jpg" width="80" alt="封面"> | [君の知らない物語](https://www.marumaru-x.com/japanese-song/play-e1pox2xryw) | supercell | 2K | 38.8K | 5:56 | 2009-08-12 | #ANM, #supercell |
| 59 | <img src="https://i.ytimg.com/vi/1tk1pqwrOys/sddefault.jpg" width="80" alt="封面"> | [廻廻奇譚](https://www.marumaru-x.com/japanese-song/play-94ogl5jkr0) | Eve | 1.9K | 82.9K | 3:44 | 2020-10-03 | #ANM, #Eve |
| 60 | <img src="https://i.ytimg.com/vi/-EKxzId_Sj4/sddefault.jpg" width="80" alt="封面"> | [アイネクライネ](https://www.marumaru-x.com/japanese-song/play-1zn4k6xre4) | 米津玄師 | 1.9K | 67.9K | 4:56 | 2014-04-23 | #JPOP, #米津玄師 |
| 61 | <img src="https://i.ytimg.com/vi/F64yFFnZfkI/sddefault.jpg" width="80" alt="封面"> | [言って。](https://www.marumaru-x.com/japanese-song/play-60rm61znpz) | ヨルシカ | 1.8K | 50.4K | 4:04 | 2017-06-28 | #JPOP, #ヨルシカ |
| 62 | <img src="https://i.ytimg.com/vi/E3hvxbM_ubw/sddefault.jpg" width="80" alt="封面"> | [大きな古時計](https://www.marumaru-x.com/japanese-song/play-e4oy562kn3) | 平井堅 | 1.8K | 38.6K | 5:21 | 2002-08-28 | #JPOP, #平井堅 |
| 63 | <img src="https://i.ytimg.com/vi/MtLHwqbE1eI/sddefault.jpg" width="80" alt="封面"> | [夢灯籠](https://www.marumaru-x.com/japanese-song/play-ywn1z0xwr7) | RADWIMPS | 1.8K | 43.4K | 2:12 | 2016-08-24 | #ANM, #RADWIMPS |
| 64 | <img src="https://i.ytimg.com/vi/-VKIqrvVOpo/sddefault.jpg" width="80" alt="封面"> | [ただ君に晴れ](https://www.marumaru-x.com/japanese-song/play-60rm455rpz) | ヨルシカ | 1.8K | 52.4K | 3:20 | 2018-05-09 | #JPOP, #ヨルシカ |
| 65 | <img src="https://i.ytimg.com/vi/9lVPAWLWtWc/sddefault.jpg" width="80" alt="封面"> | [花に亡霊](https://www.marumaru-x.com/japanese-song/play-v7n3k2gzok) | ヨルシカ | 1.8K | 53.3K | 4:03 | 2020-04-22 | #ANM, #ヨルシカ |
| 66 | <img src="https://i.ytimg.com/vi/dlFA0Zq1k2A/sddefault.jpg" width="80" alt="封面"> | [シルエット](https://www.marumaru-x.com/japanese-song/play-wdr667lr35) | KANA-BOON | 1.8K | 68.7K | 4:26 | 2014-11-26 | #ANM, #KANA-BOON |
| 67 | <img src="https://i.ytimg.com/vi/gN24W_psMpE/sddefault.jpg" width="80" alt="封面"> | [ninelie](https://www.marumaru-x.com/japanese-song/play-e4oy23mn3z) | Aimer with chelly(EGOIST) | 1.8K | 45.9K | 4:35 | 2016-05-11 | #ANM, #Aimer, #EGOIST |
| 68 | <img src="https://i.ytimg.com/vi/1wxTksLZ1Mw/hqdefault.jpg" width="80" alt="封面"> | [粉雪](https://www.marumaru-x.com/japanese-song/play-v14o7znkqx) | レミオロメン | 1.8K | 54.2K | 5:33 | 2005-11-16 | #JPOP, #レミオロメン |
| 69 | <img src="https://i.ytimg.com/vi/B7BxrAAXl94/sddefault.jpg" width="80" alt="封面"> | [ギターと孤独と蒼い惑星](https://www.marumaru-x.com/japanese-song/play-pynpv6mynd) | 結束バンド | 1.8K | 59.1K | 3:54 | 2022-11-06 | #ANM, #結束バンド |
| 70 | <img src="https://i.ytimg.com/vi/eglYGbybkrY/sddefault.jpg" width="80" alt="封面"> | [嘘](https://www.marumaru-x.com/japanese-song/play-1zn4qzkjre) | シド | 1.7K | 30.4K | 3:31 | 2009-04-29 | #ANM, #シド |
| 71 | <img src="https://i.ytimg.com/vi/5TR1wJCimyk/sddefault.jpg" width="80" alt="封面"> | [涙そうそう](https://www.marumaru-x.com/japanese-song/play-2evr8qprm5) | 夏川りみ | 1.7K | 61.1K | 4:22 | 2001-03-23 | #JPOP, #夏川りみ |
| 72 | <img src="https://i.ytimg.com/vi/Qp3b-RXtz4w/sddefault.jpg" width="80" alt="封面"> | [うっせぇわ](https://www.marumaru-x.com/japanese-song/play-72r9m224oz) | Ado | 1.7K | 58.8K | 3:23 | 2020-10-23 | #JPOP, #Ado |
| 73 | <img src="https://i.ytimg.com/vi/sHgce2bDxdg/sddefault.jpg" width="80" alt="封面"> | [渡月橋 ～君 想ふ～](https://www.marumaru-x.com/japanese-song/play-y8rj6e3n9x) | 倉木麻衣 | 1.7K | 48.5K | 4:10 | 2017-04-12 | #ANM, #倉木麻衣 |
| 74 | <img src="https://i.ytimg.com/vi/cvxm8GJJHqQ/hqdefault.jpg" width="80" alt="封面"> | [心做し](https://www.marumaru-x.com/japanese-song/play-94ogl55r0j) | 花たん | 1.7K | 45.2K | 4:29 | 2021-12-10 | #COV, #花たん |
| 75 | <img src="https://i.ytimg.com/vi/0YF8vecQWYs/sddefault.jpg" width="80" alt="封面"> | [カワキヲアメク](https://www.marumaru-x.com/japanese-song/play-wdr6zpvn35) | 美波 | 1.6K | 56K | 4:14 | 2019-01-30 | #ANM, #美波 |
| 76 | <img src="https://i.ytimg.com/vi/sAuEeM_6zpk/sddefault.jpg" width="80" alt="封面"> | [あの夢をなぞって](https://www.marumaru-x.com/japanese-song/play-94ogl940r0) | YOASOBI | 1.6K | 67.2K | 4:00 | 2020-01-18 | #JPOP, #YOASOBI |
| 77 | <img src="https://i.ytimg.com/vi/lzAyrgSqeeE/sddefault.jpg" width="80" alt="封面"> | [orion](https://www.marumaru-x.com/japanese-song/play-60rml2dnpz) | 米津玄師 | 1.6K | 49.6K | 4:51 | 2017-02-15 | #ANM, #米津玄師 |
| 78 | <img src="https://i.ytimg.com/vi/Xs0Lxif1u9E/sddefault.jpg" width="80" alt="封面"> | [すずめ feat.十明](https://www.marumaru-x.com/japanese-song/play-14o71mmzok) | RADWIMPS | 1.6K | 52.7K | 3:57 | 2022-09-30 | #ANM, #十明, #RADWIMPS |
| 79 | <img src="https://i.ytimg.com/vi/GkY9dFAECt8/sddefault.jpg" width="80" alt="封面"> | [Wherever You Are](https://www.marumaru-x.com/japanese-song/play-lkrzwxyreq) | ONE OK ROCK | 1.6K | 46.5K | 4:56 | 2010-06-09 | #JPOP, #ONE OK ROCK |
| 80 | <img src="https://i.ytimg.com/vi/_0bb30seo28/sddefault.jpg" width="80" alt="封面"> | [小さな恋のうた](https://www.marumaru-x.com/japanese-song/play-v7n3qevokw) | 粉ミルク | 1.5K | 53.4K | 4:46 | 2015-12-11 | #COV, #粉ミルク |
| 81 | <img src="https://i.ytimg.com/vi/zuoVd2QNxJo/sddefault.jpg" width="80" alt="封面"> | [青のすみか](https://www.marumaru-x.com/japanese-song/play-y7okwm3joq) | キタニタツヤ | 1.5K | 65.9K | 3:21 | 2023-07-19 | #ANM, #キタニタツヤ |
| 82 | <img src="https://i.ytimg.com/vi/2B6nj38AdD0/sddefault.jpg" width="80" alt="封面"> | [紅蓮の弓矢](https://www.marumaru-x.com/japanese-song/play-lkrz5qz0re) | Linked Horizon | 1.5K | 46.8K | 5:17 | 2013-07-10 | #ANM, #Linked Horizon |
| 83 | <img src="https://i.ytimg.com/vi/JoJ6lnF07U4/sddefault.jpg" width="80" alt="封面"> | [小さな恋のうた](https://www.marumaru-x.com/japanese-song/play-94oglxepr0) | MONGOL800 | 1.5K | 66.2K | 3:43 | 2001-09-16 | #JPOP, #MONGOL800 |
| 84 | <img src="https://i.ytimg.com/vi/pHsaIsUTHdc/sddefault.jpg" width="80" alt="封面"> | [六等星の夜](https://www.marumaru-x.com/japanese-song/play-ymre1z0wnd) | Aimer | 1.5K | 16.5K | 5:38 | 2011-09-07 | #ANM, #Aimer |
| 85 | <img src="https://i.ytimg.com/vi/1aPOj0ERTEc/sddefault.jpg" width="80" alt="封面"> | [crossing field](https://www.marumaru-x.com/japanese-song/play-72r9mv7oz3) | LiSA | 1.5K | 30K | 4:09 | 2012-08-08 | #ANM, #LiSA |
| 86 | <img src="https://i.ytimg.com/vi/1re05dQMhzw/sddefault.jpg" width="80" alt="封面"> | [THERE IS A REASON](https://www.marumaru-x.com/japanese-song/play-14o7ggzokq) | 鈴木このみ | 1.5K | 40K | 4:53 | 2017-12-20 | #ANM, #鈴木このみ |
| 87 | <img src="https://i.ytimg.com/vi/uxYLXaXtH9I/sddefault.jpg" width="80" alt="封面"> | [レオ](https://www.marumaru-x.com/japanese-song/play-1poxqvz7ry) | 優里 | 1.5K | 57K | 4:29 | 2022-01-12 | #JPOP, #優里 |
| 88 | <img src="https://i.ytimg.com/vi/bN1t3-2X3aM/sddefault.jpg" width="80" alt="封面"> | [茜さす](https://www.marumaru-x.com/japanese-song/play-y8rjjq6r9x) | Aimer | 1.5K | 39.7K | 5:40 | 2016-11-16 | #ANM, #Aimer |
| 89 | <img src="https://i.ytimg.com/vi/A_1t2Dkd2Io/hqdefault.jpg" width="80" alt="封面"> | [恋音と雨空](https://www.marumaru-x.com/japanese-song/play-072r9d5oz3) | AAA | 1.5K | 40.7K | 5:19 | 2013-09-04 | #JPOP, #AAA |
| 90 | <img src="https://i.ytimg.com/vi/LKqgY0VKZX4/sddefault.jpg" width="80" alt="封面"> | [Departures ～あなたにおくるアイの歌～](https://www.marumaru-x.com/japanese-song/play-ymreq66rd3) | EGOIST | 1.4K | 24.5K | 4:20 | 2011-11-30 | #ANM, #EGOIST |
| 91 | <img src="https://i.ytimg.com/vi/t6xdg6TKbyQ/sddefault.jpg" width="80" alt="封面"> | [プラネタリウム](https://www.marumaru-x.com/japanese-song/play-14o71v7okq) | 大塚愛 | 1.4K | 33.5K | 5:11 | 2005-09-21 | #JPOP, #大塚愛 |
| 92 | <img src="https://i.ytimg.com/vi/YnSW8ian29w/sddefault.jpg" width="80" alt="封面"> | [踊](https://www.marumaru-x.com/japanese-song/play-v7n3kgp6ok) | Ado | 1.4K | 47K | 3:29 | 2021-04-27 | #JPOP, #Ado |
| 93 | <img src="https://i.ytimg.com/vi/EQ94zflNqn4/sddefault.jpg" width="80" alt="封面"> | [愛にできることはまだあるかい](https://www.marumaru-x.com/japanese-song/play-pynpvjppnd) | RADWIMPS | 1.4K | 54.7K | 7:29 | 2019-07-19 | #ANM, #RADWIMPS |
| 94 | <img src="https://i.ytimg.com/vi/3eytpBOkOFA/sddefault.jpg" width="80" alt="封面"> | [祝福](https://www.marumaru-x.com/japanese-song/play-94ogl005r0) | YOASOBI | 1.4K | 58.4K | 3:18 | 2022-10-01 | #ANM, #YOASOBI |
| 95 | <img src="https://i.ytimg.com/vi/M80XXxMKFWw/hqdefault.jpg" width="80" alt="封面"> | [そばにいるね](https://www.marumaru-x.com/japanese-song/play-g1zn4m7ne4) | 青山テルマ feat.SoulJa | 1.4K | 32K | 5:17 | 2008-01-23 | #JPOP, #青山テルマ, #SoulJa |
| 96 | <img src="https://i.ytimg.com/vi/_CV5wVHjMfQ/sddefault.jpg" width="80" alt="封面"> | [歌に形はないけれど](https://www.marumaru-x.com/japanese-song/play-9lkrzgyneq) | 花たん | 1.4K | 36.9K | 5:31 | 2013-07-31 | #COV, #花たん |
| 97 | <img src="https://i.ytimg.com/vi/GA0MxdEYsGM/sddefault.jpg" width="80" alt="封面"> | [This game](https://www.marumaru-x.com/japanese-song/play-pynp4xyndm) | 鈴木このみ | 1.4K | 27.6K | 4:42 | 2014-05-21 | #ANM, #鈴木このみ |
| 98 | <img src="https://i.ytimg.com/vi/h-KuoHHjGRs/sddefault.jpg" width="80" alt="封面"> | [瞬き](https://www.marumaru-x.com/japanese-song/play-wzrv394n3k) | back number | 1.4K | 49.9K | 5:25 | 2017-12-20 | #JPOP, #back number |
| 99 | <img src="https://i.ytimg.com/vi/KTZ-y85Erus/sddefault.jpg" width="80" alt="封面"> | [だから僕は音楽を辞めた](https://www.marumaru-x.com/japanese-song/play-1pox1jknyw) | ヨルシカ | 1.4K | 40.7K | 4:07 | 2019-04-10 | #JPOP, #ヨルシカ |
| 100 | <img src="https://i.ytimg.com/vi/SII-S-zCg-c/sddefault.jpg" width="80" alt="封面"> | [高嶺の花子さん](https://www.marumaru-x.com/japanese-song/play-wzrvd4lr3k) | back number | 1.4K | 60.1K | 4:57 | 2013-06-26 | #JPOP, #back number |
| 101 | <img src="https://i.ytimg.com/vi/uwph0dv9E6U/sddefault.jpg" width="80" alt="封面"> | [Sincerely](https://www.marumaru-x.com/japanese-song/play-ymree0krd3) | TRUE | 1.4K | 27.6K | 4:43 | 2018-01-31 | #ANM, #TRUE |
| 102 | <img src="https://i.ytimg.com/vi/tIhL2KHVdgE/sddefault.jpg" width="80" alt="封面"> | [STYX HELIX](https://www.marumaru-x.com/japanese-song/play-e4oymvxo3z) | MYTH & ROID | 1.3K | 43.6K | 4:46 | 2016-05-25 | #ANM, #MYTH & ROID |
| 103 | <img src="https://i.ytimg.com/vi/LJkn2qqtijk/sddefault.jpg" width="80" alt="封面"> | [Catch the Moment](https://www.marumaru-x.com/japanese-song/play-1poxedyryw) | LiSA | 1.3K | 36.2K | 4:46 | 2017-02-15 | #ANM, #LiSA |
| 104 | <img src="https://i.ytimg.com/vi/RHBumUYrap4/hqdefault.jpg" width="80" alt="封面"> | [おはよう。](https://www.marumaru-x.com/japanese-song/play-ywn1zejr7l) | Keno | 1.3K | 31.1K | 4:36 | 2000-01-01 | #ANM, #Keno |
| 105 | <img src="https://i.ytimg.com/vi/qiX5DI--8bg/sddefault.jpg" width="80" alt="封面"> | [名前のない怪物](https://www.marumaru-x.com/japanese-song/play-14o716vdok) | EGOIST | 1.3K | 20.4K | 6:00 | 2012-12-05 | #ANM, #EGOIST |
| 106 | <img src="https://i.ytimg.com/vi/VQ2D8rZljwU/sddefault.jpg" width="80" alt="封面"> | [Brave Shine](https://www.marumaru-x.com/japanese-song/play-1pox4v4nyw) | Aimer | 1.3K | 30.1K | 3:54 | 2015-06-03 | #ANM, #Aimer |
| 107 | <img src="https://i.ytimg.com/vi/0wPkUlXIVP4/sddefault.jpg" width="80" alt="封面"> | [蝶々結び](https://www.marumaru-x.com/japanese-song/play-y8rjmv6r9x) | Aimer | 1.3K | 43.7K | 6:06 | 2016-08-17 | #JPOP, #Aimer |
| 108 | <img src="https://i.ytimg.com/vi/dvXRX5RJiIo/sddefault.jpg" width="80" alt="封面"> | [エウテルペ](https://www.marumaru-x.com/japanese-song/play-14o715ydok) | EGOIST | 1.3K | 15.3K | 3:49 | 2011-11-30 | #JPOP, #EGOIST |
| 109 | <img src="https://i.ytimg.com/vi/sOiMD45QGLs/sddefault.jpg" width="80" alt="封面"> | [ギラギラ](https://www.marumaru-x.com/japanese-song/play-1zn4qke7re) | Ado | 1.3K | 44.5K | 4:37 | 2021-02-14 | #JPOP, #Ado |
| 110 | <img src="https://i.ytimg.com/vi/pm9JyMiAU6A/sddefault.jpg" width="80" alt="封面"> | [再会](https://www.marumaru-x.com/japanese-song/play-94oglxjpr0) | LiSA×Uru | 1.3K | 47.8K | 4:03 | 2020-11-16 | #CM, #LiSA, #Uru |
| 111 | <img src="https://i.ytimg.com/vi/61z-cqg28R8/sddefault.jpg" width="80" alt="封面"> | [SAKURA](https://www.marumaru-x.com/japanese-song/play-v14o737rkq) | いきものがかり | 1.3K | 31.5K | 6:00 | 2006-03-15 | #JPOP, #いきものがかり |
| 112 | <img src="https://i.ytimg.com/vi/d9eudCNJv1E/sddefault.jpg" width="80" alt="封面"> | [あなただけ見つめてる](https://www.marumaru-x.com/japanese-song/play-2go284k4o3) | 大黒摩季 | 1.3K | 34.7K | 4:44 | 1993-12-10 | #ANM, #大黒摩季 |
| 113 | <img src="https://i.ytimg.com/vi/OIBODIPC_8Y/sddefault.jpg" width="80" alt="封面"> | [勇者](https://www.marumaru-x.com/japanese-song/play-lkrz5996re) | YOASOBI | 1.3K | 44.7K | 3:24 | 2023-09-29 | #ANM, #YOASOBI |
| 114 | <img src="https://i.ytimg.com/vi/kzdJkT4kp-A/sddefault.jpg" width="80" alt="封面"> | [ハルジオン](https://www.marumaru-x.com/japanese-song/play-lkrz5zm7re) | YOASOBI | 1.3K | 48.5K | 3:23 | 2020-05-11 | #OTH, #YOASOBI |
| 115 | <img src="https://i.ytimg.com/vi/MgNItWdfEIU/sddefault.jpg" width="80" alt="封面"> | [スパークル [original ver.]](https://www.marumaru-x.com/japanese-song/play-60rm90z0np) | RADWIMPS | 1.3K | 46.1K | 6:51 | 2016-11-23 | #JPOP, #RADWIMPS |
| 116 | <img src="https://i.ytimg.com/vi/pURmemr5LRM/sddefault.jpg" width="80" alt="封面"> | [brave heart](https://www.marumaru-x.com/japanese-song/play-q9oqlkmn4y) | 宮崎歩 | 1.3K | 32.2K | 4:12 | 1999-06-25 | #ANM, #宮崎歩 |
| 117 | <img src="https://i.ytimg.com/vi/wSTbdqo-j74/sddefault.jpg" width="80" alt="封面"> | [星座になれたら](https://www.marumaru-x.com/japanese-song/play-wzrv4vdlr3) | 結束バンド | 1.2K | 36.2K | 4:15 | 2022-12-25 | #ANM, #結束バンド |
| 118 | <img src="https://i.ytimg.com/vi/hkBbUf4oGfA/sddefault.jpg" width="80" alt="封面"> | [虹](https://www.marumaru-x.com/japanese-song/play-wzrv4z57r3) | 菅田将暉 | 1.2K | 61.1K | 4:32 | 2020-11-10 | #ANM, #菅田将暉 |
| 119 | <img src="https://i.ytimg.com/vi/JUbU6VLV6yI/sddefault.jpg" width="80" alt="封面"> | [365日の紙飛行機](https://www.marumaru-x.com/japanese-song/play-72r993erz3) | AKB48 | 1.2K | 70.6K | 5:06 | 2015-12-09 | #JPOP, #AKB48 |
| 120 | <img src="https://i.ytimg.com/vi/eKoD2CRr_KA/sddefault.jpg" width="80" alt="封面"> | [表裏一体](https://www.marumaru-x.com/japanese-song/play-pynpvpxndm) | ゆず | 1.2K | 31.7K | 5:47 | 2013-12-25 | #JPOP, #ゆず |
| 121 | <img src="https://i.ytimg.com/vi/v5JjlzWbkNQ/sddefault.jpg" width="80" alt="封面"> | [Get Over](https://www.marumaru-x.com/japanese-song/play-94ogl2mkr0) | Dream | 1.2K | 25.8K | 5:13 | 2002-01-01 | #ANM, #Dream |
| 122 | <img src="https://i.ytimg.com/vi/MAn9ni-drZw/sddefault.jpg" width="80" alt="封面"> | [if](https://www.marumaru-x.com/japanese-song/play-ymre17jwnd) | 西野カナ | 1.2K | 24.5K | 4:53 | 2010-08-04 | #ANM, #西野カナ |
| 123 | <img src="https://i.ytimg.com/vi/7HgJIAUtICU/sddefault.jpg" width="80" alt="封面"> | [踊り子](https://www.marumaru-x.com/japanese-song/play-v7n3k7x7ok) | Vaundy | 1.2K | 40K | 4:06 | 2021-11-17 | #JPOP, #Vaundy |
| 124 | <img src="https://i.ytimg.com/vi/F-Cm-bmdLEY/sddefault.jpg" width="80" alt="封面"> | [オレンジ](https://www.marumaru-x.com/japanese-song/play-wdr60lgr35) | 7!! | 1.2K | 29.6K | 5:52 | 2015-02-11 | #JPOP, #7!! |
| 125 | <img src="https://i.ytimg.com/vi/EEMwA8KZAqg/sddefault.jpg" width="80" alt="封面"> | [生きていたんだよな](https://www.marumaru-x.com/japanese-song/play-1poxj07nyw) | あいみょん | 1.2K | 42.4K | 3:22 | 2016-11-30 | #JPOP, #あいみょん |
| 126 | <img src="https://i.ytimg.com/vi/nEukZalW7Ac/sddefault.jpg" width="80" alt="封面"> | [名前を呼ぶよ](https://www.marumaru-x.com/japanese-song/play-v7n3kxvvok) | ラックライフ | 1.2K | 41.3K | 4:34 | 2016-05-11 | #ANM, #ラックライフ |
| 127 | <img src="https://i.ytimg.com/vi/jcSVUFplqrA/sddefault.jpg" width="80" alt="封面"> | [僕が死のうと思ったのは](https://www.marumaru-x.com/japanese-song/play-2go20m0n3p) | amazarashi | 1.2K | 71.4K | 6:08 | 2016-02-24 | #JPOP, #amazarashi |
| 128 | <img src="https://i.ytimg.com/vi/M6gcoDN9jBc/sddefault.jpg" width="80" alt="封面"> | [逆夢](https://www.marumaru-x.com/japanese-song/play-60rm9x2znp) | King Gnu | 1.2K | 47.4K | 5:20 | 2021-12-29 | #ANM, #King Gnu |
| 129 | <img src="https://i.ytimg.com/vi/9MjAJSoaoSo/sddefault.jpg" width="80" alt="封面"> | [香水](https://www.marumaru-x.com/japanese-song/play-pynpv46ynd) | 瑛人 | 1.2K | 55.2K | 4:20 | 2019-04-21 | #JPOP, #瑛人 |
| 130 | <img src="https://i.ytimg.com/vi/24K4oZjv01I/sddefault.jpg" width="80" alt="封面"> | [aLIEz](https://www.marumaru-x.com/japanese-song/play-xqrd95q5nd) | SawanoHiroyuki[nZk]:mizuki | 1.2K | 21.9K | 4:37 | 2014-09-10 | #ANM, #SawanoHiroyuki[nZk], #mizuki |
| 131 | <img src="https://i.ytimg.com/vi/-J9FuvPmMoI/sddefault.jpg" width="80" alt="封面"> | [スパークル (movie ver.)](https://www.marumaru-x.com/japanese-song/play-ymre3w8od3) | RADWIMPS | 1.2K | 26.3K | 8:58 | 2016-08-24 | #ANM, #RADWIMPS |
| 132 | <img src="https://i.ytimg.com/vi/FaRmThAbyOU/sddefault.jpg" width="80" alt="封面"> | [DAN DAN 心魅かれてく](https://www.marumaru-x.com/japanese-song/play-lvnw1lkqo7) | FIELD OF VIEW | 1.2K | 28.7K | 3:36 | 1996-03-11 | #ANM, #FIELD OF VIEW |
| 133 | <img src="https://i.ytimg.com/vi/I7ZdoZQesEA/sddefault.jpg" width="80" alt="封面"> | [世界に一つだけの花](https://www.marumaru-x.com/japanese-song/play-1zn4qzdxre) | SMAP | 1.2K | 15.5K | 4:37 | 2002-07-24 | #JPOP, #SMAP |
| 134 | <img src="https://i.ytimg.com/vi/D_Oyplmhhv0/sddefault.jpg" width="80" alt="封面"> | [喜劇](https://www.marumaru-x.com/japanese-song/play-lvnw1x23o7) | 星野源 | 1.2K | 37.3K | 4:36 | 2022-04-08 | #ANM, #星野源 |
| 135 | <img src="https://i.ytimg.com/vi/ngm99aJh7ig/sddefault.jpg" width="80" alt="封面"> | [LAST STARDUST](https://www.marumaru-x.com/japanese-song/play-wdr6qymln3) | Aimer | 1.2K | 20.4K | 5:19 | 2015-07-29 | #ANM, #Aimer |
| 136 | <img src="https://i.ytimg.com/vi/ytQ3Hs3WjQ4/sddefault.jpg" width="80" alt="封面"> | [明日への手紙](https://www.marumaru-x.com/japanese-song/play-ywn1zpmer7) | 手嶌葵 | 1.2K | 35.2K | 5:32 | 2014-07-23 | #JPOP, #手嶌葵 |
| 137 | <img src="https://i.ytimg.com/vi/09z87O1CgIw/sddefault.jpg" width="80" alt="封面"> | [KING](https://www.marumaru-x.com/japanese-song/play-v7n3kgjvok) | 天神子兎音 | 1.2K | 39.3K | 2:15 | 2020-09-11 | #COV, #天神子兎音 |
| 138 | <img src="https://i.ytimg.com/vi/4xuP6Wnkqpc/sddefault.jpg" width="80" alt="封面"> | [Time after time～花舞う街で～](https://www.marumaru-x.com/japanese-song/play-ywn137jo7l) | 倉木麻衣 | 1.2K | 29.7K | 4:11 | 2003-03-05 | #ANM, #倉木麻衣 |
| 139 | <img src="https://i.ytimg.com/vi/jbHG7fsZVkM/sddefault.jpg" width="80" alt="封面"> | [めざせポケモンマスター](https://www.marumaru-x.com/japanese-song/play-xqrd9k86nd) | 松本梨香 | 1.2K | 19.1K | 4:13 | 1997-06-28 | #ANM, #松本梨香 |
| 140 | <img src="https://i.ytimg.com/vi/eWeSqrRk-gs/sddefault.jpg" width="80" alt="封面"> | [メリーゴーランド](https://www.marumaru-x.com/japanese-song/play-60rm9g65np) | 優里 | 1.2K | 50.2K | 5:14 | 2022-12-22 | #ANM, #優里 |
| 141 | <img src="https://i.ytimg.com/vi/0q6c0AKDKU4/sddefault.jpg" width="80" alt="封面"> | [ミカヅキ](https://www.marumaru-x.com/japanese-song/play-g9r00vgrv8) | さユり | 1.2K | 29K | 4:30 | 2015-08-26 | #ANM, #さユり |
| 142 | <img src="https://i.ytimg.com/vi/vVGa8I0Atcg/sddefault.jpg" width="80" alt="封面"> | [空色デイズ](https://www.marumaru-x.com/japanese-song/play-evr81ddnm5) | 中川翔子 | 1.2K | 22.9K | 4:22 | 2007-06-27 | #ANM, #中川翔子 |
| 143 | <img src="https://i.ytimg.com/vi/bt8wNQJaKAk/sddefault.jpg" width="80" alt="封面"> | [I LOVE...](https://www.marumaru-x.com/japanese-song/play-e4oy5kzdn3) | Official髭男dism | 1.2K | 58.6K | 4:49 | 2020-02-12 | #JPOP, #Official髭男dism |
| 144 | <img src="https://i.ytimg.com/vi/a3FgmTfvJhA/sddefault.jpg" width="80" alt="封面"> | [可愛くてごめん](https://www.marumaru-x.com/japanese-song/play-xqrd9mp5nd) | かぴ | 1.1K | 45.5K | 3:42 | 2022-08-28 | #JPOP, #HoneyWorks, #かぴ |
| 145 | <img src="https://i.ytimg.com/vi/9qhJ1vhTH7A/sddefault.jpg" width="80" alt="封面"> | [君がくれた夏](https://www.marumaru-x.com/japanese-song/play-xqrd96q5nd) | 家入レオ | 1.1K | 38.9K | 4:40 | 2015-08-19 | #JPOP, #家入レオ |
| 146 | <img src="https://i.ytimg.com/vi/1zwaZkOXXqw/sddefault.jpg" width="80" alt="封面"> | [DADDY! DADDY! DO! feat. 鈴木愛理](https://www.marumaru-x.com/japanese-song/play-y7okwz4voq) | 鈴木雅之 | 1.1K | 24.3K | 4:15 | 2020-04-15 | #ANM, #鈴木雅之, #鈴木愛理 |
| 147 | <img src="https://i.ytimg.com/vi/-XgOWOS9btU/sddefault.jpg" width="80" alt="封面"> | [小さな恋のうた](https://www.marumaru-x.com/japanese-song/play-wdr6q849n3) | 新垣結衣と少年少女ガッキー団 | 1.1K | 28.2K | 5:25 | 2010-09-22 | #JPOP, #新垣結衣 |
| 148 | <img src="https://i.ytimg.com/vi/aHIR33pOUv0/sddefault.jpg" width="80" alt="封面"> | [Everything](https://www.marumaru-x.com/japanese-song/play-260rmjzrpz) | MISIA | 1.1K | 31K | 7:09 | 2000-10-25 | #JPOP, #MISIA |
| 149 | <img src="https://i.ytimg.com/vi/r93rVW--5ZU/sddefault.jpg" width="80" alt="封面"> | [晩餐歌](https://www.marumaru-x.com/japanese-song/play-g9r05g6dnv) | tuki.×優里 | 1.1K | 50.2K | 3:51 | 2023-11-06 | #JPOP, #tuki., #優里 |
| 150 | <img src="https://i.ytimg.com/vi/40dJS_LC6S8/sddefault.jpg" width="80" alt="封面"> | [泥中に咲く](https://www.marumaru-x.com/japanese-song/play-v7n31jzrkw) | ウォルピスカーター | 1.1K | 32.1K | 4:51 | 2018-12-26 | #JPOP, #ウォルピスカーター |
| 151 | <img src="https://i.ytimg.com/vi/kagoEGKHZvU/sddefault.jpg" width="80" alt="封面"> | [NIGHT DANCER](https://www.marumaru-x.com/japanese-song/play-xqrd9m46nd) | imase | 1.1K | 37.7K | 3:31 | 2022-08-19 | #JPOP, #imase |
| 152 | <img src="https://i.ytimg.com/vi/Rwzy6Qt8gq8/sddefault.jpg" width="80" alt="封面"> | [花の塔](https://www.marumaru-x.com/japanese-song/play-72r9mj69oz) | さユり | 1.1K | 29.6K | 4:36 | 2022-07-03 | #ANM, #さユり |
| 153 | <img src="https://i.ytimg.com/vi/TXpGWhdwXuo/sddefault.jpg" width="80" alt="封面"> | [僕らの手には何もないけど、](https://www.marumaru-x.com/japanese-song/play-1zn4kdmre4) | RAM WIRE | 1.1K | 32.6K | 4:26 | 2015-05-27 | #JPOP, #RAM WIRE |
| 154 | <img src="https://i.ytimg.com/vi/5CSNv9MNEC4/sddefault.jpg" width="80" alt="封面"> | [Don't say“lazy”](https://www.marumaru-x.com/japanese-song/play-dvol9mg4o2) | 放課後ティータイム | 1.1K | 11.8K | 4:24 | 2009-04-22 | #ANM, #放課後ティータイム |
| 155 | <img src="https://i.ytimg.com/vi/GB3DN7B4mx4/sddefault.jpg" width="80" alt="封面"> | [レイン](https://www.marumaru-x.com/japanese-song/play-1poxq24kry) | シド | 1.1K | 14.2K | 4:20 | 2010-06-02 | #ANM, #シド |
| 156 | <img src="https://i.ytimg.com/vi/Lq2-HHP04jM/sddefault.jpg" width="80" alt="封面"> | [変わらないもの](https://www.marumaru-x.com/japanese-song/play-94oglzv5r0) | 奥華子 | 1.1K | 11K | 4:46 | 2006-07-12 | #ANM, #奥華子 |
| 157 | <img src="https://i.ytimg.com/vi/NCPH9JUFESA/sddefault.jpg" width="80" alt="封面"> | [負けないで](https://www.marumaru-x.com/japanese-song/play-60rm98pdnp) | ZARD | 1.1K | 63.2K | 4:40 | 1993-01-27 | #JPOP, #ZARD |
| 158 | <img src="https://i.ytimg.com/vi/VhdxHln7TOU/sddefault.jpg" width="80" alt="封面"> | [Secret of my heart](https://www.marumaru-x.com/japanese-song/play-q9oql2qqn4) | 倉木麻衣 | 1.1K | 15.5K | 4:27 | 2000-04-26 | #ANM, #倉木麻衣 |
| 159 | <img src="https://i.ytimg.com/vi/wM4laths4-Y/sddefault.jpg" width="80" alt="封面"> | [世界は恋に落ちている](https://www.marumaru-x.com/japanese-song/play-ymre1j6gnd) | CHiCO with HoneyWorks | 1.1K | 17.9K | 5:21 | 2014-08-06 | #ANM, #HoneyWorks, #CHiCO |
| 160 | <img src="https://i.ytimg.com/vi/M2cckDmNLMI/sddefault.jpg" width="80" alt="封面"> | [KICK BACK](https://www.marumaru-x.com/japanese-song/play-lkrz53y6re) | 米津玄師 | 1.1K | 37K | 3:48 | 2022-10-12 | #ANM, #米津玄師 |
| 161 | <img src="https://i.ytimg.com/vi/nhOhFOoURnE/sddefault.jpg" width="80" alt="封面"> | [三原色](https://www.marumaru-x.com/japanese-song/play-xqrd9jwdnd) | YOASOBI | 1.1K | 43.7K | 3:47 | 2021-07-02 | #JPOP, #YOASOBI |
| 162 | <img src="https://i.ytimg.com/vi/a6nmtJAC4NM/sddefault.jpg" width="80" alt="封面"> | [My Dearest](https://www.marumaru-x.com/japanese-song/play-xqrdx6vnd4) | supercell | 1.1K | 18K | 5:54 | 2011-11-23 | #ANM, #supercell |
| 163 | <img src="https://i.ytimg.com/vi/H08YWE4CIFQ/sddefault.jpg" width="80" alt="封面"> | [Overdose](https://www.marumaru-x.com/japanese-song/play-pynpv6y9nd) | なとり | 1.1K | 30.5K | 3:14 | 2022-09-07 | #JPOP, #なとり |
| 164 | <img src="https://i.ytimg.com/vi/KMTo2LmixqQ/sddefault.jpg" width="80" alt="封面"> | [summertime](https://www.marumaru-x.com/japanese-song/play-y7okw5ypoq) | cinnamons × evening cinema | 1.1K | 36.2K | 4:12 | 2018-12-12 | #JPOP, #cinnamons, #evening cinema |
| 165 | <img src="https://i.ytimg.com/vi/ptnYBctoexk/sddefault.jpg" width="80" alt="封面"> | [馬と鹿](https://www.marumaru-x.com/japanese-song/play-dvol994do2) | 米津玄師 | 1.1K | 44.7K | 4:45 | 2019-09-11 | #JPOP, #米津玄師 |
| 166 | <img src="https://i.ytimg.com/vi/OcNSFV5Io0Q/sddefault.jpg" width="80" alt="封面"> | [oath sign](https://www.marumaru-x.com/japanese-song/play-v7n3klkokw) | LiSA | 1.1K | 22.9K | 4:11 | 2011-11-23 | #ANM, #LiSA |
| 167 | <img src="https://i.ytimg.com/vi/Woorod1gJ_w/sddefault.jpg" width="80" alt="封面"> | [小さな恋のうた](https://www.marumaru-x.com/japanese-song/play-dvolkjkr2w) | 天月 | 1.1K | 34.4K | 4:40 |  | #OTH, #天月 |
| 168 | <img src="https://i.ytimg.com/vi/1FliVTcX8bQ/sddefault.jpg" width="80" alt="封面"> | [新時代](https://www.marumaru-x.com/japanese-song/play-94ogl4kpr0) | Ado | 1.1K | 34.3K | 3:57 | 2022-08-10 | #ANM, #Ado |
| 169 | <img src="https://i.ytimg.com/vi/8L5cQlXMpeY/sddefault.jpg" width="80" alt="封面"> | [「僕は...」](https://www.marumaru-x.com/japanese-song/play-94ogly0er0) | あたらよ | 1.1K | 29K | 3:58 | 2024-01-08 | #ANM, #あたらよ |
| 170 | <img src="https://i.ytimg.com/vi/OZ3UuZdUHZc/sddefault.jpg" width="80" alt="封面"> | [未来へ](https://www.marumaru-x.com/japanese-song/play-g9r01q8ov8) | Kiroro | 1.1K | 27.8K | 5:30 | 1998-06-24 | #JPOP, #Kiroro |
| 171 | <img src="https://i.ytimg.com/vi/qIoDWTF0qSo/hqdefault.jpg" width="80" alt="封面"> | [深い森](https://www.marumaru-x.com/japanese-song/play-lkrz02yoeq) | Do As Infinity | 1.1K | 20.1K | 4:17 | 2001-06-27 | #ANM, #Do As Infinity |
| 172 | <img src="https://i.ytimg.com/vi/ZhMakZuBU-o/sddefault.jpg" width="80" alt="封面"> | [One more time, One more chance](https://www.marumaru-x.com/japanese-song/play-vxn5w08n9e) | 山崎まさよし | 1K | 27.7K | 5:33 | 1997-01-22 | #ANM, #山崎まさよし |
| 173 | <img src="https://i.ytimg.com/vi/QFryFamyq4U/sddefault.jpg" width="80" alt="封面"> | [星屑ビーナス](https://www.marumaru-x.com/japanese-song/play-60rmwx0opz) | Aimer | 1K | 28.5K | 4:13 | 2012-08-15 | #JPOP, #Aimer |
| 174 | <img src="https://i.ytimg.com/vi/6HYHdkEYdQE/sddefault.jpg" width="80" alt="封面"> | [いけないボーダーライン](https://www.marumaru-x.com/japanese-song/play-ymre1z36nd) | ワルキューレ | 1K | 10.9K | 4:43 | 2016-05-11 | #ANM, #ワルキューレ, #JUNNA, #鈴木みのり, #安野希世乃, #西田望見, #東山奈央 |
| 175 | <img src="https://i.ytimg.com/vi/Hh9yZWeTmVM/sddefault.jpg" width="80" alt="封面"> | [The Beginning](https://www.marumaru-x.com/japanese-song/play-lvnw15qo7x) | ONE OK ROCK | 1K | 30.9K | 5:14 | 2012-08-22 | #JPOP, #ONE OK ROCK |
| 176 | <img src="https://i.ytimg.com/vi/ERLEeGVWYxg/sddefault.jpg" width="80" alt="封面"> | [シュガーソングとビターステップ](https://www.marumaru-x.com/japanese-song/play-94ogwykn0j) | UNISON SQUARE GARDEN | 1K | 25.8K | 4:23 | 2015-05-20 | #ANM, #UNISON SQUARE GARDEN |
| 177 | <img src="https://i.ytimg.com/vi/yo-0lPwPnbo/sddefault.jpg" width="80" alt="封面"> | [会いたくて 会いたくて](https://www.marumaru-x.com/japanese-song/play-pynpvd0ndm) | 西野カナ | 1K | 28.1K | 4:44 | 2010-05-19 | #JPOP, #西野カナ |
| 178 | <img src="https://i.ytimg.com/vi/AzPWGoHvJsM/sddefault.jpg" width="80" alt="封面"> | [プラチナ](https://www.marumaru-x.com/japanese-song/play-60rm9zwznp) | 坂本真綾 | 1K | 11.8K | 4:11 | 1999-10-21 | #ANM, #坂本真綾 |
| 179 | <img src="https://i.ytimg.com/vi/ARwVe1MYAUA/sddefault.jpg" width="80" alt="封面"> | [君はロックを聴かない](https://www.marumaru-x.com/japanese-song/play-y7okxelnq9) | あいみょん | 1K | 35.9K | 4:27 | 2017-08-02 | #JPOP, #あいみょん |
| 180 | <img src="https://i.ytimg.com/vi/DuMqFknYHBs/sddefault.jpg" width="80" alt="封面"> | [イエスタデイ](https://www.marumaru-x.com/japanese-song/play-y8rj99wmn9) | Official髭男dism | 1K | 35K | 5:01 | 2019-10-09 | #JPOP, #Official髭男dism |
| 181 | <img src="https://i.ytimg.com/vi/XpM2N1y-FD8/sddefault.jpg" width="80" alt="封面"> | [いつも何度でも](https://www.marumaru-x.com/japanese-song/play-14o71z84ok) | 木村弓 | 1K | 16.2K | 3:42 | 2001-07-18 | #ANM, #木村弓 |
| 182 | <img src="https://i.ytimg.com/vi/D3IDK_R1LTg/sddefault.jpg" width="80" alt="封面"> | [Every Heart -ミンナノキモチ-](https://www.marumaru-x.com/japanese-song/play-q9oqpgqr4y) | BoA | 1K | 16.9K | 4:39 | 2002-03-13 | #JPOP, #BoA |
| 183 | <img src="https://i.ytimg.com/vi/pdGHyiPH8ig/sddefault.jpg" width="80" alt="封面"> | [終わりの世界から](https://www.marumaru-x.com/japanese-song/play-lwzrv3wn3k) | 麻枝准×やなぎなぎ | 987 | 16.6K | 5:58 | 2012-04-25 | #ANM, #やなぎなぎ |
| 184 | <img src="https://i.ytimg.com/vi/Sw1Flgub9s8/sddefault.jpg" width="80" alt="封面"> | [春泥棒](https://www.marumaru-x.com/japanese-song/play-94oglm00r0) | ヨルシカ | 983 | 33.3K | 5:00 | 2021-01-09 | #JPOP, #ヨルシカ |
| 185 | <img src="https://i.ytimg.com/vi/EXxaBXKjl6Q/sddefault.jpg" width="80" alt="封面"> | [HANABI](https://www.marumaru-x.com/japanese-song/play-e1pox4ynyw) | Mr.Children | 983 | 44.5K | 5:58 | 2008-09-03 | #JPOP, #Mr.Children |
| 186 | <img src="https://i.ytimg.com/vi/ScWlFcYn_FI/sddefault.jpg" width="80" alt="封面"> | [革命道中](https://www.marumaru-x.com/japanese-song/play-dvol96qko2) | アイナ・ジ・エンド | 982 | 35.9K | 3:21 | 2025-07-02 | #ANM, #アイナ・ジ・エンド |
| 187 | <img src="https://i.ytimg.com/vi/vd3IlOjSUGQ/sddefault.jpg" width="80" alt="封面"> | [ハルカ](https://www.marumaru-x.com/japanese-song/play-lvnw13xqo7) | YOASOBI | 978 | 39.6K | 4:05 | 2020-12-18 | #JPOP, #YOASOBI |
| 188 | <img src="https://i.ytimg.com/vi/iqEr3P78fz8/sddefault.jpg" width="80" alt="封面"> | [水平線](https://www.marumaru-x.com/japanese-song/play-1poxq5wxry) | back number | 977 | 39.8K | 5:13 | 2021-08-13 | #JPOP, #back number |
| 189 | <img src="https://i.ytimg.com/vi/XQWWS8f6X9I/sddefault.jpg" width="80" alt="封面"> | [一番の宝物](https://www.marumaru-x.com/japanese-song/play-e4oyk6dn3z) | Girls Dead Monster STARRING LiSA | 972 | 15.2K | 6:09 | 2010-12-08 | #ANM, #LiSA |
| 190 | <img src="https://i.ytimg.com/vi/Uh6dkL1M9DM/sddefault.jpg" width="80" alt="封面"> | [Flamingo](https://www.marumaru-x.com/japanese-song/play-v7n3wk3okw) | 米津玄師 | 971 | 35.3K | 3:38 | 2018-10-31 | #JPOP, #米津玄師 |
| 191 | <img src="https://i.ytimg.com/vi/M1ajQuujwKk/sddefault.jpg" width="80" alt="封面"> | [それは小さな光のような](https://www.marumaru-x.com/japanese-song/play-1zn4lkjoe4) | さユり | 971 | 22K | 4:42 | 2016-02-24 | #ANM, #さユり |
| 192 | <img src="https://i.ytimg.com/vi/Evy1FWBv9Hc/sddefault.jpg" width="80" alt="封面"> | [鳥の詩](https://www.marumaru-x.com/japanese-song/play-g9r03q0rv8) | Lia | 970 | 14.4K | 6:05 | 2000-09-08 | #ANM, #Lia |
| 193 | <img src="https://i.ytimg.com/vi/k9Eewd8TEWE/sddefault.jpg" width="80" alt="封面"> | [フォニイ](https://www.marumaru-x.com/japanese-song/play-pynpvy8ynd) | 町田ちま | 969 | 35K | 3:09 | 2021-08-05 | #COV, #町田ちま |
| 194 | <img src="https://i.ytimg.com/vi/5B8isYtE_Yw/sddefault.jpg" width="80" alt="封面"> | [季節は次々死んでいく](https://www.marumaru-x.com/japanese-song/play-q9oql244n4) | amazarashi | 967 | 30.1K | 5:40 | 2015-02-18 | #ANM, #amazarashi |
| 195 | <img src="https://i.ytimg.com/vi/T6kVa48UbUw/sddefault.jpg" width="80" alt="封面"> | [深海少女](https://www.marumaru-x.com/japanese-song/play-60rm9lpznp) | 初音ミク | 966 | 17.9K | 3:42 | 2022-12-16 | #VOC, #初音ミク |
| 196 | <img src="https://i.ytimg.com/vi/LmZD-TU96q4/sddefault.jpg" width="80" alt="封面"> | [IRIS OUT](https://www.marumaru-x.com/japanese-song/play-g9r057q2nv) | 米津玄師 | 965 | 42.9K | 2:34 | 2025-09-15 | #ANM, #米津玄師 |
| 197 | <img src="https://i.ytimg.com/vi/4vvvL8y9VHM/sddefault.jpg" width="80" alt="封面"> | [unlasting](https://www.marumaru-x.com/japanese-song/play-y8rj99e1n9) | LiSA | 965 | 22.9K | 4:54 | 2019-12-11 | #ANM, #LiSA |
| 198 | <img src="https://i.ytimg.com/vi/Z6DZP3fwVmg/sddefault.jpg" width="80" alt="封面"> | [君をのせて](https://www.marumaru-x.com/japanese-song/play-72r9mz54oz) | 井上あずみ | 959 | 12.1K | 3:25 | 2000-04-26 | #ANM, #井上あずみ |
| 199 | <img src="https://i.ytimg.com/vi/GJI4Gv7NbmE/sddefault.jpg" width="80" alt="封面"> | [秒針を噛む](https://www.marumaru-x.com/japanese-song/play-60rm7p3rpz) | ずっと真夜中でいいのに。 | 953 | 26.2K | 4:33 | 2018-11-14 | #JPOP, #ずっと真夜中でいいのに。 |
| 200 | <img src="https://i.ytimg.com/vi/fGGTf044UPI/sddefault.jpg" width="80" alt="封面"> | [ライオン](https://www.marumaru-x.com/japanese-song/play-q9oq06mn4y) | 中島愛、May'n | 951 | 16.3K | 5:04 | 2008-08-20 | #ANM, #中島愛, #May'n |
