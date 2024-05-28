from sqlalchemy import create_engine
import streamlit as st
from streamlit_option_menu import option_menu

import numpy as np
import pandas as pd

import datetime
from datetime import datetime as dt

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

class Ui:
    def __init__(self, appname):
               
        st.title(appname)
        
        # 페이지 상태 초기화
        if 'page' not in st.session_state:
            st.session_state.page = 'HOME'

        # 추가
        if "faq_page" not in st.session_state:
            st.session_state.faq_page = 1

        self.run()

    def home(self):
        # st.title("")
        # st.header("MENU")
        # menu = st.sidebar.selectbox("메뉴를 선택하세요", ["홈", "전국 자동차 등록현황", "FAQ 조회시스템"])
   
        # with st.sidebar:
        menu = option_menu(None, ["HOME", "전국 자동차 등록현황", "FAQ 조회시스템"],
                            icons=['house', 'kanban', 'list-task'],
                            menu_icon="app-indicator", default_index=0, orientation="horizontal",
                            styles={
                                "container": {"padding": "4!important", "background-color": "black"},
                                "icon": {"color": "white", "font-size": "25px"},                                
                                "nav-link": {"font-size": "16px", "color": "white", "text-align": "left", "margin":"0px", "--hover-color": "#00bcff5c"},
                                "nav-link-selected": {"background-color": "#00bcff5c"},
                            }
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
        car_data.rename(columns={
            'district': '지역명',
            'gov_car': '관용 승합차',
            'private_car': '자가용 승합차',
            'commercial_car': '영업용 승합차',
            'total_car': '승합차 합계'
        }, inplace=True)
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
        van_data.rename(columns={
            'district': '지역명',
            'gov_van': '관용 승합차',
            'private_van': '자가용 승합차',
            'commercial_van': '영업용 승합차',
            'total_van': '승합차 합계'
        }, inplace=True)
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
        truck_data.rename(columns={
            'district': '지역명',
            'gov_truck': '관용 화물차',
            'private_truck': '자가용 화물차',
            'commercial_truck': '영업용 화물차',
            'total_truck': '화물차 합계'
        }, inplace=True)
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
        special_vehicle_data.rename(columns={
            'district': '지역명',
            'gov_special': '관용 특수차',
            'private_special': '자가용 특수차',
            'commercial_special': '영업용 특수차',
            'total_special': '특수차 합계'
        }, inplace=True)
        # 특정 컬럼 제거
        special_vehicle_data.drop(columns=["id", "region_id"], inplace=True)
        # 쿼리 결과 테이블 뿌려주기
        st.table(special_vehicle_data)


        
    ### FAQ 화면
    def show_faq_system(self):
        st.title("FAQ 조회시스템")
        st.write("여기는 FAQ 조회시스템 화면입니다.")

        st.subheader("게시글 목록")

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
                button_cols = cols[left_padding:left_padding + num_buttons]
            else:
                cols = st.columns(cols_per_row)
                button_cols = cols

            for i, col in enumerate(button_cols):
                if col.button(str(start_col + i + 1)):
                    st.session_state.faq_page = start_col + i + 1
                    # 스크롤 위치 저장 자바스크립트 실행
                    st.components.v1.html("<script>saveScrollPos();</script>", height=0)
                    # 상태 업데이트 후 즉시 재로드
                    st.experimental_rerun()

    def run(self):
        if st.session_state.page == "HOME":
            self.home()
        elif st.session_state.page == "전국 자동차 등록현황":
            self.show_car_registration_status()
        elif st.session_state.page == "FAQ 조회시스템":
            self.show_faq_system()

        st.components.v1.html(scroll_script, height=0)


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

       
    ################################################################################################   
    #     여기서 부터는 기존 수업자료
    #     st.header("데이터를 보여드릴게요!:sparkles:")
    #     st.caption("이미지입니다.:sparkles:")
    #     sample_code = """
    #             def func01():
    #                 print("조회됨")

    #     """
    #     st.code(sample_code, language="python")
    #     st.text("제가 만들 모델은 이러이러하다")

    #     st.markdown("# 안녕하세요 마크다운 #1개 입니다")
        

    #     st.markdown("텍스트의 색상을 :green[초록색]으로, 그리고 :blue[파란색] 볼드체로 설정할수 있습니다.")
    #     st.markdown(":green[$\sqrt{x^2+y^2}=1$] 와 같이 latex 문법의 수식표현도 가능합니다.")
    #     st.latex(r"\sqrt{x^2+y^2}=1")

        


# <DATA 영역>
# 자료구조 말고 판다스가 제공하는 자료구조 : Series, DataFrame
# 사실상 Padas == DataFrame == Series 이어붙인것 == 넘파이의 nd.array 자료구조에 의존

# DataFrame == df == 엑셀처럼 '행'과 '열'로 구성
# 행(rows) : 가로
# 열(column) : 세로
# [행,열]
# 리스트의 경우 : [1행["홍길동", 45, ""]  2행["홍길동", 45, ""] ]
# 딕셔너리의 경우 :
# [
#      {"이름":"홍길동", "이름":"민경원"}, # Series : 엑셀 기준으로 같은 컬럼(자료타입)명 안에 있는 세로 묶음
#      {"이름":"홍길동", "나이":45}, # Series X
#      {"이름":"홍길동", "나이":45}, # Series X
#      {"이름":"홍길동", "나이":45}, # Series X
#      {"이름":"홍길동", "나이":45}, # Series X
# ]

        # st.title("데이터 프레임")        

        # dataframe = pd.DataFrame({
        #     "first column" : [1,2,3,4],
        #     "second column" : [10,20,30,40],
        # })

        # st.dataframe(dataframe, use_container_width=False) # 반응형 안됨, Interactive함

        # st.table(dataframe) # 반응형 됨

        # # 백터, 매트릭스, 텐서
        # st.metric(label="온도", value="10ºC", delta="1,2ºC")
        # st.metric(label="삼성전자", value="10ºC", delta="-1,200원")
        
        # col1, col2, col3 = st.columns(3)
        # col1.metric(label="삼성전자", value="77,000원", delta="-1,200원")
        # col2.metric(label="LG전자", value="63,000원", delta="1,200원")
        # col3.metric(label="대우전자", value="63,000원", delta="-1,200원")

        

        # button = st.button("눌러주세요")
        # button2 = st.button("되돌리기")
        # if button :
        #     st.write(":blue[버튼이 눌렸습니다]:sparkles:")
        # if button2 :
        #     pass

        # # 파일 다운로드
        # # 샘플 데이터

        # st.download_button(
        #     label='csv로 다운로드',
        #     data=dataframe.to_csv(), 
        #     file_name="sample.txt",
        #     mime="text/csv"
        # )

        # agree = st.checkbox("동의?")

        # if agree :
        #     st.write("감사합니다!:100:")

        # mbti = st.radio("라디오 버튼 제목", ("ESTJ", "ISTJ"), index=1) # index 옵션은 default로 선택되어 있는 것

        # mbti2 = st.selectbox("mbti는?", ("ISTJ", "ESTJ"))
        
        # mbti3 = st.multiselect("mbti는?(복수선택가능)", ("ISTJ", "ESTJ"))
        # print(mbti3)

        # values = st.slider(
        #     "슬라이더 범위를 선택해주세요",
        #     0.0, 100.0, (25.0, 75.0)
        # )

        # start_time = st.slider(
        #     "언제 약속을 잡는 것이 좋을까요? (슬라이더를 움직여서 시간을 선택하세요)",
        #     min_value=dt(2020, 1, 1, 0, 0),
        #     max_value=dt(2020, 1, 7, 23, 0),
        #     value=dt(2020, 1, 3, 12, 0),
        #     step=datetime.timedelta(hours=1),
        #     format="MM/DD/YY - HH:mm")
        
        # st.write("선택한 약속 시간: ", start_time)

        # title = st.text_input(label="나이입력", placeholder=20)
        # title = st.number_input(label="나이입력", min_value=0, max_value=100, placeholder=20, step=1, value=20)

        

