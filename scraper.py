import sys
import csv
import time
import random
import json
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# 確保在 Windows 控制台輸出日文等 Unicode 字元時不會因為編碼（如 CP950）錯誤而崩潰
sys.stdout.reconfigure(encoding='utf-8')

# 目標基礎網址
BASE_URL = "https://www.marumaru-x.com/japanese-song/most-liked"
# 輸出的 CSV 檔案名稱
OUTPUT_CSV = "top200_songs.csv"
# 目標收集筆數
TARGET_COUNT = 200

# HTML 範本字串，將被填入 JSON 資料和時間
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日語熱門歌曲排行榜 - Top 200 Most Liked</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;800&family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    
    <style>
        /* CSS resets & custom scrollbar */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0d0e12;
        }
        ::-webkit-scrollbar-thumb {
            background: #2a2c3a;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #7c4dff;
        }
        
        :root {
            --bg-primary: #0a0b10;
            --bg-secondary: #12131a;
            --bg-glass: rgba(18, 19, 26, 0.75);
            --border-glass: rgba(255, 255, 255, 0.08);
            --border-active: rgba(124, 77, 255, 0.5);
            --accent: #7c4dff;
            --accent-glow: rgba(124, 77, 255, 0.3);
            --text-primary: #ffffff;
            --text-secondary: #a9abb6;
            --text-muted: #646672;
            --card-hover: rgba(255, 255, 255, 0.02);
            --transition-speed: 0.3s;
        }

        body {
            font-family: 'Outfit', 'Noto Sans TC', sans-serif;
            background: linear-gradient(rgba(10, 11, 16, 0.5), rgba(10, 11, 16, 0.85)), url('sakura_forest.png') no-repeat center center fixed;
            background-size: cover;
            color: var(--text-primary);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
            padding-bottom: 60px;
        }

        /* Ambient Glow Blobs */
        .ambient-glow {
            position: absolute;
            width: 45vw;
            height: 45vw;
            border-radius: 50%;
            filter: blur(120px);
            z-index: -1;
            opacity: 0.12;
            pointer-events: none;
        }
        .glow-1 {
            background: radial-gradient(circle, #7c4dff 0%, transparent 70%);
            top: -10vw;
            left: -10vw;
        }
        .glow-2 {
            background: radial-gradient(circle, #00e5ff 0%, transparent 70%);
            bottom: 10vw;
            right: -10vw;
        }

        /* Sakura Falling Canvas */
        #sakura-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
        }

        /* Container */
        .container {
            max-width: 1300px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }

        /* Header */
        header {
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }
        .logo-area {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 0.5rem;
        }
        .logo-icon {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #7c4dff 0%, #00e5ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 2s infinite alternate;
        }
        @keyframes pulse {
            0% { transform: scale(1); filter: drop-shadow(0 0 2px var(--accent-glow)); }
            100% { transform: scale(1.05); filter: drop-shadow(0 0 10px var(--accent)); }
        }
        h1 {
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 50%, #a9abb6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            font-size: 1.1rem;
            color: var(--text-secondary);
            font-weight: 300;
        }
        .last-update {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.5rem;
        }

        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        .stat-card {
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1.25rem;
            transition: all var(--transition-speed) ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            border-color: var(--border-active);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        .stat-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: rgba(124, 77, 255, 0.1);
            color: var(--accent);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        .stat-icon.plays {
            background: rgba(0, 229, 255, 0.1);
            color: #00e5ff;
        }
        .stat-icon.singer {
            background: rgba(255, 64, 129, 0.1);
            color: #ff4081;
        }
        .stat-info .stat-val {
            font-size: 1.5rem;
            font-weight: 700;
        }
        .stat-info .stat-lbl {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        /* Toolbar controls */
        .controls-panel {
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            align-items: center;
            justify-content: space-between;
        }
        .search-box {
            position: relative;
            flex: 1;
            min-width: 280px;
        }
        .search-box i {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 1.1rem;
        }
        .search-input {
            width: 100%;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            padding: 0.75rem 1rem 0.75rem 2.75rem;
            color: var(--text-primary);
            font-size: 0.95rem;
            outline: none;
            transition: all var(--transition-speed);
        }
        .search-input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 10px var(--accent-glow);
        }
        
        .filter-selects {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }
        .custom-select {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            color: var(--text-primary);
            outline: none;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all var(--transition-speed);
        }
        .custom-select:focus {
            border-color: var(--accent);
        }

        .layout-toggle {
            display: flex;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            padding: 4px;
        }
        .layout-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1rem;
            transition: all var(--transition-speed);
        }
        .layout-btn.active {
            background: var(--accent);
            color: #fff;
        }

        /* Song List / Grid Container */
        .songs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            transition: all var(--transition-speed);
        }
        .song-card {
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: all var(--transition-speed) cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        .song-card:hover {
            transform: translateY(-8px) scale(1.02);
            border-color: var(--border-active);
            box-shadow: 0 15px 30px rgba(124, 77, 255, 0.15);
        }

        /* Image part of card */
        .card-img-wrap {
            position: relative;
            width: 100%;
            padding-top: 56.25%; /* 16:9 Aspect Ratio */
            background-color: #000;
            overflow: hidden;
        }
        .card-img {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        .song-card:hover .card-img {
            transform: scale(1.1);
        }
        .rank-badge {
            position: absolute;
            top: 12px;
            left: 12px;
            background: linear-gradient(135deg, #7c4dff 0%, #00e5ff 100%);
            color: #fff;
            font-weight: 800;
            font-size: 0.9rem;
            padding: 4px 10px;
            border-radius: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
            z-index: 2;
        }
        .duration-badge {
            position: absolute;
            bottom: 8px;
            right: 8px;
            background: rgba(0,0,0,0.7);
            color: #fff;
            font-size: 0.8rem;
            padding: 2px 6px;
            border-radius: 4px;
            backdrop-filter: blur(4px);
        }

        /* Card Content */
        .card-body {
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        .song-title {
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .song-title a {
            color: var(--text-primary);
            text-decoration: none;
            transition: color 0.2s;
        }
        .song-title a:hover {
            color: #00e5ff;
        }
        .song-singer {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            font-weight: 400;
        }

        /* Card stats info */
        .card-stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.85rem;
        }
        .card-stat-item {
            display: flex;
            align-items: center;
            gap: 4px;
            color: var(--text-secondary);
        }
        .card-stat-item.likes i {
            color: #ff4081;
        }
        .card-stat-item.plays i {
            color: #00e5ff;
        }

        /* Footer tags */
        .card-tags {
            margin-top: 0.75rem;
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }
        .tag-badge {
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 20px;
            background: rgba(255,255,255,0.05);
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.2s;
        }
        .tag-badge:hover {
            background: var(--accent);
            color: #fff;
        }

        /* Table View Layout (List mode) */
        .table-container {
            width: 100%;
            overflow-x: auto;
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            display: none; /* Controlled by script */
        }
        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.95rem;
        }
        th, td {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        th {
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
            background: rgba(0,0,0,0.1);
        }
        tr {
            transition: background-color var(--transition-speed);
        }
        tr:hover {
            background-color: var(--card-hover);
        }
        .table-thumb {
            width: 60px;
            height: 34px;
            object-fit: cover;
            border-radius: 4px;
            vertical-align: middle;
            border: 1px solid var(--border-glass);
        }
        .table-title {
            font-weight: 600;
        }
        .table-title a {
            color: #fff;
            text-decoration: none;
            transition: color 0.2s;
        }
        .table-title a:hover {
            color: #00e5ff;
        }
        .table-rank {
            font-weight: 800;
            color: var(--accent);
        }

        /* Pagination & No Results */
        .no-results {
            grid-column: 1 / -1;
            text-align: center;
            padding: 4rem 2rem;
            font-size: 1.2rem;
            color: var(--text-secondary);
            display: none;
        }

        /* Responsive styling */
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            h1 {
                font-size: 1.8rem;
            }
            .controls-panel {
                flex-direction: column;
                align-items: stretch;
            }
            .filter-selects {
                justify-content: space-between;
            }
            .custom-select {
                flex: 1;
                min-width: 120px;
            }
        }

        /* Modal Styling */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 11, 16, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }
        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }
        .modal-content {
            background: var(--bg-secondary);
            border: 1px solid var(--border-glass);
            border-radius: 24px;
            width: 90%;
            max-width: 800px;
            max-height: 85vh;
            overflow-y: auto;
            padding: 2.5rem;
            position: relative;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            transform: translateY(30px);
            transition: transform 0.3s ease;
        }
        .modal-overlay.active .modal-content {
            transform: translateY(0);
        }
        .modal-close {
            position: absolute;
            top: 1.5rem;
            right: 1.5rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glass);
            color: var(--text-primary);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 1.2rem;
        }
        .modal-close:hover {
            background: var(--accent);
            border-color: var(--accent);
            transform: rotate(90deg);
        }
        .modal-header {
            display: flex;
            gap: 2rem;
            margin-bottom: 1.5rem;
            align-items: flex-start;
        }
        @media (max-width: 600px) {
            .modal-header {
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
            .modal-song-info {
                align-items: center;
            }
        }
        .modal-cover-img {
            width: 180px;
            height: 101px; /* 16:9 ratio */
            border-radius: 12px;
            object-fit: cover;
            border: 1px solid var(--border-glass);
        }
        .modal-song-info {
            display: flex;
            flex-direction: column;
            gap: 6px;
            flex-grow: 1;
        }
        .modal-rank-badge {
            background: linear-gradient(135deg, #7c4dff 0%, #00e5ff 100%);
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.85rem;
            align-self: flex-start;
        }
        @media (max-width: 600px) {
            .modal-rank-badge {
                align-self: center;
            }
        }
        .modal-song-title {
            font-size: 1.8rem;
            font-weight: 700;
        }
        .modal-song-singer {
            font-size: 1.2rem;
            color: var(--text-secondary);
        }
        .modal-stats {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-top: 6px;
        }
        .modal-stat-item {
            display: flex;
            align-items: center;
            gap: 4px;
            background: rgba(255, 255, 255, 0.03);
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid var(--border-glass);
        }
        .modal-tags-container {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 10px;
        }
        .modal-link-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(124, 77, 255, 0.15);
            border: 1px solid var(--accent);
            color: #fff;
            padding: 6px 14px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 0.9rem;
            margin-top: 12px;
            transition: all 0.2s ease;
        }
        .modal-link-btn:hover {
            background: var(--accent);
            box-shadow: 0 0 10px var(--accent-glow);
        }
        .modal-divider {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--border-glass), transparent);
            margin: 1.5rem 0;
        }
        .lyrics-section-title {
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .lyrics-section-title::before {
            content: '';
            display: inline-block;
            width: 4px;
            height: 16px;
            background: var(--accent);
            border-radius: 2px;
        }
        .lyrics-container {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            padding-bottom: 2rem;
        }
        .lyric-line {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            padding: 4px 0;
        }
        .lyric-ja {
            font-family: 'Noto Sans JP', 'Noto Sans TC', sans-serif;
            font-size: 1.3rem;
            line-height: 2.3rem;
            color: #ffffff;
        }
        .lyric-ja ruby {
            ruby-position: over;
        }
        .lyric-ja rt {
            font-size: 0.6em;
            color: #00e5ff;
            padding-bottom: 0.1em;
            letter-spacing: 0.05em;
        }
        .lyric-zh {
            font-family: 'Noto Sans TC', sans-serif;
            font-size: 1.05rem;
            color: #ffb7d5;
            margin-top: 4px;
            line-height: 1.5rem;
        }
        .lyrics-loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 3rem 0;
            gap: 12px;
        }
        .lyrics-loading .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid rgba(124, 77, 255, 0.1);
            border-radius: 50%;
            border-top-color: var(--accent);
            animation: spin 1s linear infinite;
        }
        .lyrics-error {
            text-align: center;
            padding: 3rem 0;
            color: #ff1744;
        }
        .lyrics-error i {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            display: block;
        }

        /* App Layout holding main content and sidebar */
        .app-layout {
            display: flex;
            max-width: 1500px;
            margin: 0 auto;
            gap: 2rem;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }
        .main-content {
            flex: 1;
            min-width: 0;
        }
        
        /* Sidebar Chatbot styling */
        .chatbot-sidebar {
            width: 380px;
            flex-shrink: 0;
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            border-radius: 24px;
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            display: flex;
            flex-direction: column;
            height: calc(100vh - 4rem);
            position: sticky;
            top: 2rem;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all var(--transition-speed) ease;
        }
        .chatbot-sidebar.collapsed {
            width: 0;
            margin-left: -2rem;
            opacity: 0;
            pointer-events: none;
        }
        .chat-header {
            padding: 1.25rem 1.5rem;
            background: rgba(124, 77, 255, 0.1);
            border-bottom: 1px solid var(--border-glass);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .chat-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 1.1rem;
            color: #fff;
        }
        .chat-header-actions {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .chat-btn {
            background: none;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 1.1rem;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }
        .chat-btn:hover {
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
        }
        .chat-btn.active {
            color: var(--accent);
        }
        
        /* Key config box inside chat panel */
        .api-key-config {
            padding: 1rem 1.5rem;
            background: rgba(0, 0, 0, 0.2);
            border-bottom: 1px solid var(--border-glass);
            display: none;
        }
        .api-key-config.show {
            display: block;
        }
        .api-key-input-group {
            display: flex;
            gap: 8px;
            margin-top: 6px;
        }
        .api-key-input {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glass);
            border-radius: 8px;
            color: #fff;
            padding: 6px 10px;
            font-size: 0.85rem;
            outline: none;
        }
        .api-key-input:focus {
            border-color: var(--accent);
        }
        .api-key-btn {
            background: var(--accent);
            border: none;
            color: #fff;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.85rem;
            cursor: pointer;
            font-weight: 500;
        }
        
        /* Messages container */
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .chat-msg {
            display: flex;
            flex-direction: column;
            max-width: 85%;
        }
        .chat-msg.user {
            align-self: flex-end;
        }
        .chat-msg.model {
            align-self: flex-start;
        }
        .msg-bubble {
            padding: 10px 14px;
            border-radius: 16px;
            font-size: 0.95rem;
            line-height: 1.4;
            word-break: break-word;
        }
        .chat-msg.user .msg-bubble {
            background: var(--accent);
            color: #fff;
            border-bottom-right-radius: 4px;
        }
        .chat-msg.model .msg-bubble {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glass);
            color: var(--text-primary);
            border-bottom-left-radius: 4px;
        }
        .msg-bubble p {
            margin-bottom: 6px;
        }
        .msg-bubble p:last-child {
            margin-bottom: 0;
        }
        .msg-bubble ul, .msg-bubble ol {
            padding-left: 1.25rem;
            margin-bottom: 6px;
        }
        .msg-time {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 4px;
            align-self: flex-end;
        }
        .chat-msg.model .msg-time {
            align-self: flex-start;
        }
        
        /* Chat suggestions */
        .chat-suggestions {
            padding: 0.75rem 1.5rem;
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            border-top: 1px solid var(--border-glass);
            background: rgba(0, 0, 0, 0.1);
        }
        .suggestion-chip {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            padding: 4px 10px;
            font-size: 0.8rem;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
        }
        .suggestion-chip:hover {
            background: rgba(124, 77, 255, 0.15);
            border-color: var(--accent);
            color: #fff;
        }
        
        /* Chat Input */
        .chat-input-area {
            padding: 1rem 1.5rem;
            background: rgba(0, 0, 0, 0.2);
            border-top: 1px solid var(--border-glass);
            display: flex;
            gap: 10px;
        }
        .chat-input-box {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            color: #fff;
            padding: 10px 14px;
            font-size: 0.9rem;
            outline: none;
            resize: none;
            height: 40px;
            max-height: 100px;
            font-family: inherit;
        }
        .chat-input-box:focus {
            border-color: var(--accent);
        }
        .chat-send-btn {
            background: var(--accent);
            border: none;
            color: #fff;
            width: 40px;
            height: 40px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 1.1rem;
        }
        .chat-send-btn:hover {
            background: #9666ff;
            box-shadow: 0 0 10px var(--accent-glow);
        }
        
        /* Floating toggle button */
        .chatbot-toggle-float {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #7c4dff 0%, #00e5ff 100%);
            color: #fff;
            display: none;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: 0 5px 20px rgba(124, 77, 255, 0.4);
            transition: all 0.3s;
            z-index: 99;
        }
        .chatbot-toggle-float:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(124, 77, 255, 0.6);
        }
        
        /* Layout responsive adaptations */
        @media (max-width: 1200px) {
            .app-layout {
                flex-direction: column;
                padding: 1rem;
            }
            .chatbot-sidebar {
                width: 100%;
                height: 550px;
                position: relative;
                top: 0;
            }
            .chatbot-sidebar.collapsed {
                display: none;
            }
            .chatbot-toggle-float {
                display: flex;
            }
        }
    </style>
