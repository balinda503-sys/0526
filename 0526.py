import streamlit as st

# 1. 設定網頁為寬版模式
st.set_page_config(layout="wide")

# 2. 標題與目的說明
st.title("🧱 簡單規劃版面（認識 Columns 空間切分）")
st.write("目的：完全不連線雲端，只專注在「如何在網頁上橫向切出三個大直欄」")

st.markdown("---")

# 3. 核心武器與關鍵概念說明
intro_col1, intro_col2 = st.columns([1, 1])

with intro_col1:
    st.subheader("核心武器")
    # 這裡配合題目，把程式碼文字也同步改成 st.columns(4) 方便對照
    st.code("st.columns(4)", language="python") 
    st.write("像切豆腐一樣，在瀏覽器切出四塊獨立畫布空間")

with intro_col2:
    st.subheader("關鍵概念")
    st.markdown("- `layout=\"wide\"` 把網頁兩邊留白填滿，最適合多欄位看板")
    st.markdown("- 用 `with` 語法像填空一樣把文字塞進對應直欄")
    st.markdown("- 欄位擴充：只要增加變數，瀏覽器就會自動重新分配每一欄的寬度！")

st.markdown("---")

# 4. 【核心修改處】將 3 改成 4，並多宣告一個 col4 變數
col1, col2, col3, col4 = st.columns(4)

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

# 5. 【新增處】在最底下加上 with col4: 區塊
with col4:
    st.markdown("### 🔵 Backlog")
    st.write("後備任務")
