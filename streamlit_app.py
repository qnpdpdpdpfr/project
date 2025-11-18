import streamlit as st
import pandas as pd
import chardet

FILE = "STCS_우리나라기후평년값_DD_20251118211755.csv"

# ------------------------------------------------
# 인코딩 자동 감지
# ------------------------------------------------
with open(FILE, "rb") as f:
    raw = f.read()
detected = chardet.detect(raw)
encoding = detected["encoding"]

# ------------------------------------------------
# CSV 읽기 (try/except 없음)
# ------------------------------------------------
data = pd.read_csv(FILE, encoding=encoding)

# ------------------------------------------------
# Streamlit UI
# ------------------------------------------------
st.title("기후평년값 대시보드")
st.write(f"Detected Encoding: **{encoding}**")

st.dataframe(data)

