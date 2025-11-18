import streamlit as st
import pandas as pd
import altair as alt

# --------------------------------------------------
# 1) 파일 경로
# --------------------------------------------------
FILE = "STCS_우리나라기후평년값_DD_20251118211755.csv"

# --------------------------------------------------
# 2) CSV 로드 함수 (EUC-KR 고정 + 안정적 예외처리)
# --------------------------------------------------
@st.cache_data
def load_data(path):
    try:
        # 가장 가능성 높은 EUC-KR로 직접 로드
        return pd.read_csv(path, encoding="euc-kr")
    except:
        try:
            # UTF-8 BOM 가능성
            return pd.read_csv(path, encoding="utf-8-sig")
        except:
            try:
                # 구분자 자동 추론
                return pd.read_csv(path, encoding="euc-kr", sep=None, engine="python")
            except Exception as e:
                st.error(f"CSV 파일을 읽을 수 없습니다: {e}")
                return pd.DataFrame()

# --------------------------------------------------
# 3) 데이터 불러오기
# --------------------------------------------------
data = load_data(FILE)

st.title("우리나라 기후 평년값 대시보드 (안정 버전)")

# --------------------------------------------------
# 4) 데이터 확인
# --------------------------------------------------
if st.checkbox("데이터 보기"):
    st.dataframe(data)

# --------------------------------------------------
# 5) 숫자 컬럼 자동 감지
# --------------------------------------------------
if len(data) == 0:
    st.stop()

numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

if len(numeric_cols) == 0:
    st.warning("숫자형 컬럼이 없습니다.")
    st.stop()

# --------------------------------------------------
# 6) 날짜 또는 인덱스 기반 x축 설정
# --------------------------------------------------
# 날짜 컬럼 찾기 (없으면 인덱스 사용)
date_cols = [c for c in data.columns if any(k in c.lower() for k in ["date", "일", "날짜"])]

if date_cols:
    x_col = date_cols[0]
else:
    data = data.reset_index()
    x_col = "index"

# --------------------------------------------------
# 7) 시각화
# --------------------------------------------------
target_col = st.selectbox("시각화할 숫자 컬럼 선택", numeric_cols)

chart = (
    alt.Chart(data)
    .mark_line()
    .encode(
        x=alt.X(x_col, title="X축"),
        y=alt.Y(target_col, title=target_col),
        tooltip=[target_col]
    )
)

st.altair_chart(chart, use_container_width=True)

# --------------------------------------------------
# 8) 요약 통계
# --------------------------------------------------
st.subheader("요약 통계")
st.write(data[target_col].describe())

# --------------------------------------------------
# 9) 다운로드
# --------------------------------------------------
csv = data.to_csv(index=False).encode('utf-8-sig')
st.download_button("CSV 다운로드", csv, "processed_data.csv", "text/csv")
