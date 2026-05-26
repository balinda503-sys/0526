import pandas as pd
import streamlit as st

# 設定網頁標題與佈局
st.set_page_config(page_title="網拍進貨與蝦皮利潤計算器", layout="wide")
st.title("🛍️ 網拍進貨商品與蝦皮利潤換算系統")

# --- 側邊欄：設定目前匯率、手續費與新增商品 ---
st.sidebar.header("📊 匯率與平台參數設定")

# 1. 匯率設定
exchange_rate = st.sidebar.number_input(
    "今日人民幣匯率 (RMB ➡️ TWD)", min_value=1.0, max_value=10.0, value=4.5, step=0.01
)

# 2. 蝦皮手續費率設定 (可依實際狀況調整，例如 7.5%, 9.5%, 11.5% 等)
shopee_fee_rate = (
    st.sidebar.number_input(
        "蝦皮綜合手續費率 (%)", min_value=0.0, max_value=30.0, value=9.5, step=0.5
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
            "預估蝦皮賣價": 299.0,
        },
        {
            "品項名稱": "復古皮革雙肩包",
            "商品網址": "https://item.taobao.com/item.htm?id=67890",
            "人民幣進價": 88.0,
            "進貨數量": 5,
            "預估蝦皮賣價": 680.0,
        },
    ]

# 新增商品的輸入欄位
with st.sidebar.form(key="add_product_form", clear_on_submit=True):
    new_name = st.text_input("商品品項名稱", placeholder="例如：日系復古襯衫")
    new_url = st.text_input("商品網址", placeholder="請貼上淘寶/批發網址")
    new_rmb = st.number_input("人民幣進價 (￥)", min_value=0.0, step=0.1)
    new_qty = st.number_input("進貨數量", min_value=1, step=1, value=1)
    new_price = st.number_input("預估蝦皮台幣賣價 ($)", min_value=0.0, step=10.0)

    submit_button = st.form_submit_button("新增到清單")

    if submit_button:
        if new_name and new_url:
            st.session_state.product_list.append(
                {
                    "品項名稱": new_name,
                    "商品網址": new_url,
                    "人民幣進價": new_rmb,
                    "進貨數量": new_qty,
                    "預估蝦皮賣價": new_price,
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

    # 蝦皮相關計算
    df["蝦皮手續費"] = df["預估蝦皮賣價"] * shopee_fee_rate
    df["單件估計進帳"] = df["預估蝦皮賣價"] - df["蝦皮手續費"]
    df["單件預估淨利"] = df["單件估計進帳"] - df["台幣進價"]
    df["預估利潤總額"] = df["單件預估淨利"] * df["進貨數量"]

    # 顯示上方的總統計數據看板
    total_twd_cost = df["台幣進貨總額"].sum()
    total_profit = df["預估利潤總額"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="📊 本批進貨商品總數", value=f"{df['進貨數量'].sum()} 件")
    col2.metric(label="🇹🇼 總折合台幣成本", value=f"NT$ {total_twd_cost:,.0f}")
    col3.metric(
        label="💰 本批完售預估總利潤",
        value=f"NT$ {total_profit:,.0f}",
        delta=f"利潤率 {(total_profit/df['預估蝦皮賣價'].sum()*100/df['進貨數量'].sum()):.1f}%"
        if total_twd_cost > 0
        else "0%",
    )

    st.markdown("---")
    st.subheader("📋 進貨明細與蝦皮利潤估算 (可在表格內雙擊直接修改)")

    # 使用 st.data_editor 呈現完整表格
    edited_df = st.data_editor(
        df,
        column_config={
            "商品網址": st.column_config.LinkColumn(
                "商品網址", display_text="🔗 點我開啟連結"
            ),
            "人民幣進價": st.column_config.NumberColumn("人民幣進價", format="￥%.2f"),
            "進貨數量": st.column_config.NumberColumn("進貨數量", min_value=1),
            "台幣進價": st.column_config.NumberColumn(
                "台幣進價成本", format="NT$ %.1f"
            ),
            "預估蝦皮賣價": st.column_config.NumberColumn(
                "預估蝦皮賣價", min_value=0.0, format="NT$ %.0f"
            ),
            "蝦皮手續費": st.column_config.NumberColumn("蝦皮手續費", format="NT$ %.1f"),
            "單件估計進帳": st.column_config.NumberColumn(
                "單件進帳(扣費後)", format="NT$ %.1f"
            ),
            "單件預估淨利": st.column_config.NumberColumn("單件淨利", format="NT$ %.1f"),
            "預估利潤總額": st.column_config.NumberColumn("預估利潤總額", format="NT$ %.0f"),
        },
        disabled=[
            "台幣進價",
            "台幣進貨總額",
            "蝦皮手續費",
            "單件估計進帳",
            "單件預估淨利",
            "預估利潤總額",
        ],  # 鎖定自動計算欄位
        use_container_width=True,
    )

    # 將修改後的資料寫回 session_state
    cleaned_df = edited_df[["品項名稱", "商品網址", "人民幣進價", "進貨數量", "預估蝦皮賣價"]]
    st.session_state.product_list = cleaned_df.to_dict(orient="records")

    # 額外功能：清空所有資料
    if st.button("🗑️ 清空所有進貨資料"):
        st.session_state.product_list = []
        st.rerun()

else:
    st.info("💡 目前暫無進貨商品，請使用左側側邊欄（Sidebar）新增第一筆商品！")
