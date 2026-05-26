import streamlit as st

# 1. 關鍵概念：設定網頁為寬版模式，把兩邊留白填滿
st.set_page_config(layout="wide")

# 2. 標題與目的說明
st.title("🧱 簡單規劃版面（認識 Columns 空間切分）")
st.write("目的：完全不連線雲端，只專注在「如何在網頁上橫向切出三個大直欄」")

st.markdown("---")

# 3. 核心武器與關鍵概念說明（使用 Streamlit 的欄位來並排呈現）
intro_col1, intro_col2 = st.columns([1, 1])

with intro_col1:
    st.subheader("核心武器")
    st.code("st.columns(3)", language="python")
    st.write("像切豆腐一樣，在瀏覽器切出三塊獨立畫布空間")

with intro_col2:
    st.subheader("關鍵概念")
    st.markdown("- `layout=\"wide\"` 把網頁兩邊留白填滿，最適合多欄位看板")
    st.markdown("- 用 `with` 語法像填空一樣把文字塞進對應直欄")
    st.markdown("- 三欄分別對應 🔴 To Do、🟡 In Progress、🟢 Done")

st.markdown("---")

# 4. 核心實作：切出三欄畫布
col1, col2, col3 = st.columns(3)

# 用 with 語法將內容塞進對應的直欄
with col1:
    st.markdown("### 🔴 To Do")
    st.write("待辦事項")

with col2:
    st.markdown("### 🟡 In Progress")
    st.write("執行中")

with col3:
    st.markdown("### 🟢 Done")
    st.write("已完成")
