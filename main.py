import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화 216편의 데이터를 그래프로 살펴봅니다.")

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

try:
    df = pd.read_csv(DATA_URL)
except Exception as e:
    st.error("데이터를 불러오지 못했습니다.")
    st.stop()

# --------------------------------------------------
# 데이터 전처리
# --------------------------------------------------

# 장르가 여러 개이면 첫 번째 장르만 사용
df["genre"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 숫자 열을 숫자형으로 변환
number_columns = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10"
]

for col in number_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# 그래프 1
# --------------------------------------------------
st.divider()
st.header("📊 그래프 1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    height=550,
    legend_title="장르"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info("장르별로 1년 동안 박스오피스 10위권에 진입한 영화가 몇 편씩 있었는지와 각 장르가 차지하는 비율을 알 수 있습니다.")
