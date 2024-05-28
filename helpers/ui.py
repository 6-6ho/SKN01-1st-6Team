from sqlalchemy import create_engine
import streamlit as st
from streamlit_option_menu import option_menu

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd

import datetime
from datetime import datetime as dt

from PIL import Image
import base64
from io import BytesIO

scroll_script = """
<script>
    // 스크롤 위치 저장 함수
    function saveScrollPos() {
        localStorage.setItem('scrollPos', window.scrollY);
    }

    // 페이지 로드 시 스크롤 위치 복원
    document.addEventListener('DOMContentLoaded', (event) => {
        let scrollPos = localStorage.getItem('scrollPos');
        if (scrollPos) {
            window.scrollTo(0, parseInt(scrollPos));
        }
    });

    // 페이지를 떠나기 전 스크롤 위치 저장
    window.addEventListener('beforeunload', (event) => {
        saveScrollPos();
    });
</script>
"""

# matplotlib 한글폰트 이슈 때문에 항상 해주는 세팅
# 한글폰트 설정
# Windows, 리눅스 사용자
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


class Ui:
    def __init__(self, appname):

        st.title(appname)

        # 페이지 상태 초기화
        if "page" not in st.session_state:
            st.session_state.page = "HOME"

        # 추가
        if "faq_page" not in st.session_state:
            st.session_state.faq_page = 1

        self.run()

    def home(self):

        # with st.sidebar: 사이드바 페이지 전환
        menu = option_menu(
            None,
            ["HOME", "전국 자동차 등록현황", "FAQ 조회시스템"],
            icons=["house", "kanban", "list-task"],
            menu_icon="app-indicator",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "4!important", "background-color": "black"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "color": "white",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#00bcff5c",
                },
                "nav-link-selected": {"background-color": "#00bcff5c"},
            },
        )

        if menu == "HOME":
            self.show_home()
        elif menu == "전국 자동차 등록현황":
            self.show_car_registration_status()
        elif menu == "FAQ 조회시스템":
            self.show_faq_system()

    ### HOME 화면
    def show_home(self):
        st.markdown("# :green[HOME Dashboard] 📊")
        st.markdown(
            "###### Contributors : :green[민경원], :green[허우영], :green[이민재], :green[송준호]"
        )

        sample_code = """
                class Streamlit:                
                    def project01(self, 조원1, 조원2, 조원3, 조원4):
                        self.조원1 = "조원1"
                        self.조원2 = "조원2"
                        self.조원3 = "조원3"
                        self.조원4 = "조원4"
                        
                        return 조원1, 조원2, 조원3, 조원4
                
                streamlit_team = Streamlit()                        
                contributors = streamlit_team.project01("민경원", "허우영", "이민재", "송준호")
                print("Contributors " + contributors)
        """
        st.code(sample_code, language="python")
        st.write("")
        st.write("")
        st.write("")

        # 도넛 차트
        car_data = self.load_car_data()
        van_data = self.load_van_data()
        truck_data = self.load_truck_data()
        special_vehicle_data = self.load_special_vehicle_data()

        # 컬럼명 변경 + 데이터 타입 확인 및 변환
        car_data.rename(
            columns={
                "district": "지역명",
                "gov_car": "관용 승용차",
                "private_car": "자가용 승용차",
                "commercial_car": "영업용 승용차",
                "total_car": "승용차 합계",
            },
            inplace=True,
        )
        car_data["관용 승용차"] = pd.to_numeric(
            car_data["관용 승용차"], errors="coerce"
        )
        car_data["자가용 승용차"] = pd.to_numeric(
            car_data["자가용 승용차"], errors="coerce"
        )
        car_data["영업용 승용차"] = pd.to_numeric(
            car_data["영업용 승용차"], errors="coerce"
        )
        car_data["승용차 합계"] = pd.to_numeric(
            car_data["승용차 합계"], errors="coerce"
        )

        van_data.rename(
            columns={
                "district": "지역명",
                "gov_van": "관용 승합차",
                "private_van": "자가용 승합차",
                "commercial_van": "영업용 승합차",
                "total_van": "승합차 합계",
            },
            inplace=True,
        )
        van_data["관용 승합차"] = pd.to_numeric(
            van_data["관용 승합차"], errors="coerce"
        )
        van_data["자가용 승합차"] = pd.to_numeric(
            van_data["자가용 승합차"], errors="coerce"
        )
        van_data["영업용 승합차"] = pd.to_numeric(
            van_data["영업용 승합차"], errors="coerce"
        )
        van_data["승합차 합계"] = pd.to_numeric(
            van_data["승합차 합계"], errors="coerce"
        )

        truck_data.rename(
            columns={
                "district": "지역명",
                "gov_truck": "관용 화물차",
                "private_truck": "자가용 화물차",
                "commercial_truck": "영업용 화물차",
                "total_truck": "화물차 합계",
            },
            inplace=True,
        )
        truck_data["관용 화물차"] = pd.to_numeric(
            truck_data["관용 화물차"], errors="coerce"
        )
        truck_data["자가용 화물차"] = pd.to_numeric(
            truck_data["자가용 화물차"], errors="coerce"
        )
        truck_data["영업용 화물차"] = pd.to_numeric(
            truck_data["영업용 화물차"], errors="coerce"
        )
        truck_data["화물차 합계"] = pd.to_numeric(
            truck_data["화물차 합계"], errors="coerce"
        )

        special_vehicle_data.rename(
            columns={
                "district": "지역명",
                "gov_special": "관용 특수차",
                "private_special": "자가용 특수차",
                "commercial_special": "영업용 특수차",
                "total_special": "특수차 합계",
            },
            inplace=True,
        )
        special_vehicle_data["관용 특수차"] = pd.to_numeric(
            special_vehicle_data["관용 특수차"], errors="coerce"
        )
        special_vehicle_data["자가용 특수차"] = pd.to_numeric(
            special_vehicle_data["자가용 특수차"], errors="coerce"
        )
        special_vehicle_data["영업용 특수차"] = pd.to_numeric(
            special_vehicle_data["영업용 특수차"], errors="coerce"
        )
        special_vehicle_data["특수차 합계"] = pd.to_numeric(
            special_vehicle_data["특수차 합계"], errors="coerce"
        )

        st.subheader("차종별 지역 분포")
        # 한 줄에 두 개의 컬럼을 생성합니다.
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            fig1 = px.pie(
                car_data,
                names="지역명",
                values="승용차 합계",
                title="CAR(승용차) 기준",
                hole=0.5,
                width=390,
                height=505,
            )
            st.plotly_chart(fig1)

        with col2:
            fig2 = px.pie(
                van_data,
                names="지역명",
                values="승합차 합계",
                title="VAN(승합차) 기준",
                hole=0.5,
                width=390,
                height=505,
            )
            st.plotly_chart(fig2)

        with col3:
            fig3 = px.pie(
                truck_data,
                names="지역명",
                values="화물차 합계",
                title="TRUCK(화물차) 기준",
                hole=0.5,
                width=390,
                height=505,
            )
            st.plotly_chart(fig3)

        with col4:
            fig4 = px.pie(
                special_vehicle_data,
                names="지역명",
                values="특수차 합계",
                title="SV(특수차) 기준",
                hole=0.5,
                width=390,
                height=505,
            )
            st.plotly_chart(fig4)

        st.write("")
        st.write("")
        st.write("")

        st.subheader("방명록")
        title = st.text_input("제목", key="home_text_title")
        content = st.text_area("내용", key="home_text_content")

        if st.button("작성", key="home_submit"):
            st.subheader("게시글 목록")
            st.write("제목:", title)
            st.write("내용:", content)
            st.success("게시글이 HOME 화면에 작성되었습니다.")

    ##### 전국 자동차 등록 현황
    def show_car_registration_status(self):
        st.title("전국 자동차 등록현황")
        total_car = self.sum_total_car()
        total_special = self.sum_total_special()
        total_truck = self.sum_total_truck()
        total_van = self.sum_total_van()
        total_ccc = (
            int(total_car.iloc[0][0])
            + int(total_special.iloc[0][0])
            + int(total_truck.iloc[0][0])
            + int(total_van.iloc[0][0])
        )
        r_total_ccc = format(total_ccc, ",")
        st.write(f"24년 4월 기준, 전국 자동차 등록 대수는 {r_total_ccc}대 입니다.")
        k1, k2 = st.columns([0.5, 0.5])

        submenu = option_menu(
            None,
            ["전국 자동차 등록현황", "도시별 자동차 등록현황"],
            menu_icon="app-indicator",
            icons=["car-front-fill", "car-front"],
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "4!important", "background-color": "black"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "color": "white",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#00bcff5c",
                },
                "nav-link-selected": {"background-color": "#00bcff5c"},
            },
        )
        if submenu == "전국 자동차 등록현황":
            second_menu = option_menu(
                None,
                ["전국 용도별 자동차 등록 현황", "전국 차종별 자동차 등록 현황"],
                menu_icon="app-indicator",
                default_index=0,
                orientation="horizontal",
                styles={
                    "container": {
                        "padding": "4!important",
                        "background-color": "black",
                    },
                    "icon": {"color": "white", "font-size": "25px"},
                    "nav-link": {
                        "font-size": "16px",
                        "color": "white",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#00bcff5c",
                    },
                    "nav-link-selected": {"background-color": "#00bcff5c"},
                },
            )
            with k1:
                if second_menu == "전국 용도별 자동차 등록 현황":
                    pri_total_car = self.pri_total_car()
                    pri_total_special = self.pri_total_special()
                    pri_total_truck = self.pri_total_truck()
                    pri_total_van = self.pri_total_van()
                    pri_total_ccc = (
                        int(pri_total_car.iloc[0][0])
                        + int(pri_total_special.iloc[0][0])
                        + int(pri_total_truck.iloc[0][0])
                        + int(pri_total_van.iloc[0][0])
                    )
                    st.write(
                        f"전국 자가용 자동차 등록 대수 : {format(pri_total_ccc,',')}대"
                    )

                    com_total_car = self.com_total_car()
                    com_total_special = self.com_total_special()
                    com_total_truck = self.com_total_truck()
                    com_total_van = self.com_total_van()
                    com_total_ccc = (
                        int(com_total_car.iloc[0][0])
                        + int(com_total_special.iloc[0][0])
                        + int(com_total_truck.iloc[0][0])
                        + int(com_total_van.iloc[0][0])
                    )
                    st.write(
                        f"전국 영업용 자동차 등록 대수 : {format(com_total_ccc,',')}대"
                    )

                    gov_total_car = self.gov_total_car()
                    gov_total_special = self.gov_total_special()
                    gov_total_truck = self.gov_total_truck()
                    gov_total_van = self.gov_total_van()
                    gov_total_ccc = (
                        int(gov_total_car.iloc[0][0])
                        + int(gov_total_special.iloc[0][0])
                        + int(gov_total_truck.iloc[0][0])
                        + int(gov_total_van.iloc[0][0])
                    )
                    st.write(
                        f"전국 관용 자동차 등록 대수 : {format(gov_total_ccc,',')}대"
                    )
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.dataframe(
                        {
                            "용도": ["자가용", "영업용", "관용"],
                            "대수(대)": [pri_total_ccc, com_total_ccc, gov_total_ccc],
                        },
                        use_container_width=True,
                    )
                    with k2:
                        fig = px.pie(
                            names=["자가용", "영업용", "관용"],
                            values=[pri_total_ccc, com_total_ccc, gov_total_ccc],
                        )
                        st.plotly_chart(fig)
                elif second_menu == "전국 차종별 자동차 등록 현황":
                    st.write(
                        f"전국 승용차 등록 대수 : {format(int(total_car.iloc[0]),',')}대"
                    )
                    st.write(
                        f"전국 승합차 등록 대수 : {format(int(total_van.iloc[0]),',')}대"
                    )
                    st.write(
                        f"전국 화물차 등록 대수 : {format(int(total_truck.iloc[0]),',')}대"
                    )
                    st.write(
                        f"전국 특수차 등록 대수 : {format(int(total_special.iloc[0]),',')}대"
                    )
                    st.write("")
                    st.write("")
                    st.dataframe(
                        {
                            "용도": ["승용차", "승합차", "화물차", "특수차"],
                            "대수(대)": [
                                int(total_car.iloc[0]),
                                int(total_van.iloc[0]),
                                int(total_truck.iloc[0]),
                                int(total_special.iloc[0]),
                            ],
                        },
                        use_container_width=True,
                    )
                    with k2:
                        fig = px.pie(
                            names=["승용차", "승합차", "화물차", "특수차"],
                            values=[
                                int(total_car.iloc[0]),
                                int(total_van.iloc[0]),
                                int(total_truck.iloc[0]),
                                int(total_special.iloc[0]),
                            ],
                        )
                        st.plotly_chart(fig)
        elif submenu == "도시별 자동차 등록현황":
            p1, p2 = st.columns([0.45, 0.55])
            with p1:
                city_list = self.get_city_list()
                city_choice = st.selectbox("도시 선택", city_list)

                if city_choice == "강원":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":
                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다.",
                        )
                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "경기":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "경남":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "경북":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "광주":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "대구":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "대전":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "부산":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "서울":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "세종":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "울산":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "인천":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "전남":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "전북":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "제주":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "충남":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

                if city_choice == "충북":
                    radio_sorting = st.radio(
                        label="정렬 방식", options=["용도별", "차종별"], horizontal=True
                    )
                    city_car = self.get_citys_car_list(city_choice)
                    city_special = self.get_citys_special_list(city_choice)
                    city_truck = self.get_citys_truck_list(city_choice)
                    city_van = self.get_citys_van_list(city_choice)
                    if radio_sorting == "용도별":

                        dcar_gov = (
                            int(city_car.iloc[0][0])
                            + int(city_special.iloc[0][0])
                            + int(city_truck.iloc[0][0])
                            + int(city_van.iloc[0][0])
                        )
                        dcar_com = (
                            int(city_car.iloc[0][1])
                            + int(city_special.iloc[0][1])
                            + int(city_truck.iloc[0][1])
                            + int(city_van.iloc[0][1])
                        )
                        dcar_pri = (
                            int(city_car.iloc[0][2])
                            + int(city_special.iloc[0][2])
                            + int(city_truck.iloc[0][2])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(dcar_gov+dcar_com+dcar_pri, ',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["자가용", "영업용", "관용"],
                                "대수(대)": [dcar_pri, dcar_com, dcar_gov],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["자가용", "영업용", "관용"],
                                values=[dcar_pri, dcar_com, dcar_gov],
                            )
                            st.plotly_chart(fig)
                    else:
                        d_car = (
                            int(city_car.iloc[0][0])
                            + int(city_car.iloc[0][1])
                            + int(city_car.iloc[0][2])
                        )
                        d_spv = (
                            int(city_special.iloc[0][0])
                            + int(city_special.iloc[0][1])
                            + int(city_special.iloc[0][2])
                        )
                        d_tru = (
                            int(city_truck.iloc[0][0])
                            + int(city_truck.iloc[0][1])
                            + int(city_truck.iloc[0][2])
                        )
                        d_van = (
                            int(city_van.iloc[0][0])
                            + int(city_van.iloc[0][1])
                            + int(city_van.iloc[0][2])
                        )
                        st.write(
                            f"{city_choice}의 전체 차량은 {format(d_car+d_spv+d_tru+d_van,',')}대 입니다."
                        )

                        st.dataframe(
                            {
                                "용도": ["승용차", "승합차", "화물차", "특수차"],
                                "대수(대)": [d_car, d_van, d_tru, d_spv],
                            },
                            use_container_width=True,
                        )
                        with p2:
                            fig = px.pie(
                                names=["승용차", "승합차", "화물차", "특수차"],
                                values=[d_car, d_van, d_tru, d_spv],
                            )
                            st.plotly_chart(fig)

        ### CAR
        st.title("🚗")
        st.subheader("전국 시도별 승용차 등록 현황 (단위: 대)")
        car_data = self.load_car_data()
        # 컬럼명 변경
        car_data.rename(
            columns={
                "district": "지역명",
                "gov_car": "관용 승용차",
                "private_car": "자가용 승용차",
                "commercial_car": "영업용 승용차",
                "total_car": "승합차 합계",
            },
            inplace=True,
        )
        # 특정 컬럼 제거
        car_data.drop(columns=["id", "region_id"], inplace=True)
        # 쿼리 결과 테이블 뿌려주기
        st.table(car_data)
        st.write("")
        st.write("")
        st.write("")

        ### VAN
        st.title("🚌")
        st.subheader("전국 시도별 승합차 등록 현황 (단위: 대)")
        van_data = self.load_van_data()
        # 컬럼명 변경
        van_data.rename(
            columns={
                "district": "지역명",
                "gov_van": "관용 승합차",
                "private_van": "자가용 승합차",
                "commercial_van": "영업용 승합차",
                "total_van": "승합차 합계",
            },
            inplace=True,
        )
        # 특정 컬럼 제거
        van_data.drop(columns=["id", "region_id"], inplace=True)
        # 데이터 타입 확인 및 변환
        van_data["관용 승합차"] = pd.to_numeric(
            van_data["관용 승합차"], errors="coerce"
        )
        van_data["자가용 승합차"] = pd.to_numeric(
            van_data["자가용 승합차"], errors="coerce"
        )
        van_data["영업용 승합차"] = pd.to_numeric(
            van_data["영업용 승합차"], errors="coerce"
        )
        van_data["승합차 합계"] = pd.to_numeric(
            van_data["승합차 합계"], errors="coerce"
        )

        # 데이터 확인
        # st.write("데이터 타입 확인:", van_data.dtypes)

        # 쿼리 결과 테이블 뿌려주기
        st.table(van_data)

        # 막대 차트
        # st.subheader("영업용 승합차 수 (막대 차트)")
        # fig, ax = plt.subplots()
        # sns.barplot(x='지역명', y='승합차 합계', data=van_data, ax=ax)
        # plt.xticks(rotation=90)
        # st.pyplot(fig)

        ### TRUCK
        st.title("🚜")
        st.subheader("전국 시도별 화물차 등록 현황 (단위: 대)")
        truck_data = self.load_truck_data()
        # 컬럼명 변경
        truck_data.rename(
            columns={
                "district": "지역명",
                "gov_truck": "관용 화물차",
                "private_truck": "자가용 화물차",
                "commercial_truck": "영업용 화물차",
                "total_truck": "화물차 합계",
            },
            inplace=True,
        )
        # 특정 컬럼 제거
        truck_data.drop(columns=["id", "region_id"], inplace=True)
        # 쿼리 결과 테이블 뿌려주기
        st.table(truck_data)
        st.write("")
        st.write("")
        st.write("")
        ### SPECIAL VEHICLE
        st.title("🚕")
        st.subheader("전국 시도별 특수차 등록 현황 (단위: 대)")
        special_vehicle_data = self.load_special_vehicle_data()
        # 컬럼명 변경
        special_vehicle_data.rename(
            columns={
                "district": "지역명",
                "gov_special": "관용 특수차",
                "private_special": "자가용 특수차",
                "commercial_special": "영업용 특수차",
                "total_special": "특수차 합계",
            },
            inplace=True,
        )
        # 특정 컬럼 제거
        special_vehicle_data.drop(columns=["id", "region_id"], inplace=True)
        # 쿼리 결과 테이블 뿌려주기
        st.table(special_vehicle_data)

    ### FAQ 화면
    def show_faq_system(self):

        def get_image_base64(image_path):
            image = Image.open(image_path)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return img_str

        image_path = r"img/rent_img.png"

        html_code = '<div style="display: flex; flex-direction: column; align-items: flex-start;">'

        img_str = get_image_base64(image_path)
        html_code += (
            f'<img src="data:image/png;base64,{img_str}" style="margin-bottom: 10px;"/>'
        )

        html_code += "</div>"

        # Streamlit에서 HTML 코드 렌더링
        st.markdown(html_code, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="text-align: center;">
                <h2 style="font-size: 25px;">무엇을 도와드릴까요?<br></h2>
                <h2 style="font-size: 15px;">자주 찾는 질문을 모아봤어요<br></h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        faq_data = self.load_faq_data()
        # 페이지당 항목 수 설정
        items_per_page = 5

        # 총 페이지 수 계산
        total_pages = (len(faq_data) - 1) // items_per_page + 1

        # 선택된 페이지의 데이터만 표시
        start_idx = (st.session_state.faq_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_data = faq_data.iloc[start_idx:end_idx]

        # 페이지
        for index, row in page_data.iterrows():
            with st.expander(row["title"]):
                st.markdown("<hr>", unsafe_allow_html=True)
                st.write(row["content"])

        # 페이지 선택 버튼을 여러 줄로 배치하고 가운데 정렬
        cols_per_row = 10  # 한 줄에 배치할 버튼 수
        rows = (total_pages - 1) // cols_per_row + 1

        for row_num in range(rows):
            start_col = row_num * cols_per_row
            end_col = min(start_col + cols_per_row, total_pages)
            num_buttons = end_col - start_col

            # 가운데 정렬을 위해 빈 열 추가
            if num_buttons < cols_per_row:
                left_padding = (cols_per_row - num_buttons) // 2
                right_padding = cols_per_row - num_buttons - left_padding
                cols = st.columns(left_padding + num_buttons + right_padding)
                button_cols = cols[left_padding : left_padding + num_buttons]
            else:
                cols = st.columns(cols_per_row)
                button_cols = cols

            for i, col in enumerate(button_cols):
                if col.button(str(start_col + i + 1)):
                    st.session_state.faq_page = start_col + i + 1
                    st.experimental_rerun()

        st.write("")
        st.write("")
        st.markdown(
            f"""
            <div style="text-align: center;">
                <h2 style="font-size: 22px;"><br><br>더 자세한 상담이 필요하신가요?</h2>
            <div>
            """,
            unsafe_allow_html=True,
        )

        image_path = r"img/cs_num.png"

        html_code = '<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">'

        img_str = get_image_base64(image_path)
        html_code += (
            f'<img src="data:image/png;base64,{img_str}" style="margin-bottom: 10px;"/>'
        )

        html_code += "</div>"

        # Streamlit에서 HTML 코드 렌더링
        st.markdown(html_code, unsafe_allow_html=True)

    def run(self):
        if st.session_state.page == "HOME":
            self.home()
        elif st.session_state.page == "전국 자동차 등록현황":
            self.show_car_registration_status()
        elif st.session_state.page == "FAQ 조회시스템":
            self.show_faq_system()

        st.components.v1.html(scroll_script, height=0)

    def sum_total_car(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(total_car) FROM car;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def sum_total_special(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(total_special) FROM special_vehicle;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def sum_total_truck(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(total_truck) FROM truck;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def sum_total_van(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(total_van) FROM van;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    # 전체 관용 차량정보 수집
    def gov_total_car(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(gov_car) FROM car;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def gov_total_special(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(gov_special) FROM special_vehicle;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def gov_total_truck(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(gov_truck) FROM truck;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def gov_total_van(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(gov_van) FROM van;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    # 전국 영업용 자동차 등록 대수
    def com_total_car(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(commercial_car) FROM car;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def com_total_special(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(commercial_special) FROM special_vehicle;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def com_total_truck(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(commercial_truck) FROM truck;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def com_total_van(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(commercial_van) FROM van;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    # 전국 자가용 자동차 등록 대수
    def pri_total_car(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(private_car) FROM car;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def pri_total_special(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(private_special) FROM special_vehicle;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def pri_total_truck(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(private_truck) FROM truck;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def pri_total_van(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT SUM(private_van) FROM van;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    # 도시 리스트 가져오기
    def get_city_list(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT NAME FROM region;;"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    # 도시 차종별 대수 가져오기
    def get_citys_car_list(self, city_name):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = f"SELECT gov_car, commercial_car, private_car FROM car WHERE district = '{city_name}';"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def get_citys_special_list(self, city_name):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = f"SELECT gov_special, commercial_special, private_special FROM special_vehicle WHERE district = '{city_name}';"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def get_citys_truck_list(self, city_name):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = f"SELECT gov_truck, commercial_truck, private_truck FROM truck WHERE district = '{city_name}';"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def get_citys_van_list(self, city_name):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = f"SELECT gov_van, commercial_van, private_van FROM van WHERE district = '{city_name}';"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def load_car_data(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_car = "SELECT * FROM car"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def load_van_data(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_van = "SELECT * FROM van"
        with engine.connect() as connection:
            return pd.read_sql(query_van, connection)

    def load_truck_data(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_truck = "SELECT * FROM truck"
        with engine.connect() as connection:
            return pd.read_sql(query_truck, connection)

    def load_special_vehicle_data(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query_special_vehicle = "SELECT * FROM special_vehicle"
        with engine.connect() as connection:
            return pd.read_sql(query_special_vehicle, connection)

    def load_faq_data(self):
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_port = "3306"
        db_name = "scrawling"

        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        query = "SELECT * FROM faq"
        with engine.connect() as connection:
            return pd.read_sql(query, connection)