</head>
<body>

    <!-- Ambient Glow Blobs -->
    <div class="ambient-glow glow-1"></div>
    <div class="ambient-glow glow-2"></div>

    <!-- Sakura Falling Canvas -->
    <canvas id="sakura-canvas"></canvas>

    <!-- Loading Overlay -->
    <div id="loading-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(10,11,16,0.9); z-index:9999; justify-content:center; align-items:center; flex-direction:column; gap:1rem;">
        <div style="border: 4px solid var(--border-glass); border-top: 4px solid var(--accent); border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"></div>
        <div style="font-size:1.2rem; font-weight:500;" id="loading-text">正在重新爬取最新歌曲排行...</div>
        <div style="font-size:0.9rem; color:var(--text-secondary);" id="loading-subtext">預估需要 20-30 秒，請勿關閉網頁</div>
    </div>
    <style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>

    <div class="app-layout">
        <div class="main-content">
            <div class="container" style="padding: 0; max-width: 100%;">
                
                <!-- Header -->
                <header>
                    <div class="logo-area">
                        <i class="bi bi-music-note-list logo-icon"></i>
                    </div>
                    <h1>日語熱門歌曲排行榜</h1>
                    <p class="subtitle">MaruMaru-X Most Liked Japanese Songs Top 200</p>
                    <p class="last-update" id="update-time">資料更新時間: [DATE_PLACEHOLDER]</p>
                </header>

                <!-- Stats Grid -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon"><i class="bi bi-music-note"></i></div>
                        <div class="stat-info">
                            <div class="stat-val">200</div>
                            <div class="stat-lbl">歌曲總數</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="bi bi-heart-fill"></i></div>
                        <div class="stat-info">
                            <div class="stat-val" id="total-likes">0</div>
                            <div class="stat-lbl">點讚總數</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon plays"><i class="bi bi-play-circle-fill"></i></div>
                        <div class="stat-info">
                            <div class="stat-val" id="total-plays">0</div>
                            <div class="stat-lbl">觀看次數</div>
                        </div>
                    </div>
                </div>

        <!-- Controls Toolbar -->
        <div class="controls-panel">
            <div class="search-box">
                <i class="bi bi-search"></i>
                <input type="text" class="search-input" id="search" placeholder="搜尋歌名、歌手或標籤...">
            </div>
            <div class="filter-selects">
                <select class="custom-select" id="sort-by">
                    <option value="rank">按排名 (1-200)</option>
                    <option value="likes-desc">按愛心數量 (多到少)</option>
                    <option value="plays-desc">按播放次數 (多到少)</option>
                    <option value="date-desc">按發佈時間 (新到舊)</option>
                    <option value="duration-desc">按歌曲時長 (長到短)</option>
                </select>
                <select class="custom-select" id="filter-tag">
                    <option value="all">所有標籤</option>
                </select>
                <!-- Refresh Button -->
                <button class="custom-select" id="btn-refresh" style="background: rgba(124, 77, 255, 0.1); border-color: rgba(124, 77, 255, 0.3); color: #fff; cursor: pointer;">
                    <i class="bi bi-arrow-clockwise"></i> 重新爬取資料
                </button>
            </div>
            <div class="layout-toggle">
                <button class="layout-btn active" id="btn-grid" title="網格檢視"><i class="bi bi-grid-fill"></i></button>
                <button class="layout-btn" id="btn-table" title="列表檢視"><i class="bi bi-list-task"></i></button>
            </div>
        </div>

        <!-- Grid View Layout -->
        <div class="songs-grid" id="songs-grid">
            <!-- Dynamic cards go here -->
        </div>

        <!-- Table View Layout -->
        <div class="table-container" id="table-container">
            <table>
                <thead>
                    <tr>
                        <th style="width: 80px;">排名</th>
                        <th style="width: 100px;">封面</th>
                        <th>歌名</th>
                        <th>歌手</th>
                        <th style="width: 100px;">愛心數量</th>
                        <th style="width: 100px;">播放次數</th>
                        <th style="width: 80px;">時長</th>
                        <th style="width: 120px;">發佈日期</th>
                        <th>標籤</th>
                    </tr>
                </thead>
                <tbody id="songs-table-body">
                    <!-- Dynamic rows go here -->
                </tbody>
            </table>
        </div>

        <!-- No Results -->
        <div class="no-results" id="no-results">
            <i class="bi bi-music-note-beamed" style="font-size: 3rem; color: var(--text-muted); display: block; margin-bottom: 1rem;"></i>
            沒有找到符合條件的歌曲。
        </div>

            </div>
        </div>

        <!-- Chatbot Sidebar -->
        <div class="chatbot-sidebar" id="chatbot-sidebar">
            <div class="chat-header">
                <div class="chat-title">
                    <i class="bi bi-robot" style="color: var(--accent); font-size: 1.25rem;"></i>
                    <span>AI 歌曲小幫手</span>
                </div>
                <div class="chat-header-actions">
                    <button class="chat-btn" id="btn-toggle-key" title="設定 Gemini API Key">
                        <i class="bi bi-key-fill"></i>
                    </button>
                    <button class="chat-btn" id="btn-chat-close" title="收合聊天室">
                        <i class="bi bi-x-lg"></i>
                    </button>
                </div>
            </div>
            
            <div class="api-key-config" id="api-key-panel">
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 6px;">
                    請輸入您的 Gemini API Key：
                </div>
                <div class="api-key-input-group">
                    <input type="password" class="api-key-input" id="chat-api-key" placeholder="AIzaSy...">
                    <button class="api-key-btn" id="btn-save-key">儲存</button>
                </div>
                <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 6px; line-height: 1.2;">
                    API Key 將存儲於您本機的 localStorage 中。若不填寫，將使用後端環境變數 GEMINI_API_KEY。
                </div>
            </div>
            
            <div class="chat-messages" id="chat-history">
                <div class="chat-msg model">
                    <div class="msg-bubble">
                        哈囉！我是您的 AI 歌曲小幫手。我可以為您推薦 Top 200 的日文歌曲、分析歌手或提供歌曲類型建議。
                        <br><br>
                        請在上方設定您的 <strong>Gemini API Key</strong> 即可開始與我對談喔！
                    </div>
                    <div class="msg-time" id="welcome-msg-time">--:--</div>
                </div>
            </div>
            
            <div class="chat-suggestions">
                <div class="suggestion-chip" onclick="sendSuggestion('推薦 3 首米津玄師的歌曲')">推薦米津玄師</div>
                <div class="suggestion-chip" onclick="sendSuggestion('有哪些標籤是 #ANM (動漫) 的熱門歌？')">動漫熱門歌</div>
                <div class="suggestion-chip" onclick="sendSuggestion('幫我推薦播放次數大於 100K 且愛心多的歌曲')">高播放量推薦</div>
            </div>
            
            <div class="chat-input-area">
                <textarea class="chat-input-box" id="chat-input" placeholder="問問我關於排行榜的歌... (按 Enter 發送)"></textarea>
                <button class="chat-send-btn" id="btn-chat-send" title="發送訊息">
                    <i class="bi bi-send-fill"></i>
                </button>
            </div>
        </div>
    </div>
    
    <!-- Floating toggle button to reopen chatbot -->
    <div class="chatbot-toggle-float" id="chatbot-toggle-float" title="打開 AI 聊天室">
        <i class="bi bi-chat-dots-fill"></i>
    </div>

    <!-- Lyrics Modal -->
    <div id="lyrics-modal" class="modal-overlay">
        <div class="modal-content">
            <button class="modal-close" onclick="closeLyricsModal()"><i class="bi bi-x-lg"></i></button>
            <div class="modal-header">
                <img id="modal-cover" src="" alt="封面" class="modal-cover-img">
                <div class="modal-song-info">
                    <span id="modal-rank" class="modal-rank-badge">#1</span>
                    <h2 id="modal-title" class="modal-song-title">Song Title</h2>
                    <h3 id="modal-singer" class="modal-song-singer">Singer</h3>
                    <div class="modal-stats">
                        <span class="modal-stat-item"><i class="bi bi-heart-fill" style="color: #ff4081;"></i> <span id="modal-likes">0</span></span>
                        <span class="modal-stat-item"><i class="bi bi-play-circle-fill" style="color: #00e5ff;"></i> <span id="modal-plays">0</span></span>
                        <span class="modal-stat-item"><i class="bi bi-clock"></i> <span id="modal-duration">0:00</span></span>
                        <span class="modal-stat-item"><i class="bi bi-calendar3"></i> <span id="modal-date">未知</span></span>
                    </div>
                    <div id="modal-tags" class="modal-tags-container"></div>
                    <div>
                        <a id="modal-external-link" href="" target="_blank" class="modal-link-btn"><i class="bi bi-box-arrow-up-right"></i> 前往 MaruMaru 原網頁</a>
                    </div>
                </div>
            </div>
            <hr class="modal-divider">
            <div class="modal-body">
                <h4 class="lyrics-section-title">歌詞 Lyrics</h4>
                <div id="modal-lyrics-loading" class="lyrics-loading">
                    <div class="spinner"></div>
                    <p>正在載入歌詞...</p>
                </div>
                <div id="modal-lyrics-error" class="lyrics-error" style="display: none;">
                    <i class="bi bi-exclamation-triangle-fill"></i>
                    <p id="modal-error-message">載入歌詞失敗。</p>
                </div>
                <div id="modal-lyrics-container" class="lyrics-container">
                    <!-- Lyrics lines go here -->
                </div>
            </div>
        </div>
    </div>

    <!-- Data Injection -->
    <script>
        // Data injected from python for static preview
        const staticSongs = SONGS_JSON_PLACEHOLDER;
        let songs = [];

        // Format numbers for dashboard (e.g. 9.5K to 9500)
        function convertToNumber(valStr) {
            if (!valStr) return 0;
            valStr = String(valStr).trim().toUpperCase();
            if (!valStr || valStr === '0') return 0;
            if (valStr.includes('K')) {
                return parseFloat(valStr.replace('K', '')) * 1000;
            }
            if (valStr.includes('M')) {
                return parseFloat(valStr.replace('M', '')) * 1000000;
            }
            return parseFloat(valStr) || 0;
        }

        // Check if running from web server or local filesystem
        const isLocalFile = window.location.protocol === 'file:';
        const isLocalServer = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost';

        async function initApp() {
            const refreshBtn = document.getElementById('btn-refresh');
            if (!isLocalServer) {
                console.log("Running in static mode (GitHub Pages or local file).");
                songs = staticSongs;
                document.getElementById('update-time').textContent = "資料更新時間: [DATE_PLACEHOLDER] (靜態網頁模式)";
                if (refreshBtn) {
                    refreshBtn.title = "靜態模式下不可直接重新爬取，請在本地執行 python scraper.py 更新";
                    refreshBtn.style.opacity = "0.5";
                    refreshBtn.addEventListener('click', () => {
                        alert("當前為 GitHub Pages 靜態模式。如需更新資料，請在本地執行 python scraper.py 重新爬取並推送到 GitHub！");
                    });
                }
                calculateAndDisplayStats(songs);
                setupTagFilterDropdown();
                renderSongs();
            } else {
                console.log("Running in FastAPI dynamic mode.");
                document.getElementById('update-time').textContent = "資料更新時間: API 即時數據";
                if (refreshBtn) {
                    refreshBtn.addEventListener('click', triggerScrapeAPI);
                }
                await fetchSongsFromAPI();
                await fetchStatsFromAPI();
                setupTagFilterDropdown();
            }
            // Initialize Sakura Animation
            initSakura();
            // Initialize Chatbot
            initChat();
        }

        // Fetch all songs from API
        async function fetchSongsFromAPI() {
            try {
                const response = await fetch('/api/songs');
                if (response.ok) {
                    songs = await response.json();
                    renderSongs();
                } else {
                    console.error("Failed to fetch songs from API.");
                }
            } catch (e) {
                console.error("Error fetching songs from API:", e);
            }
        }

        // Fetch stats from API
        async function fetchStatsFromAPI() {
            try {
                const response = await fetch('/api/stats');
                if (response.ok) {
                    const stats = await response.json();
                    
                    const totalLikesVal = stats.total_likes;
                    const totalPlaysVal = stats.total_plays;
                    
                    document.getElementById('total-likes').textContent = totalLikesVal >= 1000 ? (totalLikesVal / 1000).toFixed(1) + 'K' : totalLikesVal;
                    document.getElementById('total-plays').textContent = totalPlaysVal >= 1000000 ? (totalPlaysVal / 1000000).toFixed(1) + 'M' : (totalPlaysVal >= 1000 ? (totalPlaysVal / 1000).toFixed(1) + 'K' : totalPlaysVal);
                    const topSingerEl = document.getElementById('top-singer');
                    if (topSingerEl) topSingerEl.textContent = stats.top_singer;
                }
            } catch (e) {
                console.error("Error fetching stats:", e);
            }
        }

        // Calculate and display stats locally (static mode fallback)
        function calculateAndDisplayStats(songList) {
            let totalLikesVal = 0;
            let totalPlaysVal = 0;
            const singerCounts = {};

            songList.forEach(song => {
                totalLikesVal += convertToNumber(song.愛心數量);
                totalPlaysVal += convertToNumber(song.播放次數);
                if (song.歌手) {
                    singerCounts[song.歌手] = (singerCounts[song.歌手] || 0) + 1;
                }
            });

            let topSinger = '--';
            let maxCount = 0;
            for (const [singer, count] of Object.entries(singerCounts)) {
                if (count > maxCount) {
                    maxCount = count;
                    topSinger = singer + ' (' + count + '首)';
                }
            }

            document.getElementById('total-likes').textContent = totalLikesVal >= 1000 ? (totalLikesVal / 1000).toFixed(1) + 'K' : totalLikesVal;
            document.getElementById('total-plays').textContent = totalPlaysVal >= 1000000 ? (totalPlaysVal / 1000000).toFixed(1) + 'M' : (totalPlaysVal >= 1000 ? (totalPlaysVal / 1000).toFixed(1) + 'K' : totalPlaysVal);
            const topSingerEl = document.getElementById('top-singer');
            if (topSingerEl) topSingerEl.textContent = topSinger;
        }

        // Setup dropdown
        function setupTagFilterDropdown() {
            const allTagsSet = new Set();
            songs.forEach(song => {
                if (song.標籤) {
                    song.標籤.split(',').forEach(t => {
                        const tag = t.trim();
                        if (tag) allTagsSet.add(tag);
                    });
                }
            });
            const filterTagSelect = document.getElementById('filter-tag');
            filterTagSelect.innerHTML = '<option value="all">所有標籤</option>';
            Array.from(allTagsSet).sort().forEach(tag => {
                const opt = document.createElement('option');
                opt.value = tag;
                opt.textContent = tag;
                filterTagSelect.appendChild(opt);
            });
        }

        // Trigger Scrape through FastAPI
        let checkStatusInterval = null;
        async function triggerScrapeAPI() {
            try {
                const response = await fetch('/api/scrape', { method: 'POST' });
                if (response.ok) {
                    showLoadingOverlay("正在啟動背景爬蟲程式...");
                    startCheckingScrapeStatus();
                } else {
                    const err = await response.json();
                    alert("啟動爬蟲失敗: " + (err.message || "未知原因"));
                }
            } catch (e) {
                alert("連接 API 失敗，請確認 FastAPI 伺服器正在運行。");
            }
        }

        function showLoadingOverlay(text) {
            document.getElementById('loading-overlay').style.display = 'flex';
            document.getElementById('loading-text').textContent = text;
        }

        function hideLoadingOverlay() {
            document.getElementById('loading-overlay').style.display = 'none';
        }

        function startCheckingScrapeStatus() {
            if (checkStatusInterval) clearInterval(checkStatusInterval);
            checkStatusInterval = setInterval(async () => {
                try {
                    const response = await fetch('/api/scrape/status');
                    if (response.ok) {
                        const statusData = await response.json();
                        if (statusData.status === 'running') {
                            showLoadingOverlay("正在背景重新爬取最新歌曲排行，請稍候...");
                        } else if (statusData.status === 'completed') {
                            clearInterval(checkStatusInterval);
                            showLoadingOverlay("資料更新完成！正在重新載入數據...");
                            setTimeout(async () => {
                                await fetchSongsFromAPI();
                                await fetchStatsFromAPI();
                                setupTagFilterDropdown();
                                hideLoadingOverlay();
                            }, 1000);
                        } else if (statusData.status === 'failed') {
                            clearInterval(checkStatusInterval);
                            hideLoadingOverlay();
                            alert("爬蟲執行失敗: " + (statusData.error || "未知錯誤"));
                        }
                    }
                } catch (e) {
                    console.error("Error checking scrape status:", e);
                }
            }, 2000);
        }

        // UI elements
        const searchInput = document.getElementById('search');
        const sortBySelect = document.getElementById('sort-by');
        const filterTag = document.getElementById('filter-tag');
        const btnGrid = document.getElementById('btn-grid');
        const btnTable = document.getElementById('btn-table');
        const songsGrid = document.getElementById('songs-grid');
        const tableContainer = document.getElementById('table-container');
        const songsTableBody = document.getElementById('songs-table-body');
        const noResults = document.getElementById('no-results');

        let currentLayout = 'grid';

        // Layout Toggle Actions
        btnGrid.addEventListener('click', () => {
            currentLayout = 'grid';
            btnGrid.classList.add('active');
            btnTable.classList.remove('active');
            songsGrid.style.display = 'grid';
            tableContainer.style.display = 'none';
            renderSongs();
        });

        btnTable.addEventListener('click', () => {
            currentLayout = 'table';
            btnTable.classList.add('active');
            btnGrid.classList.remove('active');
            songsGrid.style.display = 'none';
            tableContainer.style.display = 'block';
            renderSongs();
        });

        // Event listeners for sorting & filtering
        searchInput.addEventListener('input', renderSongs);
        sortBySelect.addEventListener('change', renderSongs);
        filterTag.addEventListener('change', renderSongs);

        // Core Render Function
        function renderSongs() {
            const searchQuery = searchInput.value.toLowerCase().trim();
            const sortBy = sortBySelect.value;
            const tagFilter = filterTag.value;

            // 1. Filter
            let filteredSongs = songs.filter(song => {
                const matchSearch = song.歌名.toLowerCase().includes(searchQuery) || 
                                    song.歌手.toLowerCase().includes(searchQuery) ||
                                    (song.標籤 && song.標籤.toLowerCase().includes(searchQuery));
                
                const matchTag = tagFilter === 'all' || 
                                 (song.標籤 && song.標籤.split(',').map(t => t.trim()).includes(tagFilter));

                return matchSearch && matchTag;
            });

            // 2. Sort
            filteredSongs.sort((a, b) => {
                if (sortBy === 'rank') {
                    return a.排名 - b.排名;
                } else if (sortBy === 'likes-desc') {
                    return convertToNumber(b.愛心數量) - convertToNumber(a.愛心數量);
                } else if (sortBy === 'plays-desc') {
                    return convertToNumber(b.播放次數) - convertToNumber(a.播放次數);
                } else if (sortBy === 'date-desc') {
                    return new Date(b.發佈日期 || '1970-01-01') - new Date(a.發佈日期 || '1970-01-01');
                } else if (sortBy === 'duration-desc') {
                    const getSecs = (str) => {
                        if (!str) return 0;
                        const pts = str.split(':').map(Number);
                        return pts.length === 2 ? pts[0] * 60 + pts[1] : 0;
                    };
                    return getSecs(b.時長) - getSecs(a.時長);
                }
                return 0;
            });

            // 3. Render Views
            if (filteredSongs.length === 0) {
                noResults.style.display = 'block';
                songsGrid.innerHTML = '';
                songsTableBody.innerHTML = '';
                return;
            }
            noResults.style.display = 'none';

            if (currentLayout === 'grid') {
                songsGrid.innerHTML = filteredSongs.map(song => {
                    const tagsHtml = song.標籤 ? song.標籤.split(',').map(t => `<a href="#" class="tag-badge" onclick="filterByTag('${t.trim()}'); return false;">${t.trim()}</a>`).join('') : '';
                    return `
                        <div class="song-card">
                            <div class="rank-badge">#${song.排名}</div>
                            <div class="card-img-wrap" onclick="openLyricsModal(${song.排名})" style="cursor: pointer;">
                                <img src="${song.封面 || 'https://via.placeholder.com/320x180?text=No+Thumbnail'}" alt="${song.歌名}" class="card-img" loading="lazy">
                                <div class="duration-badge">${song.時長}</div>
                            </div>
                            <div class="card-body">
                                <h3 class="song-title"><a href="#" onclick="openLyricsModal(${song.排名}); return false;">${song.歌名}</a></h3>
                                <p class="song-singer">${song.歌手}</p>
                                <div class="card-stats">
                                    <span class="card-stat-item likes"><i class="bi bi-heart-fill"></i> ${song.愛心數量}</span>
                                    <span class="card-stat-item plays"><i class="bi bi-play-circle-fill"></i> ${song.播放次數}</span>
                                    <span class="card-stat-item date"><i class="bi bi-calendar3"></i> ${song.發佈日期}</span>
                                </div>
                                <div class="card-tags">${tagsHtml}</div>
                            </div>
                        </div>
                    `;
                }).join('');
            } else {
                songsTableBody.innerHTML = filteredSongs.map(song => {
                    const tagsHtml = song.標籤 ? song.標籤.split(',').map(t => `<a href="#" class="tag-badge" onclick="filterByTag('${t.trim()}'); return false;">${t.trim()}</a>`).join(' ') : '';
                    return `
                        <tr>
                            <td class="table-rank">#${song.排名}</td>
                            <td><img src="${song.封面 || 'https://via.placeholder.com/60x34?text=No+Thumb'}" class="table-thumb" alt="封面" loading="lazy" onclick="openLyricsModal(${song.排名})" style="cursor: pointer;"></td>
                            <td class="table-title"><a href="#" onclick="openLyricsModal(${song.排名}); return false;">${song.歌名}</a></td>
                            <td>${song.歌手}</td>
                            <td style="color: #ff4081; font-weight: 500;"><i class="bi bi-heart-fill"></i> ${song.愛心數量}</td>
                            <td style="color: #00e5ff;"><i class="bi bi-play-circle-fill"></i> ${song.播放次數}</td>
                            <td>${song.時長}</td>
                            <td style="font-size: 0.85rem; color: var(--text-secondary);">${song.發佈日期}</td>
                            <td>${tagsHtml}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // Helper to trigger filtering from tags
        window.filterByTag = function(tag) {
            filterTag.value = tag;
            renderSongs();
        };

        // Modal functions
        async function openLyricsModal(rank) {
            const song = songs.find(s => s.排名 === rank);
            if (!song) return;

            const modal = document.getElementById('lyrics-modal');
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';

            document.getElementById('modal-cover').src = song.封面 || 'https://via.placeholder.com/320x180?text=No+Thumbnail';
            document.getElementById('modal-rank').textContent = `#${song.排名}`;
            document.getElementById('modal-title').textContent = song.歌名;
            document.getElementById('modal-singer').textContent = song.歌手;
            document.getElementById('modal-likes').textContent = song.愛心數量;
            document.getElementById('modal-plays').textContent = song.播放次數;
            document.getElementById('modal-duration').textContent = song.時長;
            document.getElementById('modal-date').textContent = song.發佈日期 || '未知';

            const tagsContainer = document.getElementById('modal-tags');
            tagsContainer.innerHTML = '';
            if (song.標籤) {
                song.標籤.split(',').forEach(tag => {
                    const cleanTag = tag.trim();
                    if (cleanTag) {
                        const tagEl = document.createElement('span');
                        tagEl.className = 'tag-badge';
                        tagEl.style.cursor = 'default';
                        tagEl.textContent = cleanTag;
                        tagsContainer.appendChild(tagEl);
                    }
                });
            }

            document.getElementById('modal-external-link').href = song.歌曲連結;

            const loadingEl = document.getElementById('modal-lyrics-loading');
            const errorEl = document.getElementById('modal-lyrics-error');
            const containerEl = document.getElementById('modal-lyrics-container');

            loadingEl.style.display = 'flex';
            errorEl.style.display = 'none';
            containerEl.style.display = 'none';
            containerEl.innerHTML = '';

            try {
                let lyrics = null;
                // Primary: Try fetching the static JSON file directly (essential for GitHub Pages)
                try {
                    const res = await fetch(`lyrics/${rank}.json`);
                    if (res.ok) {
                        lyrics = await res.json();
                    }
                } catch (e) {
                    console.warn("Static lyrics fetch failed, trying API/Local fallbacks.");
                }

                // Fallback 1: Try FastAPI /api/lyrics/{rank}
                if (!lyrics) {
                    try {
                        const res = await fetch(`/api/lyrics/${rank}`);
                        if (res.ok) {
                            lyrics = await res.json();
                        }
                    } catch (e) {
                        console.warn("FastAPI local endpoint not available.");
                    }
                }

                // Fallback 2: Try absolute localhost FastAPI endpoint if previewing from file://
                if (!lyrics && isLocalFile) {
                    try {
                        const res = await fetch(`http://127.0.0.1:8000/api/lyrics/${rank}`);
                        if (res.ok) {
                            lyrics = await res.json();
                        }
                    } catch (e) {
                        console.error("FastAPI localhost fallback failed:", e);
                    }
                }

                if (!lyrics || lyrics.length === 0) {
                    throw new Error(isLocalFile 
                        ? "無法載入歌詞。在靜態 file:// 預覽模式下，瀏覽器安全限制可能會阻止載入。請啟動 FastAPI 伺服器並瀏覽 http://127.0.0.1:8000 存取。" 
                        : "找不到該歌曲的歌詞資料。請確認已執行爬取歌詞程式。");
                }

                lyrics.forEach(line => {
                    const lineEl = document.createElement('div');
                    lineEl.className = 'lyric-line';

                    const jaEl = document.createElement('div');
                    jaEl.className = 'lyric-ja';
                    jaEl.innerHTML = line.ja_html;

                    const zhEl = document.createElement('div');
                    zhEl.className = 'lyric-zh';
                    zhEl.textContent = line.zh_text || '';

                    lineEl.appendChild(jaEl);
                    if (line.zh_text) {
                        lineEl.appendChild(zhEl);
                    }
                    containerEl.appendChild(lineEl);
                });

                loadingEl.style.display = 'none';
                containerEl.style.display = 'flex';

            } catch (err) {
                console.error(err);
                loadingEl.style.display = 'none';
                document.getElementById('modal-error-message').textContent = err.message;
                errorEl.style.display = 'block';
            }
        }

        function closeLyricsModal() {
            const modal = document.getElementById('lyrics-modal');
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }

        window.openLyricsModal = openLyricsModal;
        window.closeLyricsModal = closeLyricsModal;

        // Close modal when clicking outside content
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('lyrics-modal');
            if (e.target === modal) {
                closeLyricsModal();
            }
        });

        // Sakura Falling Animation logic
        function initSakura() {
            const canvas = document.getElementById('sakura-canvas');
            const ctx = canvas.getContext('2d');
            
            let w = canvas.width = window.innerWidth;
            let h = canvas.height = window.innerHeight;
            
            window.addEventListener('resize', () => {
                w = canvas.width = window.innerWidth;
                h = canvas.height = window.innerHeight;
            });
            
            const petalCount = 35;
            const petals = [];
            
            class Petal {
                constructor() {
                    this.x = Math.random() * w;
                    this.y = Math.random() * h - h;
                    this.r = Math.random() * 6 + 4; // size
                    this.d = Math.random() * petalCount; // density / rotation offset
                    this.velX = Math.random() * 2 - 0.5; // X drift speed
                    this.velY = Math.random() * 1.5 + 1; // Y fall speed
                    this.flip = Math.random();
                    this.flipSpeed = Math.random() * 0.03 + 0.01;
                }
                
                draw() {
                    if (this.y > h || this.x > w || this.x < -10) {
                        this.x = Math.random() * w;
                        this.y = -20;
                        this.velX = Math.random() * 2 - 0.5;
                        this.velY = Math.random() * 1.5 + 1;
                    }
                    
                    ctx.beginPath();
                    ctx.save();
                    ctx.translate(this.x, this.y);
                    ctx.rotate(this.d * Math.PI / 180);
                    ctx.scale(this.flip, 1);
                    
                    // Sakura pink colors
                    const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, this.r);
                    grad.addColorStop(0, '#ffb7d5');
                    grad.addColorStop(1, '#ff8da1');
                    ctx.fillStyle = grad;
                    
                    ctx.moveTo(0, 0);
                    ctx.bezierCurveTo(-this.r, -this.r, -this.r * 1.5, this.r / 2, 0, this.r * 1.5);
                    ctx.bezierCurveTo(this.r * 1.5, this.r / 2, this.r, -this.r, 0, 0);
                    
                    ctx.fill();
                    ctx.restore();
                }
                
                update() {
                    this.x += this.velX + Math.sin(this.d * 0.01) * 0.5;
                    this.y += this.velY;
                    this.d += 0.5;
                    this.flip += this.flipSpeed;
                    if (this.flip > 1 || this.flip < -1) {
                        this.flipSpeed = -this.flipSpeed;
                    }
                }
            }
            
            for (let i = 0; i < petalCount; i++) {
                petals.push(new Petal());
            }
            
            function animate() {
                ctx.clearRect(0, 0, w, h);
                petals.forEach(p => {
                    p.update();
                    p.draw();
                });
                requestAnimationFrame(animate);
            }
            
            animate();
        }

        // Chatbot Panel logic
        const sidebar = document.getElementById('chatbot-sidebar');
        const toggleKeyBtn = document.getElementById('btn-toggle-key');
        const closeChatBtn = document.getElementById('btn-chat-close');
        const floatToggleBtn = document.getElementById('chatbot-toggle-float');
        const apiKeyPanel = document.getElementById('api-key-panel');
        const apiKeyInput = document.getElementById('chat-api-key');
        const saveKeyBtn = document.getElementById('btn-save-key');
        const chatHistory = document.getElementById('chat-history');
        const chatInput = document.getElementById('chat-input');
        const chatSendBtn = document.getElementById('btn-chat-send');

        let chatHistoryData = []; // format: {role: "user"|"model", text: "..."}

        // Initialize API Key and Chat
        function initChat() {
            // Restore API key
            const savedKey = localStorage.getItem('gemini_api_key');
            if (savedKey) {
                apiKeyInput.value = savedKey;
                toggleKeyBtn.classList.add('active');
            }

            // Set welcome msg time
            const now = new Date();
            document.getElementById('welcome-msg-time').textContent = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

            // Toggle api key panel
            toggleKeyBtn.addEventListener('click', () => {
                apiKeyPanel.classList.toggle('show');
            });

            // Save api key
            saveKeyBtn.addEventListener('click', () => {
                const key = apiKeyInput.value.trim();
                if (key) {
                    localStorage.setItem('gemini_api_key', key);
                    toggleKeyBtn.classList.add('active');
                    alert('Gemini API Key 儲存成功！');
                } else {
                    localStorage.removeItem('gemini_api_key');
                    toggleKeyBtn.classList.remove('active');
                    alert('Gemini API Key 已清除。將使用後端環境變數。');
                }
                apiKeyPanel.classList.remove('show');
            });

            // Collapsing / Expanding Sidebar
            closeChatBtn.addEventListener('click', () => {
                sidebar.classList.add('collapsed');
                floatToggleBtn.style.display = 'flex';
            });

            floatToggleBtn.addEventListener('click', () => {
                sidebar.classList.remove('collapsed');
                floatToggleBtn.style.display = 'none';
            });

            // Send message events
            chatInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            chatSendBtn.addEventListener('click', sendMessage);
        }

        // Send suggestions
        window.sendSuggestion = function(text) {
            chatInput.value = text;
            sendMessage();
        };

        // Render message in chat UI
        function appendMessage(role, text) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `chat-msg ${role}`;

            const bubbleDiv = document.createElement('div');
            bubbleDiv.className = 'msg-bubble';
            
            // Basic markdown-to-html conversion for clean list display
            bubbleDiv.innerHTML = formatMarkdown(text);

            const timeDiv = document.createElement('div');
            timeDiv.className = 'msg-time';
            const now = new Date();
            timeDiv.textContent = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

            msgDiv.appendChild(bubbleDiv);
            msgDiv.appendChild(timeDiv);
            chatHistory.appendChild(msgDiv);

            // Auto scroll to bottom
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }

        // Basic helper to convert markdown lists & bold text to HTML
        function formatMarkdown(text) {
            if (!text) return '';
            let html = text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
                .replace(/`(.*?)`/g, '<code>$1</code>');
                
            // Convert list items
            const lines = html.split('\\n');
            let inList = false;
            let formattedLines = [];
            
            lines.forEach(line => {
                const trimmed = line.trim();
                if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
                    if (!inList) {
                        formattedLines.push('<ul>');
                        inList = true;
                    }
                    formattedLines.push(`<li>${trimmed.substring(2)}</li>`);
                } else if (/^\\d+\\.\\s/.test(trimmed)) {
                    if (!inList) {
                        formattedLines.push('<ol>');
                        inList = true;
                    }
                    const numMatch = trimmed.match(/^\\d+\\.\\s/)[0];
                    formattedLines.push(`<li>${trimmed.substring(numMatch.length)}</li>`);
                } else {
                    if (inList) {
                        formattedLines.push(formattedLines[formattedLines.length - 1].startsWith('<li>') ? '</ul>' : '</ol>');
                        inList = false;
                    }
                    formattedLines.push(line ? `<p>${line}</p>` : '<br>');
                }
            });
            
            if (inList) {
                formattedLines.push('</ul>');
            }
            
            return formattedLines.join('');
        }

        async function sendMessage() {
            const text = chatInput.value.trim();
            if (!text) return;

            // Display user message
            appendMessage('user', text);
            chatInput.value = '';

            // Loading bubble
            const loadingMsg = document.createElement('div');
            loadingMsg.className = 'chat-msg model';
            loadingMsg.id = 'chat-loading-bubble';
            loadingMsg.innerHTML = `
                <div class="msg-bubble">
                    <div style="display: flex; gap: 4px; align-items: center; padding: 4px 8px;">
                        <span style="animation: bounce 1.4s infinite ease-in-out; width:6px; height:6px; background:#fff; border-radius:50%"></span>
                        <span style="animation: bounce 1.4s infinite ease-in-out 0.2s; width:6px; height:6px; background:#fff; border-radius:50%"></span>
                        <span style="animation: bounce 1.4s infinite ease-in-out 0.4s; width:6px; height:6px; background:#fff; border-radius:50%"></span>
                    </div>
                </div>
            `;
            chatHistory.appendChild(loadingMsg);
            chatHistory.scrollTop = chatHistory.scrollHeight;

            // Add CSS bounce animation if not present
            if (!document.getElementById('bounce-anim-style')) {
                const style = document.createElement('style');
                style.id = 'bounce-anim-style';
                style.textContent = `
                    @keyframes bounce {
                        0%, 80%, 100% { transform: scale(0); }
                        40% { transform: scale(1.0); }
                    }
                `;
                document.head.appendChild(style);
            }

            const apiKey = localStorage.getItem('gemini_api_key') || '';
            if (!apiKey) {
                const loadingBubble = document.getElementById('chat-loading-bubble');
                if (loadingBubble) loadingBubble.remove();
                appendMessage('model', '❌ 尚未設定 API Key。請點選聊天室右上角金鑰按鈕，輸入您的 Gemini API Key 即可開始對談。');
                return;
            }

            let catalogText = "以下是本站的最受歡迎日文歌排行前 150 名的資料資料 (包含 排名, 歌名, 歌手, 愛心數量, 播放次數, 時長, 發佈日期, 標籤):\n";
            try {
                songs.slice(0, 150).forEach(song => {
                    catalogText += `#${song.排名}: ${song.歌名} - ${song.歌手} (愛心: ${song.愛心數量}, 播放: ${song.播放次數}, 時長: ${song.時長}, 日期: ${song.發佈日期 || '未知'}, 標籤: ${song.標籤 || ''})\n`;
                });
            } catch (err) {
                catalogText += "（無法載入歌曲資料庫，請以您的歌曲知識回答。）";
            }

            const systemInstruction = 
                "你是 'MaruMaru-X 日語熱門歌曲排行榜 (Top 200)' 網站的 AI 助手。\n" +
                "你擁有網站上熱門日文歌曲的完整數據庫（前150首）。請善加利用這些資訊回答使用者關於歌曲推薦、熱門歌手、播放量、發佈日期、時長、標籤篩選等問題。\n" +
                "如果使用者問及排行榜外的歌，請委婉告知你只專注於 Top 200 排行榜，但能推薦排行榜內相似風格的歌。\n" +
                "請一律使用『繁體中文』回答，語氣要親切、專業、客氣。回答內容請用 Markdown 格式進行條列與粗體標示，以便閱讀。\n" +
                catalogText + "\n";

            const contents = [];
            chatHistoryData.forEach(item => {
                contents.push({
                    role: item.role === 'user' ? 'user' : 'model',
                    parts: [{ text: item.text }]
                });
            });
            contents.push({
                role: 'user',
                parts: [{ text: text }]
            });

            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
            const reqBody = {
                contents: contents,
                systemInstruction: {
                    parts: [{ text: systemInstruction }]
                },
                generationConfig: {
                    temperature: 0.7,
                    topP: 0.95,
                    maxOutputTokens: 1024
                }
            };

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(reqBody)
                });

                const loadingBubble = document.getElementById('chat-loading-bubble');
                if (loadingBubble) loadingBubble.remove();

                if (response.ok) {
                    const data = await response.json();
                    const candidates = data.candidates || [];
                    if (candidates.length > 0 && candidates[0].content && candidates[0].content.parts && candidates[0].content.parts[0].text) {
                        const replyText = candidates[0].content.parts[0].text;
                        appendMessage('model', replyText);
                        chatHistoryData.push({ role: 'user', text: text });
                        chatHistoryData.push({ role: 'model', text: replyText });
                    } else {
                        appendMessage('model', '❌ 錯誤：Gemini API 回傳格式不符合預期。');
                    }
                } else {
                    const errData = await response.json().catch(() => ({}));
                    const errMsg = (errData.error && errData.error.message) || '無法取得 AI 回覆。';
                    appendMessage('model', `❌ API 錯誤：${errMsg}`);
                }
            } catch (e) {
                const loadingBubble = document.getElementById('chat-loading-bubble');
                if (loadingBubble) loadingBubble.remove();
                appendMessage('model', '❌ 網路連線失敗，請檢查網路。');
            }
        }

        // Initial Render
        initApp();
    </script>
