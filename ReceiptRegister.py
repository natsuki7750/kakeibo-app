import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="レシート登録", page_icon="🧾", layout="wide")
st.title("🧾 レシート・明細登録")

csv_path = "data/kakeibo.csv"

type_option = st.radio("区分を選択", ["支出", "収入", "固定費"])
date = st.date_input("日付", value=datetime.today())
amount = st.number_input("金額", min_value=0, step=100)
shop = st.text_input("店名（任意）")

# 自動カテゴリ推定（簡易版）
def estimate_category(shop_name, amount):
    if "セブン" in shop_name or "ファミマ" in shop_name:
        return "食費"
    elif amount >= 30000:
        return "住居費"
    else:
        return "未分類"

category = st.selectbox("カテゴリ（自動推定）", 
    ["食費", "光熱費", "通信費", "養育費", "教育費", "交際費", "雑費", "交通費", "医療費", "日用品", "衣類費", "住居費", "保険料", "税金", "娯楽費", "未分類"],
    index=["食費", "光熱費", "通信費", "養育費", "教育費", "交際費", "雑費", "交通費", "医療費", "日用品", "衣類費", "住居費", "保険料", "税金", "娯楽費", "未分類"].index(estimate_category(shop, amount))
)

if st.button("登録する"):
    new_row = pd.DataFrame([{
        "date": date.strftime("%Y-%m-%d"),
        "type": type_option,
        "category": category,
        "amount": amount,
        "shop": shop
    }])
    try:
        df = pd.read_csv(csv_path)
        df = pd.concat([df, new_row], ignore_index=True)
    except FileNotFoundError:
        df = new_row

    df.to_csv(csv_path, index=False, encoding="utf-8")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    df.to_csv(f"data/kakeibo_{timestamp}.csv", index=False, encoding="utf-8")
    st.success("登録しました！")