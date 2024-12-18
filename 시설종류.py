import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# 1. 페이지 설정
st.set_page_config(page_title="우리 주변에는 어떤 시설이 있나요?", layout="wide")
st.title("우리 주변에는 어떤 시설이 있나요?")
st.write("### 우리 생활 속에서 중요한 시설들을 배우고, 직접 찾아볼 수 있는 시간을 가져보아요.")

# 2. Geocoding 설정
geolocator = Nominatim(user_agent="geoapi")

def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        st.error(f"Geocoding 오류: {e}")
        return None, None

def extract_district(address):
    try:
        if "구" in address:
            return address.split("구")[0].split()[-1] + "구"
        else:
            return "알 수 없음"
    except Exception as e:
        return "알 수 없음"

# 3. 색상 매핑
facility_colors = {
    "병원": "blue",
    "공원": "green",
    "도서관": "purple",
    "구청": "orange",
    "경찰서": "red",
    "소방서": "darkred",
    "우체국": "pink",
    "체육센터": "cadetblue",
    "쇼핑/유통": "lightgreen",
    "교육/문화": "darkblue",
    "기타": "gray"
}

# 4. 서울 다중이용시설 데이터 불러오기
DATA_FILE = "서울시 시설물 정보.csv"
try:
    data = pd.read_csv(DATA_FILE, encoding="cp949")

    # 도로명 주소에서 구 이름 추출
    if "구" not in data.columns:
        data["구"] = data["도로명주소"].apply(extract_district)

    # 구 필터 안내
    st.write("#### 이번에는 우리 동네가 속한 구를 선택해볼까요?")
    st.write("구는 우리 생활 주변의 행정구역을 의미해요. 원하는 구를 선택해보세요.")
    region_filter = st.selectbox("구 선택", options=["전체"] + sorted(data["구"].unique()))

    # 시설 필터 안내
    st.write("#### 이번에는 시설의 종류를 살펴봅시다!")
    st.write("병원, 공원, 도서관 등 우리 주변의 다양한 시설들이 어떤 역할을 하는지 알아볼까요?")
    type_filter = st.selectbox("시설 종류 선택", options=["전체"] + sorted(data["종류"].unique()))

    filtered_data = data
    if region_filter != "전체":
        filtered_data = filtered_data[filtered_data["구"] == region_filter]
    if type_filter != "전체":
        filtered_data = filtered_data[filtered_data["종류"] == type_filter]

    # 지도 생성
    map_center = [filtered_data["위도"].mean(), filtered_data["경도"].mean()] if not filtered_data.empty else [37.5665, 126.9780]
    m = folium.Map(location=map_center, zoom_start=12)

    # 시설 점 추가
    st.write("#### 지도에서 선택한 시설을 확인해보세요!")
    st.write("지도에 표시된 점은 선택한 시설들을 나타냅니다. 각 시설을 클릭해 정보를 확인해보세요.")
    for _, row in filtered_data.iterrows():
        marker_color = facility_colors.get(row["종류"], "gray")
        folium.CircleMarker(
            location=[row["위도"], row["경도"]],
            radius=5,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.7
        ).add_to(m)

    # 지도 표시
    st_folium(m, width=800, height=600)

    # 다중이용시설 목록 안내
    st.write("#### 이제 목록으로도 확인해보세요!")
    st.write("시설 목록은 선택한 구와 시설 종류에 따라 변경됩니다. 우리 동네에는 어떤 시설들이 있는지 알아보세요.")
    st.dataframe(filtered_data)

    # 확인 문제 추가
    st.write("### 알아보아요!")
    st.write("우리 동네 구 이름은 무엇인가요?")
    st.write("구 이름은 선택한 지역을 나타냅니다. 예를 들어 '관악구'와 같은 이름을 입력하세요.")
    user_answer = st.text_input("구 이름을 입력하세요:")

    if user_answer:
        if user_answer == region_filter:
            st.success("정답입니다! 다음 챕터로 넘어가세요.")
        else:
            st.error("틀렸습니다. 다시 생각해보세요!")

except FileNotFoundError:
    st.error("서울 다중이용시설 데이터 파일을 찾을 수 없습니다. '서울시 시설물 정보.csv' 파일이 올바른 경로에 있는지 확인해주세요.")
except Exception as e:
    st.error(f"데이터를 처리하는 중 오류가 발생했습니다: {e}")
