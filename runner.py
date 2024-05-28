from helpers.car_crawling import car_crawling
from helpers.db import insert_db
from helpers.faq_crawling import faq_crawling
from helpers.ui import Ui
from streamlit.web.cli import main


if __name__ == "__main__":

    ### 01 WEB CRAWLING :  통계청 KOSIS 공유서비스 OPEN API + Selenium
    # car_crawling.py
    # faq_crawler.py

    # 02 DB 작업
    # db.py

    # 03 스트림릿 클래스
    # ui.py
    # car_crawling()
    # faq_crawling()
    # insert_db()

    Ui("전국 자동차 등록 현황과 렌터카 FAQ 한 눈에 보기 👀")
