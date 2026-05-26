import pandas as pd
import streamlit as st

# 設定網頁標題與佈局
st.set_page_config(page_title="網拍進貨計算器", layout="wide")
st.title("🛍️ 網拍進貨商品與匯率換算系統")

# --- 側邊欄：設定目前匯率與新增商品 ---
st.sidebar.header("📊 匯率與進貨設定")

# 1. 讓使用者自訂人民幣對台幣的匯率（例如：4.5）
exchange_rate = st.sidebar.number_input(
    "今日人民幣匯率 (RMB ➡️ TWD)", min_value=1.0, max_value=10.0, value=4.5, step=0.01
)

st.sidebar.markdown("---")
st.sidebar.subheader("➕ 新增商品品項")

# 使用 session_state 來儲存商品清單，確保重整時資料不會消失
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

# 新增商品的輸入欄位
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
    # 轉成 DataFrame 方便處理
    df = pd.DataFrame(st.session_state.product_list)

    # 核心計算邏輯：自動算出台幣進價、人民幣總額、台幣總額
    df["台幣進價"] = df["人民幣進價"] * exchange_rate
    df["人民幣總額"] = df["人民幣進價"] * df["進貨數量"]
    df["台幣總額"] = df["台幣進價"] * df["進貨數量"]

    # 顯示上方的總統計數據看板
    total_rmb = df["人民幣總額"].sum()
    total_twd = df["台幣總額"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="📊 本批進貨商品總數", value=f"{df['進貨數量'].sum()} 件")
    col2.metric(label="💰 總人民幣成本", value=f"￥{total_rmb:,.2f}")
    col3.metric(label="🇹🇼 總折合台幣成本", value=f"NT$ {total_twd:,.0f}")

    st.markdown("---")
    st.subheader("📋 進貨明細表格 (可在表格內直接修改數量或價格)")

    # 使用 st.data_editor 讓使用者能直接在網頁畫面上修改表格內容
    edited_df = st.data_editor(
        df,
        column_config={
            "商品網址": st.column_config.LinkColumn(
                "商品網址", display_text="🔗 點我開啟連結"
            ),
            "人民幣進價": st.column_config.NumberColumn("人民幣進價", format="￥%.2f"),
            "台幣進價": st.column_config.NumberColumn("台幣進價 (自動)", format="NT$ %.2f"),
            "人民幣總額": st.column_config.NumberColumn(
                "人民幣總額", format="￥%.2f"
            ),
            "台幣總額": st.column_config.NumberColumn("台幣總額", format="NT$ %.0f"),
            "進貨數量": st.column_config.NumberColumn("進貨數量", min_value=1),
        },
        disabled=["台幣進價", "人民幣總額", "台幣總額"],  # 鎖定自動計算的欄位，不讓使用者手動改
        use_container_width=True,
    )

    # 處理使用者直接在表格修改後的連動更新
    # 排除自動計算欄位後寫回 session_state
    cleaned_df = edited_df[["品項名稱", "商品網址", "人民幣進價", "進貨數量"]]
    st.session_state.product_list = cleaned_df.to_dict(orient="records")

    # 額外功能：清空所有資料
    if st.button("🗑️ 清空所有進貨資料"):
        st.session_state.product_list = []
        st.rerun()

else:
    st.info("💡 目前暫無進貨商品，請使用左側側邊欄（Sidebar）新增第一筆商品！")
