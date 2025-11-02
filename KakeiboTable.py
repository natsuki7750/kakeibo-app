import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="家計表", page_icon="📋", layout="wide")
st.title("📋 家計表（編集・削除機能付き）")

csv_path = "data/kakeibo.csv"
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.warning("家計簿データが見つかりません。まずはレシート登録を行ってください。")
    st.stop()

df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
month_filter = st.selectbox("表示する月を選択", sorted(df["month"].unique()))
df_filtered = df[df["month"] == month_filter].copy()

edited_rows = []
delete_flags = []
category_options = ["食費", "光熱費", "通信費", "養育費", "教育費", "交際費", "雑費", "交通費", "医療費", "日用品", "衣類費", "住居費", "保険料", "税金", "娯楽費", "未分類"]

st.markdown("### 編集・削除対象一覧")

for i, row in df_filtered.iterrows():
    st.write(f"🧾 {row['date']} | {row['shop']}")
    new_amount = st.number_input(f"金額（行 {i}）", value=row["amount"], min_value=0, step=100)
    new_cat = st.selectbox(f"カテゴリ（行 {i}）", category_options, index=category_options.index(row["category"]))
    delete = st.checkbox(f"この行を削除（行 {i}）", value=False)
    edited_rows.append((i, new_amount, new_cat))
    delete_flags.append((i, delete))

if st.button("編集内容を保存する"):
    for idx, new_amount, new_cat in edited_rows:
        df.at[idx, "amount"] = new_amount
        df.at[idx, "category"] = new_cat
    df.to_csv(csv_path, index=False, encoding="utf-8")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    df.to_csv(f"data/kakeibo_{timestamp}.csv", index=False, encoding="utf-8")
    st.success("編集内容を保存しました！")

if st.button("チェックされた行を削除する"):
    delete_indices = [idx for idx, flag in delete_flags if flag]
    if delete_indices:
        df = df.drop(index=delete_indices).reset_index(drop=True)
        df.to_csv(csv_path, index=False, encoding="utf-8")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        df.to_csv(f"data/kakeibo_{timestamp}.csv", index=False, encoding="utf-8")
        st.success(f"{len(delete_indices)} 行を削除しました！")
    else:
        st.info("削除対象が選択されていません。")