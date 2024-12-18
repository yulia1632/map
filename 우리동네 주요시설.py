import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(page_title="우리 동네 시설 지도", layout="wide")
st.title("우리 동네 시설 지도")
st.write("### 지도에서 우리 동네 주요 시설들을 알아보고 탐험해보세요!")

# 2. 서울 다중이용시설 데이터 불러오기
DATA_FILE = "서울시 시설물 정보.csv"
try:
    data = pd.read_csv(DATA_FILE, encoding="cp949")

    # 인헌초등학교 위치 추가
    inheon_school = pd.DataFrame({
        "시설명": ["인헌초등학교"],
        "위도": [37.477243],  # 정확한 위도
        "경도": [126.963883],  # 정확한 경도
        "구": ["관악구"],
        "도로명주소": ["서울특별시 관악구 낙성대로 23"],
        "종류": ["학교"]
    })
    data = pd.concat([data, inheon_school], ignore_index=True)

    # 관악구 데이터로 한정
    st.write("#### 이번에는 관악구를 중심으로 우리 주변 시설들을 살펴보겠습니다!")
    gw_data = data[data["도로명주소"].str.contains("관악구", na=False)]

    # 지도 생성
    map_center = [37.477243, 126.963883]  # 관악구 중심
    m = folium.Map(location=map_center, zoom_start=13)

    # 시설 마커 추가
    st.write("#### 지도에서 각 시설을 클릭하면 이름과 역할을 확인할 수 있어요.")
    for _, row in gw_data.iterrows():
        popup_content = folium.Popup(f"<b>{row['시설명']}</b> - {row['종류']}", max_width=300)
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=popup_content,
            icon=folium.Icon(color="blue")
        ).add_to(m)

    # 인헌초등학교 특별 표시
    folium.Marker(
        location=[37.477243, 126.963883],
        popup=folium.Popup("<b>여기있어요!</b> 인헌초등학교", max_width=300),
        icon=folium.Icon(color="red")
    ).add_to(m)

    # 지도 표시
    st_folium(m, width=800, height=600)

    # 다중이용시설 목록 안내
    st.write("#### 이제 표로도 확인해볼까요?")
    st.write("아래 표에서 시설 이름과 종류를 확인하고, 위치와 역할을 떠올려보세요.")
    st.dataframe(gw_data)

    # 확인 문제 추가
    st.write("### 알아보아요!")
    st.write("우리 학교에서 가까운 시설은 무엇이 있나요?! 지도에서 찾아보고 아래에 적어봅시다.")
    answer1 = st.text_input("가까운 시설 이름을 입력하세요:")
    if answer1:
        st.success("잘했어요! 입력하신 시설: " + answer1)

    st.write("그 시설의 역할은 무엇인가요?")
    st.write("병원은 치료를, 도서관은 공부와 독서를, 공원은 산책과 휴식을 제공합니다. 다른 시설들은 어떤 역할을 할까요?")
    answer2 = st.text_input("시설의 역할을 입력하세요:")
    if answer2:
        st.success("좋아요! 입력하신 역할: " + answer2)

except FileNotFoundError:
    st.error("서울 다중이용시설 데이터 파일을 찾을 수 없습니다. '서울시 시설물 정보.csv' 파일이 올바른 경로에 있는지 확인해주세요.")
except Exception as e:
    st.error(f"데이터를 처리하는 중 오류가 발생했습니다: {e}")
