import streamlit as st
import requests
import json
import os

LOCAL_DATA_PATH = "data/knowledge_apcs_python.json"

@st.cache_data
def load_knowledge_base(url=None):
    # 嘗試從網路抓取
    if url:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.warning(f"無法從 URL 載入資料，切換至本機備份。錯誤: {e}")

    # 讀取本機檔案
    if os.path.exists(LOCAL_DATA_PATH):
        with open(LOCAL_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    return None
