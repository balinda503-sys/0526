import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="網拍進價與建議售價",
    layout="wide"
)

st.title("網拍進價與建議售價（多商品版）")

# =========================
# 參數設定
# =========================
exchange_rate = st.sidebar.number_input(
    "人民幣匯率",
    value=9.0,
    step=0.1
)

shopee_fee = st.sidebar.number_input(
    "蝦皮手續費 (%)",
    value=20.0,
    step=1.0
) / 100

profit_rate = st.sidebar.number_input(
    "預計利潤 (%)",
    value=15.0,
    step=1.0
) / 100

# =========================
# 初始化資料
# =========================
if "products" not in st.session_state:
    st.session_state.products = pd.DataFrame({
        "商品名稱": [""],
        "商品網址": [""],
        "人民幣進價": [0.0],
        "進貨數量": [1]
    })

st.subheader("商品資料表")

# =========================
# 可編輯表格
# =========================
edited_df = st.data_editor(
    st.session_state.products,
    num_rows="dynamic",
    use_container_width=True
)

# =========================
# 計算欄位
# =========================
result_df = edited_df.copy()

# 人民幣轉台幣
result_df["台幣成本"] = (
    result_df["人民幣進價"] * exchange_rate
)

# 建議售價
result_df["建議售價"] = (
    result_df["台幣成本"] *
    (1 + shopee_fee + profit_rate)
).round(0)

# 總成本
result_df["總成本"] = (
    result_df["台幣成本"] *
    result_df["進貨數量"]
).round(0)

# 預估利潤
result_df["預估利潤"] = (
    result_df["建議售價"] -
    result_df["台幣成本"]
).round(0)

# =========================
# 顯示結果
# =========================
st.subheader("計算結果")

st.dataframe(
    result_df,
    use_container_width=True
)

# =========================
# 統計資訊
# =========================
total_cost = result_df["總成本"].sum()
total_profit = (
    result_df["預估利潤"] *
    result_df["進貨數量"]
).sum()

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "總進貨成本",
        f"NT$ {total_cost:,.0f}"
    )

with col2:
    st.metric(
        "預估總利潤",
        f"NT$ {total_profit:,.0f}"
    )

# =========================
# CSV下載
# =========================
csv = result_df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="下載 CSV",
    data=csv,
    file_name="商品售價計算.csv",
    mime="text/csv"
)
