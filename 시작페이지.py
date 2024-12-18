import streamlit as st

# 메인 페이지
st.set_page_config(page_title="우리동네 주요시설 알아보기", layout="wide")
st.title("우리동네 주요시설 알아보기")
st.image("ourtown.jpg", width=600)

# 오늘의 학습목표 추가
st.markdown("<h2 style='text-align: center;'>오늘의 학습목표</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>내가 살고있는 동네의 위치를 알고, 주요 시설을 지도에서 확인한다.</h3>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'> ⬅️시설 종류 탭을 누르세요!</h2>", unsafe_allow_html=True)
