import streamlit as st

# 設定寬版模式
st.set_page_config(layout="wide", page_title="Trello 看板", page_icon="📋")

st.title("🧱 階段四終極完成版：GitHub 雲端同步 Trello 看板")
st.caption("授權標註：edit by 闕河正 | 完整功能版 (美化優化版)")

# ==========================================
# 上半部：指派新任務 表單區
# ==========================================
st.subheader("➕ 指派新任務")

# 使用 st.form 讓輸入框維持在同一橫列，並顯得有區塊感
with st.form("task_form", clear_on_submit=True):
    form_col1, form_col2, form_col3 = st.columns([2, 1, 1])
    with form_col1:
        task_name = st.text_input("任務名稱", placeholder="輸入任務名稱...")
    with form_col2:
        task_status = st.selectbox("狀態", ["To Do", "In Progress", "Done"])
    with form_col3:
        task_owner = st.text_input("負責人", placeholder="誰來負責...")
        
    submit_btn = st.form_submit_button("確認指派並同步雲端")
    if submit_btn:
        # 這裡放你原本寫的雲端同步、寫入資料庫/試算表的邏輯
        st.success(f"成功指派任務：{task_name}")

st.markdown("---")

# ==========================================
# 下半部：看板動態狀態監控 (美化重點！)
# ==========================================
st.subheader("📊 看板動態狀態監控")

# 模擬從雲端抓下來的資料 (請維持你原本的資料讀取邏輯，這裡僅作美化呈現示範)
mock_tasks = [
    {"name": "網拍上架", "status": "To Do", "owner": "lili"},
    {"name": "淘寶下單", "status": "In Progress", "owner": "chen"}
]

# 切出三個大直欄
col1, col2, col3 = st.columns(3)

# 🟢 1. To Do 欄位
with col1:
    # 運用 HTML 語法讓標題自帶顏色背景，更有 Trello 的感覺
    st.markdown('<div style="background-color:#ffe6e6; padding:10px; border-radius:5px;"><h3 style="color:#d9534f; margin:0;">🔴 To Do (待辦)</h3></div>', unsafe_allow_html=True)
    st.write("") # 留下一點間隔
    
    # 篩選屬於 To Do 的任務
    todo_tasks = [t for t in mock_tasks if t["status"] == "To Do"]
    if todo_tasks:
        for task in todo_tasks:
            # 💡 重點：使用 border=True 做出獨立的任務小卡片
            with st.container(border=True):
                st.markdown(f"### **{task['name']}**")  # 修正原本顯示成 ** 的問題
                st.caption(f"👤 負責人: {task['owner']}")
    else:
        st.info("暫無待辦任務")

# 🟡 2. In Progress 欄位
with col2:
    st.markdown('<div style="background-color:#fff9e6; padding:10px; border-radius:5px;"><h3 style="color:#f0ad4e; margin:0;">🟡 In Progress (執行中)</h3></div>', unsafe_allow_html=True)
    st.write("")
    
    progress_tasks = [t for t in mock_tasks if t["status"] == "In Progress"]
    if progress_tasks:
        for task in progress_tasks:
            with st.container(border=True):
                st.markdown(f"### **{task['name']}**")
                st.caption(f"👤 負責人: {task['owner']}")
    else:
        st.info("暫無執行中任務")

# 🟢 3. Done 欄位
with col3:
    st.markdown('<div style="background-color:#e6f9ec; padding:10px; border-radius:5px;"><h3 style="color:#5cb85c; margin:0;">🟢 Done (已完成)</h3></div>', unsafe_allow_html=True)
    st.write("")
    
    done_tasks = [t for t in mock_tasks if t["status"] == "Done"]
    if done_tasks:
        for task in done_tasks:
            with st.container(border=True):
                # 已完成的任務可以加上刪除線 <s> 或改為灰色
                st.markdown(f"### ~~{task['name']}~~")
                st.caption(f"👤 負責人: {task['owner']}")
    else:
        # 當沒有任務時，可以用內建的 info 藍色區塊提示，視覺很柔和
        st.info("暫無已完成任務")
