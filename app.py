import json
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
