import streamlit as st

st.set_page_config(page_title="家計簿アプリ", layout="centered")

st.title("📊 家計簿アプリ")

st.markdown("""
このアプリは、スマホでかんたんに使える家計簿管理ツールです。  
レシートの写真を撮るだけで自動で読み取ったり、手入力でも登録できます。  
月ごとの収支やカテゴリ別の支出をグラフで確認できます。
""")

st.subheader("主な機能")
st.markdown("""
- レシートの写真を撮って登録（自動読み取り）  
- 手入力での明細登録もOK  
- 予算の設定・編集  
- 月ごとの収支グラフ  
- カテゴリ別の支出グラフ  
- CSV形式で保存（クラウド不要）  
- 過去のデータ復元（最大半年分）
""")

st.info("まずは下のボタンから始めてみましょう！")

col1, col2 = st.columns(2)
with col1:
    if st.button("📷 レシート登録へ"):
        st.switch_page("pages/ReceiptRegister.py")
with col2:
    if st.button("📈 グラフを見る"):
        st.switch_page("pages/GraphView.py")
