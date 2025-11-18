import streamlit as st
import pandas as pd
import altair as alt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("STCS_우리나라기후평년값_DD_20251118211755.csv", encoding="utf-8")
    return df

data = load_data()

st.title("우리나라 기후 평년값 대시보드")

# Show raw data
if st.checkbox("데이터 보기"):
    st.dataframe(data)

# Column selection
numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
date_cols = [col for col in data.columns if 'date' in col.lower() or '일' in col]

# Basic chart
target_col = st.selectbox("시각화할 컬럼 선택", numeric_cols)

chart = (
    alt.Chart(data)
    .mark_line()
    .encode(
        x=alt.X(date_cols[0] if date_cols else numeric_cols[0], title="날짜"),
        y=alt.Y(target_col, title=target_col),
        tooltip=[target_col]
    )
)

st.altair_chart(chart, use_container_width=True)

# Summary stats
st.subheader("요약 통계")
st.write(data[target_col].describe())

# Download processed CSV
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(label="CSV 다운로드", data=csv, file_name="processed_data.csv", mime='text/csv')
