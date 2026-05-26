import pandas as pd
import streamlit as st

# 設定網頁標題與佈局
st.set_page_config(page_title="網拍進貨與蝦皮利潤定價器", layout="wide")
st.title("🛍️ 網拍進貨商品與蝦皮 10% 利潤定價系統")

# --- 側邊欄：設定目前匯率、手續費、目標利潤與新增商品 ---
st.sidebar.header("📊 匯率與定價參數設定")

# 1. 匯率設定
exchange_rate = st.sidebar.number_input(
    "今日人民幣匯率 (RMB ➡️ TWD)", min_value=1.0, max_value=10.0, value=4.5, step=0.01
)

# 2. 蝦皮手續費率設定
shopee_fee_rate = (
    st.sidebar.number_input(
        "蝦皮綜合手續費率 (%)", min_value=0.0, max_value=30.0, value=9.5, step=0.5
    )
    / 100
)

# 3. 新增：目標利潤率設定（預設為你想要的 20%）
target_profit_rate = (
    st.sidebar.number_input(
        "🎯 期望目標利潤率 (%)", min_value=0.0, max_value=80.0, value=20.0, step=1.0
    )
    / 100
)

st.sidebar.markdown("---")
st.sidebar.subheader("➕ 新增商品品項")

# 使用 session_state 儲存商品清單
if "product_list" not in st.session_state:
    st.session_state.product_list = [
        {
            "品項名稱": "韓版寬鬆純棉T恤",
            "商品網址": "https://detail.tmall.com/item.htm?id=12345",
            "人民幣進價": 35.0,
            "進貨數量": 10,
        },
        {
            "品項名稱": "復古皮革雙肩包",
            "商品網址": "https://item.taobao.com/item.htm?id=67890",
            "人民幣進價": 88.0,
            "進貨數量": 5,
        },
    ]

# 新增商品的輸入欄位（這次不需要手動猜賣價了，系統會自動幫你算）
with st.sidebar.form(key="add_product_form", clear_on_submit=True):
    new_name = st.text_input("商品品項名稱", placeholder="例如：日系復古襯衫")
    new_url = st.text_input("商品網址", placeholder="請貼上淘寶/批發網址")
    new_rmb = st.number_input("人民幣進價 (￥)", min_value=0.0, step=0.1)
    new_qty = st.number_input("進貨數量", min_value=1, step=1, value=1)

    submit_button = st.form_submit_button("新增到清單")

    if submit_button:
        if new_name and new_url:
            st.session_state.product_list.append(
                {
                    "品項名稱": new_name,
                    "商品網址": new_url,
                    "人民幣進價": new_rmb,
                    "進貨數量": new_qty,
                }
            )
            st.toast(f"✅ 已成功新增：{new_name}")
        else:
            st.error("❌ 請填寫商品名稱與網址！")


# --- 主畫面：資料處理與表格顯示 ---
if st.session_state.product_list:
    df = pd.DataFrame(st.session_state.product_list)

    # 核心計算邏輯
    df["台幣進價"] = df["人民幣進價"] * exchange_rate
    df["台幣進貨總額"] = df["台幣進價"] * df["進貨數量"]

    # 關鍵：自動倒推計算「滿足目標利潤的蝦皮建議售價」
    # 公式：台幣成本 / (1 - 手續費率 - 利潤率)
    denominator = 1 - shopee_fee_rate - target_profit_rate
    if denominator > 0:
        df["建議蝦皮賣價"] = df["台幣進價"] / denominator
    else:
        df["建議蝦皮賣價"] = 0.0

    # 依據建議賣價計算手續費與淨利，驗證數字
    df["蝦皮手續費(估)"] = df["建議蝦皮賣價"] * shopee_fee_rate
    df["估計單件進帳"] = df["建議蝦皮賣價"] - df["蝦皮手續費(估)"]
    df["單件預估淨利"] = df["估計單件進帳"] - df["台幣進價"]
    df["預估利潤總額"] = df["單件預估淨利"] * df["進貨數量"]

    # 顯示上方的總統計數據看板
    total_twd_cost = df["台幣進貨總額"].sum()
    total_profit = df["預估利潤總額"].sum()
