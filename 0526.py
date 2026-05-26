import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(
    page_title="網拍售價系統",
    layout="wide"
)

st.title("網拍進價與建議售價")

# =========================
# Google Sheets 認證
# =========================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

# =========================
# 讀取 Google Sheet
# =========================
sheet = client.open("Tasks").sheet1

data = sheet.get_all_records()

df = pd.DataFrame(data)

# =========================
# 參數
# =========================
exchange_rate = 9
shopee_fee = 0.20
profit_rate = 0.15

# =========================
# 計算
# =========================
df["台幣成本"] = (
    df["人民幣進價"] * exchange_rate
)

df["建議售價"] = (
    df["台幣成本"] *
    (1 + shopee_fee + profit_rate)
).round(0)

df["總成本"] = (
    df["台幣成本"] *
    df["進貨數量"]
).round(0)

# =========================
# 顯示
# =========================
st.dataframe(
    df,
    use_container_width=True
)
