import streamlit as st
import pandas as pd
import altair as alt
import chardet

st.title("우리나라 기후 평년값 대시보드")

# ---------------------
# 안전한 CSV 로딩 함수
# ---------------------
@st.cache_data
def load_data(path):
    import chardet
    # 인코딩 자동 감지
    with open(path, "rb") as f:
        raw = f.read()
        result = chardet.detect(raw)
        enc = result.get("encoding", "utf-8")

    # try-except 전체 블록
    try:
        df = pd.read_csv(path, encoding=enc)
        return df
    except Exception:
        pass

    for enc2 in ["cp949", "euc-kr", "utf-8"]:
        try:
            df = pd.read_csv(path, encoding=enc2)
            return df
        except Exception:
            pass

    st.error("CSV 파일을 읽을 수 없습니다.")
    return pd.DataFrame()

# ---------------------
# CSV 파일 로드
# ---------------------
FILE = "STCS_우리나라기후평년값_DD_20251118211755.csv"

data = load_data(FILE)

# ---------------------
# 데이터 보기
# ---------------------
if st.checkbox("데이터 보기"):
    st.dataframe(pd.DataFrame(data))

# ---------------------
# 컬럼 분류
# ---------------------
try:
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
except:
    numeric_cols = []

# x축 컬럼 강제 문자열 변환
stringified = data.astype(str)

# ---------------------
# 시각화 컬럼 선택
# ---------------------
if numeric_cols:
    target_col = st.selectbox("시각화할 컬럼 선택", numeric_cols)
else:
    st.error("수치형 컬럼이 없어서 그래프를 생성할 수 없습니다.")
    st.stop()

# ---------------------
# 안정적인 Altair 차트 생성
# ---------------------
alt.data_transformers.disable_max_rows()

chart = (
    alt.Chart(stringified.reset_index())
    .mark_line()
    .encode(
        x=alt.X("index:N", title="행 번호"),
        y=alt.Y(target_col, title=target_col),
        tooltip=[target_col]
    )
)

st.altair_chart(chart, use_container_width=True)

# ---------------------
# 요약 통계
# ---------------------
st.subheader("요약 통계")
st.write(data[target_col].describe())

# ---------------------
# 파일 다운로드
# ---------------------
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="CSV 다운로드",
    data=csv,
    file_name="processed_data.csv",
    mime='text/csv'
)
