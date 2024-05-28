from sqlalchemy import create_engine
import streamlit as st
from streamlit_option_menu import option_menu

import numpy as np
import pandas as pd

import datetime
from datetime import datetime as dt

from PIL import Image
import base64
from io import BytesIO

db_user = "root"
db_password = "1234"
db_host = "localhost"
db_port = "3306"
db_name = "scrawling"

engine = create_engine(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)


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
        # st.title("")
        # st.header("MENU")
        # menu = st.sidebar.selectbox("메뉴를 선택하세요", ["홈", "전국 자동차 등록현황", "FAQ 조회시스템"])

        # with st.sidebar:
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

    def show_home(self):
        st.title("HOME")
        st.markdown("### 여기는 HOME 화면입니다.")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("Contributors 소개 코드")
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
                print("저희 6팀 프로젝트의 기여자는 " + contributors + "입니다." )
        """
        st.code(sample_code, language="python")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.subheader("게시글 작성")
        title = st.text_input("제목", key="home_text_title")
        content = st.text_area("내용", key="home_text_content")

        if st.button("작성", key="home_submit"):
            st.subheader("게시글 목록")
            st.write("제목:", title)
            st.write("내용:", content)
            st.success("게시글이 HOME 화면에 작성되었습니다.")

        st.subheader("게시글 목록")

    ### 전국 자동차 등록 현황
    def show_car_registration_status(self):
        st.title("전국 자동차 등록 현황")
        st.write("출처 : 통계청 KOSIS 공유서비스 OPEN API 데이터")
        st.write("")
        st.write("")
        st.write("")
        # CAR
        st.title("🚗")
        st.subheader("전국 시도별 승용차 등록 현황 (단위: 대)")
        car_data = self.load_car_data()
        # 컬럼명 변경
        car_data.rename(
            columns={
                "district": "지역명",
                "gov_car": "관용 승합차",
                "private_car": "자가용 승합차",
                "commercial_car": "영업용 승합차",
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
        # VAN
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
        # 쿼리 결과 테이블 뿌려주기
        st.table(van_data)
        st.write("")
        st.write("")
        st.write("")
        # TRUCK
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
        # SPECIAL VEHICLE
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

    def load_car_data(self):
        query_car = "SELECT * FROM car"
        with engine.connect() as connection:
            return pd.read_sql(query_car, connection)

    def load_van_data(self):
        query_van = "SELECT * FROM van"
        with engine.connect() as connection:
            return pd.read_sql(query_van, connection)

    def load_truck_data(self):
        query_truck = "SELECT * FROM truck"
        with engine.connect() as connection:
            return pd.read_sql(query_truck, connection)

    def load_special_vehicle_data(self):
        query_special_vehicle = "SELECT * FROM special_vehicle"
        with engine.connect() as connection:
            return pd.read_sql(query_special_vehicle, connection)

    def load_faq_data(self):
        query = "SELECT * FROM faq"
        with engine.connect() as connection:
            return pd.read_sql(query, connection)