</body>
</html>
"""

def parse_likes(likes_text):
    """
    將愛心數量的文字格式（例如 9.5K）轉換為數值，方便後續分析與呈現
    """
    if not likes_text:
        return 0
    likes_text = str(likes_text).strip().upper()
    try:
        if 'K' in likes_text:
            return int(float(likes_text.replace('K', '')) * 1000)
        if 'M' in likes_text:
            return int(float(likes_text.replace('M', '')) * 1000000)
        return int(likes_text)
    except Exception:
        return likes_text # 若轉換失敗則保留原始文字

def scrape_songs():
    songs_list = []
    
    # 使用 Playwright 啟動無頭瀏覽器
    with sync_playwright() as p:
        print("正在啟動瀏覽器...")
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"] # 避開自動化檢測
        )
        
        # 建立瀏覽器上下文，並設定模擬一般使用者的 User-Agent
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        
        current_page = 1
        
        while len(songs_list) < TARGET_COUNT:
            # 建立分頁網址（如第一頁或後面頁數）
            target_url = f"{BASE_URL}/{current_page}" if current_page > 1 else BASE_URL
            print(f"\n正在載入網頁: {target_url} (目前已收集 {len(songs_list)} 筆)...")
            
            try:
                # 載入網頁，只等 DOM 載入，縮短逾時設定
                page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
                
                # 等待關鍵的歌曲卡片元素渲染完成
                page.wait_for_selector("div.song-list-root", timeout=15000)
                
                # 模擬捲動頁面到底部以觸發動態資源載入
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
                
                # 取得渲染後的網頁 HTML 原始碼
                html_content = page.content()
                
                # 使用 BeautifulSoup 進行 HTML 解析
                soup = BeautifulSoup(html_content, "html.parser")
                
                # 尋找所有歌曲卡片元素
                song_cards = soup.find_all("div", class_="song-list-root")
                if not song_cards:
                    print("未找到任何歌曲卡片，可能已到達最後一頁或網頁載入失敗。")
                    break
                
                print(f"本頁偵測到 {len(song_cards)} 首歌曲。")
                
                for card in song_cards:
                    if len(songs_list) >= TARGET_COUNT:
                        break
                        
                    # 略過廣告區塊 (通常帶有 ads-root 樣式類別)
                    if "ads-root" in card.get("class", []):
                        continue
                        
                    # 1. 提取歌名 (Song Title)
                    title_element = card.find("h2", class_="card-title")
                    if not title_element:
                        continue # 若無歌名元素，代表不是真正的歌曲卡片，直接略過
                        
                    title = ""
                    song_url = ""
                    if title_element:
                        a_tag = title_element.find("a")
                        title = a_tag.get("title") if a_tag and a_tag.get("title") else title_element.get_text(strip=True)
                        if a_tag:
                            href = a_tag.get("href", "")
                            if href:
                                song_url = href if href.startswith("http") else "https://www.marumaru-x.com/" + href.lstrip("/")
                    
                    # 2. 提取歌手 (Singer)
                    singer_element = card.find("h3", class_="card-subtitle")
                    singer = singer_element.get_text(strip=True) if singer_element else "未知歌手"
                    
                    # 3. 提取封面 (Poster)
                    img_tag = card.find("img")
                    poster = ""
                    if img_tag:
                        poster = img_tag.get("src") or img_tag.get("srcset", "").split(" ")[0]
                    
                    # 4. 提取愛心數量 (Likes)
                    likes = "0"
                    heart_icon = card.find("i", class_="bi-heart")
                    if heart_icon:
                        likes = heart_icon.parent.get_text(strip=True)
                        
                    # 5. 提取播放次數 (Plays)
                    plays = "0"
                    play_icon = card.find("i", class_="bi-play-circle")
                    if play_icon:
                        plays = play_icon.parent.get_text(strip=True)
                        
                    # 6. 提取時長 (Duration)
                    duration_elem = card.find("div", class_="duration")
                    duration = duration_elem.get_text(strip=True) if duration_elem else ""
                    
                    # 7. 提取發佈日期 (Publish Date)
                    badge_elem = card.select_one("div.vu-abs-l-b span.badge")
                    date_str = badge_elem.get_text(strip=True) if badge_elem else ""
                    
                    # 8. 提取標籤 (Tags)
                    tag_elements = card.find("div", class_="singer-tag")
                    tags = []
                    if tag_elements:
                        tags = [a.get_text(strip=True) for a in tag_elements.find_all("a")]
                    
                    # 記錄排名（目前列表長度 + 1）
                    rank = len(songs_list) + 1
                    
                    songs_list.append({
                        "排名": rank,
                        "封面": poster,
                        "歌名": title,
                        "歌手": singer,
                        "愛心數量": likes,
                        "愛心數量(數值)": parse_likes(likes),
                        "播放次數": plays,
                        "時長": duration,
                        "發佈日期": date_str,
                        "標籤": ", ".join(tags),
                        "歌曲連結": song_url
                    })
                    
                    print(f" #{rank:03d} | 歌名: {title} | 歌手: {singer} | 愛心: {likes} | 播放: {plays} | 時長: {duration}")
                
                # 換頁計數器加一，準備抓取下一頁
                current_page += 1
                
                # 加入隨機延遲（1-3秒）避免請求過於頻繁
                delay = random.uniform(1.0, 3.0)
                time.sleep(delay)
                
            except Exception as e:
                print(f"載入或解析網頁時發生錯誤: {e}")
                break
                
        # 關閉瀏覽器
        browser.close()
        
    return songs_list

def save_to_csv(songs):
    """
    將爬取到的歌曲資料儲存成 CSV 檔案
    """
    if not songs:
        print("無資料可儲存！")
        return
        
    print(f"\n正在將 {len(songs)} 筆資料寫入至 {OUTPUT_CSV}...")
    try:
        # 使用 utf-8-sig 編碼以確保 Excel 開啟時日文與中文不會亂碼 (BOM)
        with open(OUTPUT_CSV, mode="w", encoding="utf-8-sig", newline="") as f:
            fieldnames = ["排名", "封面", "歌名", "歌手", "愛心數量", "愛心數量(數值)", "播放次數", "時長", "發佈日期", "標籤", "歌曲連結"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(songs)
        print("資料儲存成功！")
    except Exception as e:
        print(f"儲存 CSV 檔案時發生錯誤: {e}")

def generate_readme(songs):
    """
    生成 README.md，其中包含歌曲表格
    """
    if not songs:
        return
        
    print("\n正在生成 README.md...")
    try:
        with open("README.md", mode="w", encoding="utf-8") as f:
            f.write("# MaruMaru-X Most Liked Japanese Songs (Top 200)\n\n")
            f.write("此專案收集了 [MaruMaru 日語音樂網](https://www.marumaru-x.com/japanese-song/most-liked) 上最受歡迎的 200 首日文歌曲資訊，包含 YouTube 封面圖、播放量、愛心數、時長、發佈日期及標籤等資訊。並自動生成了此 README 文件與一個精美的互動式網頁 [index.html](index.html)。\n\n")
            
            f.write("## 專案功能\n")
            f.write("- **多功能爬蟲**：使用 Playwright 與 BeautifulSoup 動態抓取 MaruMaru-X 排行榜資料，避開自動化檢測。\n")
            f.write("- **數據導出**：自動輸出完整的 [top200_songs.csv](top200_songs.csv) 檔案，包含完整的中日文字型支援與 BOM 設定，便於後續分析與使用。\n")
            f.write("- **互動式網頁**：自動生成 [index.html](index.html) 網頁，支援即時搜尋、標籤篩選、多欄位排序（愛心數、播放次數、發佈時間、時長），並包含網格卡片與列表視圖的切換。**並內建櫻花飄落背景動效！**\n\n")
            
            f.write("## 快速開始\n\n")
            f.write("### 1. 安裝環境需求\n")
            f.write("```bash\npip install -r requirements.txt\npython -m playwright install chromium\n```\n\n")
            
            f.write("### 2. 啟動 FastAPI 服務與動態展示網頁\n")
            f.write("此專案現已支援 FastAPI 後端伺服器！執行以下指令啟動：\n")
            f.write("```bash\npython -m uvicorn main:app --reload\n```\n")
            f.write("啟動後，請瀏覽 [http://127.0.0.1:8000](http://127.0.0.1:8000) 即可查看完全動態、即時更新的互動式儀表板。並可以直接在網頁上點選 **「重新爬取資料」** 按鈕，這將會在後端觸發非同步的背景爬蟲工作，更新 CSV 及網頁數據！\n\n")
            
            f.write("### 3. 獨立執行爬蟲程式\n")
            f.write("如果您只想靜態抓取並更新資料：\n")
            f.write("```bash\npython scraper.py\n```\n\n")
            
            f.write("## 排行榜數據表 (Top 200)\n\n")
            # 寫入 markdown 表頭
            f.write("| 排名 | 封面 | 歌名 | 歌手 | 愛心數量 | 播放次數 | 時長 | 發佈日期 | 標籤 |\n")
            f.write("| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |\n")
            
            for song in songs:
                # 封面使用 small img
                poster_html = f'<img src="{song["封面"]}" width="80" alt="封面">' if song.get("封面") else "無封面"
                # 歌名使用 Markdown 超連結
                title_link = f'[{song["歌名"]}]({song["歌曲連結"]})' if song.get("歌曲連結") else song["歌名"]
                
                f.write(f'| {song["排名"]} | {poster_html} | {title_link} | {song["歌手"]} | {song["愛心數量"]} | {song["播放次數"]} | {song["時長"]} | {song["發佈日期"]} | {song["標籤"]} |\n')
            
        print("README.md 生成成功！")
    except Exception as e:
        print(f"生成 README.md 時發生錯誤: {e}")

def generate_html(songs):
    """
    將歌曲資料注入 HTML 範本中，生成 index.html
    """
    if not songs:
        return
        
    print("\n正在生成 index.html...")
    try:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 轉換為 JSON 格式
        songs_json = json.dumps(songs, ensure_ascii=False)
        
        # 替換範本中的預留位置
        rendered_html = HTML_TEMPLATE.replace("const staticSongs = SONGS_JSON_PLACEHOLDER;", f"const staticSongs = {songs_json};")
        rendered_html = rendered_html.replace("[DATE_PLACEHOLDER]", now_str)
        
        # 寫入 index.html (同時寫入 index.html 和 index.htm)
        for filename in ["index.html", "index.htm"]:
            with open(filename, mode="w", encoding="utf-8") as f:
                f.write(rendered_html)
            print(f"{filename} 生成成功！")
            
    except Exception as e:
        print(f"生成 HTML 檔案時發生錯誤: {e}")

if __name__ == "__main__":
    start_time = time.time()
    
    # 執行爬蟲主程式
    songs_data = scrape_songs()
    
    # 儲存結果到 CSV
    save_to_csv(songs_data)
    
    # 爬取歌詞資料
    try:
        from scrape_lyrics import scrape_all_lyrics
        scrape_all_lyrics(force=False, max_workers=6)
    except Exception as e:
        print(f"爬取歌詞時發生錯誤: {e}")
    
    # 生成 README.md
    generate_readme(songs_data)
    
    # 生成 index.html 和 index.htm
    generate_html(songs_data)
    
    end_time = time.time()
    print(f"\n爬蟲任務完成！共收集 {len(songs_data)} 筆資料，耗時 {end_time - start_time:.2f} 秒。")
