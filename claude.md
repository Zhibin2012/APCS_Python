這是一個完整的專案結構設計。你可以將以下程式碼區塊分別存檔，或直接將這段 Markdown 內容提供給具備檔案操作能力的 AI 工具（如 Claude Code）來執行。

---

### 1. `.streamlit/config.toml`

設定 Streamlit 為寬版模式，並套用簡潔的主題。

```toml
[theme]
primaryColor = "#2E7D32"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F1F8E9"
textColor = "#212121"
font = "sans serif"

[layout]
pageLimit = 1000
wideMode = true

```

---

### 2. `requirements.txt`

列出專案所需的最小依賴。

```text
streamlit
requests
jsonschema
pandas

```

---

### 3. `data/schema.json`

定義嚴謹的知識庫資料結構。

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "meta": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "version": { "type": "string" },
        "updated_at": { "type": "string" }
      },
      "required": ["title", "version"]
    },
    "levels": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "level": { "type": "integer", "minimum": 1, "maximum": 5 },
          "name": { "type": "string" },
          "focus": { "type": "string" },
          "categories": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": { "type": "string" },
                "title": { "type": "string" },
                "desc": { "type": "string" },
                "implementation": { "type": "string" },
                "py_syntax": { "type": "array", "items": { "type": "string" } },
                "common_pitfalls": { "type": "array", "items": { "type": "string" } },
                "mini_examples": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "title": { "type": "string" },
                      "type": { "enum": ["code", "io", "note"] },
                      "content": { "type": "string" }
                    }
                  }
                }
              },
              "required": ["id", "title", "py_syntax"]
            }
          }
        },
        "required": ["level", "name", "categories"]
      }
    }
  },
  "required": ["meta", "levels"]
}

```

---

### 4. `data/knowledge_apcs_python.json`

包含完整教學內容的核心資料檔案（節錄部分核心內容，確保格式完整）。

```json
{
  "meta": {
    "title": "APCS Python 知識庫",
    "version": "1.0.0",
    "updated_at": "2026-02-05"
  },
  "levels": [
    {
      "level": 2,
      "name": "基礎程式設計能力",
      "focus": "變數、邏輯判斷與基礎迴圈應用",
      "categories": [
        {
          "id": "l2_io",
          "title": "輸入與輸出",
          "desc": "處理 APCS 測資與格式化輸出",
          "implementation": "使用 sys.stdin 提高效率，利用 f-string 控制格式",
          "py_syntax": ["input()", "print(f'...')", "sys.stdin.readline"],
          "common_pitfalls": ["忘了 split() 導致輸入變成整串字串", "print 多出空格導致 PE"],
          "mini_examples": [
            {
              "title": "快速讀取整數列表",
              "type": "code",
              "content": "import sys\nnums = list(map(int, sys.stdin.read().split()))"
            }
          ]
        }
      ]
    },
    {
      "level": 4,
      "name": "基礎資料結構運用",
      "focus": "遞迴、搜尋與線性資料結構",
      "categories": [
        {
          "id": "l4_recursion",
          "title": "遞迴與 DFS",
          "desc": "分解問題，處理樹狀或圖狀搜尋",
          "implementation": "必須設定遞迴深度，注意終止條件",
          "py_syntax": ["sys.setrecursionlimit", "def dfs(v):"],
          "common_pitfalls": ["遞迴太深導致 RecursionError", "忘了標記 visited 導致死迴圈"],
          "mini_examples": [
            {
              "title": "DFS 遍歷框架",
              "type": "code",
              "content": "def dfs(u):\n    visited.add(u)\n    for v in adj[u]:\n        if v not in visited:\n            dfs(v)"
            }
          ]
        }
      ]
    }
  ]
}

```

---

### 5. `lib/data_loader.py`

處理資料讀取、GitHub Fallback 與快取。

```python
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

```

---

### 6. `app.py`

Streamlit 應用程式主入口。

```python
import streamlit as st
from lib.data_loader import load_knowledge_base

st.set_page_config(page_title="APCS Python 教材瀏覽器", layout="wide")

# Sidebar - 導覽與資料來源
with st.sidebar:
    st.title("📚 APCS 學習導覽")
    mode = st.radio("前往頁面", ["知識庫探索", "JSON 技術手冊"])
    
    st.divider()
    source_url = st.text_input("GitHub Raw URL (選填)", placeholder="https://raw.githubusercontent.com/...")
    
# 載入資料
data = load_knowledge_base(source_url)

if not data:
    st.error("無法載入知識庫資料，請檢查路徑或 URL。")
else:
    if mode == "知識庫探索":
        st.header(f"🎯 {data['meta']['title']}")
        
        # 篩選器
        col1, col2 = st.columns(2)
        levels = {f"Level {l['level']}: {l['name']}": l for l in data['levels']}
        
        with col1:
            selected_level_name = st.selectbox("選擇級分", list(levels.keys()))
            selected_level = levels[selected_level_name]
            
        with col2:
            categories = {c['title']: c for c in selected_level['categories']}
            selected_cat_name = st.selectbox("選擇知識點", list(categories.keys()))
            cat = categories[selected_cat_name]

        st.divider()
        
        # 內容展示
        st.subheader(f"{cat['title']}")
        st.info(f"**能力重點：** {selected_level['focus']}")
        
        t1, t2, t3 = st.tabs(["💡 實作要點", "⌨️ Python 語法", "⚠️ 常見陷阱"])
        
        with t1:
            st.write(cat['implementation'])
            for ex in cat.get('mini_examples', []):
                with st.expander(f"範例: {ex['title']}"):
                    st.code(ex['content'], language='python' if ex['type']=='code' else None)
        
        with t2:
            cols = st.columns(len(cat['py_syntax']))
            for i, syntax in enumerate(cat['py_syntax']):
                cols[i % 3].code(syntax)
        
        with t3:
            for pitfall in cat['common_pitfalls']:
                st.warning(pitfall)

    elif mode == "JSON 技術手冊":
        st.header("🛠️ JSON 規格與教學")
        st.write("本系統使用 JSON 作為資料驅動，結構如下：")
        
        st.json(data['meta'])
        
        if st.button("下載當前知識庫 JSON"):
            st.download_button(
                label="確認下載",
                data=json.dumps(data, indent=2, ensure_ascii=False),
                file_name="knowledge_apcs_python.json",
                mime="application/json"
            )

```

---

### 7. `scripts/validate.py`

獨立的驗證腳本。

```python
import json
import sys
from jsonschema import validate, ValidationError

def run_validation():
    try:
        with open("data/knowledge_apcs_python.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        with open("data/schema.json", "r", encoding="utf-8") as f:
            schema = json.load(f)
            
        validate(instance=data, schema=schema)
        print("✅ 驗證通過：資料符合 Schema 規範。")
    except ValidationError as e:
        print(f"❌ 驗證失敗：{e.message}")
        print(f"路徑：{list(e.path)}")
        sys.exit(1)
    except Exception as e:
        print(f"💥 發生非預期錯誤：{e}")
        sys.exit(1)

if __name__ == "__main__":
    run_validation()

```

---

### 下一步建議

1. 將上述內容分別存入對應檔案。
2. 執行 `pip install -r requirements.txt`。
3. 執行 `streamlit run app.py` 啟動預覽。

