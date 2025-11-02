import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

st.set_page_config(page_title="グラフ表示", page_icon="📈", layout="wide")
st.title("📈 家計グラフ表示")

csv_path = "data/kakeibo.csv"
df = pd.read_csv(csv_path)
df["date"] = pd.to_datetime(df["date"])

st.sidebar.markdown("### 📅 表示期間")
period = st.sidebar.radio("期間を選択", ["過去1年", "全期間"])

if period == "過去1年":
    one_year_ago = datetime.today() - timedelta(days=365)
    df = df[df["date"] >= one_year_ago]

df["month"] = df["date"].dt.to_period("M").astype(str)
monthly = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
monthly["貯蓄額"] = monthly.get("収入", 0) - monthly.get("支出", 0) - monthly.get("固定費", 0)
monthly = monthly.reset_index()

st.subheader("📊 月別収支推移と貯蓄額")

base = alt.Chart(monthly).encode(x="month:N")

bars = base.mark_bar().encode(
    y=alt.Y("支出:Q", title="金額"),
    color=alt.value("#D0021B"),
    tooltip=["month", "支出"]
) + base.mark_bar().encode(
    y="収入:Q",
    color=alt.value("#4A90E2"),
    tooltip=["month", "収入"]
) + base.mark_bar().encode(
    y="固定費:Q",
    color=alt.value("#6BA368"),
    tooltip=["month", "固定費"]
)

line = base.mark_line(point=True, color="black").encode(
    y=alt.Y("貯蓄額:Q", title="金額"),
    tooltip=["month", "貯蓄額"]
)

st.altair_chart(bars + line, use_container_width=True)

st.subheader("📊 カテゴリ別支出（パレート図）")

df_spend = df[df["type"] == "支出"]
cat_sum = df_spend.groupby("category")["amount"].sum().sort_values(ascending=False)
cat_df = cat_sum.reset_index()
cat_df["累積比率"] = cat_df["amount"].cumsum() / cat_df["amount"].sum() * 100

color_map = {
    "食費": "#6BA368", "光熱費": "#4A90E2", "通信費": "#34495E", "養育費": "#F5A623",
    "教育費": "#F8E71C", "交際費": "#D96C9D", "雑費": "#95A5A6", "交通費": "#8B572A",
    "医療費": "#D0021B", "日用品": "#D5C4A1", "衣類費": "#9013FE", "住居費": "#0B5345",
    "保険料": "#5D6D7E", "税金": "#7B241C", "娯楽費": "#50E3C2", "未分類": "#CCCCCC"
}

bar = alt.Chart(cat_df).mark_bar().encode(
    x=alt.X("category:N", title="カテゴリ"),
    y=alt.Y("amount:Q", title="支出額"),
    color=alt.Color("category:N", scale=alt.Scale(domain=list(color_map.keys()), range=list(color_map.values()))),
    tooltip=["category", "amount"]
)

line = alt.Chart(cat_df).mark_line(point=True, color="gray").encode(
    x="category:N",
    y=alt.Y("累積比率:Q", title="累積比率"),
    tooltip=["category", "累積比率"]
)

st.altair_chart(bar + line, use_container_width=True)