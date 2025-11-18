import streamlit as st
import pandas as pd
import altair as alt
import chardet

FILE = "STCS_우리나라기후평년값_DD_20251118211755.csv"

# ---------------------
# 안전한 CSV 로딩 함수 (오류 X)
# ---------------------
@st.cache_data
def load_data(path):
    # 1) chardet로 인코딩 감지
    with open(path, "rb") as f:
        raw = f.read()
        detect = chardet.detect(raw)
        enc = detect["encoding"]

    # 2) 감지된 인코딩으로 읽기
    try:
        df = pd.read_csv(path, encoding=enc)
        return df
    except:
        pass

    # 3) 최종 fallback
    for enc2 in ["cp949", "euc-kr", "utf-8"]:
        try:
            df = pd.read_csv(path, encoding=enc2)
            return df
        except:
            continue

    # 모두 실패한 경우
    st.error("CSV 파일을 읽을 수 없습니다.")
    return pd.DataFrame()

# ---------------------
# 데이터 로드
# ---------------------
data = load_data(FILE)

st.title("우리나라 기후 평년값 대시보드")

# ---------------------
# 데이터 보기
# ---------------------
if st.checkbox("데이터 보기"):
    st.dataframe(data)

# ---------------------
# 시각화
# ---------------------
numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

# 날짜 컬럼 자동 탐색 (없으면 첫 번째 컬럼 사용)
date_cols = [c for c in data.columns if "일" in c or "date" in c.lower()]
x_col = date_cols[0] if date_cols else data.columns[0]

target_col = st.selectbox("시각화할 컬럼 선택", numeric_cols)

chart = (
    alt.Chart(data)
    .mark_line()
    .encode(
        x=alt.X(x_col, title="날짜"),
        y=alt.Y(target_col, title=target_col),
        tooltip=[x_col, target_col]
    )
)

st.altair_chart(chart, use_container_width=True)

# ---------------------
# 요약 통계
# ---------------------
st.subheader("요약 통계")
st.write(data[target_col].describe())

# ---------------------
# 다운로드 버튼
# ---------------------
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="CSV 다운로드",
    data=csv,
    file_name="processed_data.csv",
    mime="text/csv"
)
