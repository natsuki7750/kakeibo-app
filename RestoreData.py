import streamlit as st
import os
import glob
import shutil

st.set_page_config(page_title="復元", page_icon="🕒", layout="wide")
st.title("🕒 家計簿データの復元")

csv_path = "data/kakeibo.csv"
backup_files = sorted(glob.glob("data/kakeibo_*.csv"), reverse=True)

if not backup_files:
    st.warning("復元可能なバックアップが見つかりません。")
    st.stop()

backup_labels = [os.path.basename(f).replace(".csv", "") for f in backup_files]

st.markdown("""
### ✅ 復元について
- 過去に保存された家計簿データを復元できます
- 復元すると現在のデータは**上書きされます**
- 保存履歴は**最大半年分**を目安に管理してください
""")

selected_backup = st.selectbox("復元する日時を選択", backup_labels)

if st.button("このデータに復元する（上書き確認）"):
    backup_path = f"data/{selected_backup}.csv"
    if os.path.exists(backup_path):
        shutil.copy(backup_path, csv_path)
        st.success(f"{selected_backup} のデータに復元しました！")
    else:
        st.error("選択されたバックアップファイルが見つかりません。")