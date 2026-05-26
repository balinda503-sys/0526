import streamlit as st

# 1. 網頁初始化設定（必須放在程式碼第一行）
# layout="wide" 會把網頁兩邊的留白填滿，變成寬螢幕，最適合看多欄位的看板
st.set_page_config(layout="wide")

st.title("階段一：Trello 畫布空間規劃測試")
st.caption("授權標註：edit by 闕河正 | 專屬資淺初學者講義")

st.write("---")

# 2. 呼叫 st.columns(3)，在網頁橫向切出三個一模一樣寬度的大直欄變數
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

st.set_page_config(layout="wide") 

st.title(" 階段三：外星文濾網分流與空間歸隊測試") 

st.caption("授權標註：edit by 闕河正")

conn = st.connection("gsheets", type="gsheets")

df = conn.read(worksheet="Tasks", ttl="0")

st.write("---")

col1, col2, col3 = st.columns(3)

with col1: 

    st.markdown("###  To Do") 

    #  內層做濾網，外層做篩選：只抓出狀態為 To Do 的小表格 

    todo_df = df[df["status"] == "To Do"] # 把它印在左邊這欄 st.dataframe(todo_df)

with col2: 

    st.markdown("###  In Progress") 

    #  只抓出狀態為 In Progress 的小表格 

    ip_df = df[df["status"] == "In Progress"] 

    st.dataframe(ip_df)

with col3: 

    st.markdown("###  Done") 

    #  只抓出狀態為 Done 的小表格 

    done_df = df[df["status"] == "Done"] 

    st.dataframe(done_df)
