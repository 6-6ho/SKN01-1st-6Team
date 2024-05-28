"""
SK 렌터카 FAQ 크롤러

robot.txt 내용

User-agent: *
Allow: /

"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter


def faq_crawling():
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(level.levelname)s - %(message)s"
    )

    # 크롬 드라이버 설정
    driver = webdriver.Chrome()
    driver.get("https://homepage.skcarrental.com/customer/faq")

    # 데이터 저장 리스트
    faq_data = []

    # 페이지 번호에 해당하는 버튼 클릭 함수
    def click_page(page_number):
        try:
            page_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//button[text()='{page_number}']")
                )
            )
            driver.execute_script("arguments[0].click();", page_button)
            time.sleep(2)  # 페이지 로딩 대기
        except Exception as e:
            logging.error(f"페이지 {page_number}로 이동 실패: {e}")

    # FAQ 데이터 수집 함수
    def collect_faq_data():
        while True:
            try:
                branch_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "branch_wrap"))
                )
                logging.info(
                    f"branch_elements : {len(branch_elements)}"
                )  # 요소 개수 로그

                for i in range(len(branch_elements)):
                    branch_elements = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, "branch_wrap")
                        )
                    )
                    branch = branch_elements[i]
                    try:
                        driver.execute_script("arguments[0].click();", branch)
                        time.sleep(2)  # 페이지 로딩 대기

                        title_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.CLASS_NAME, "board_title")
                            )
                        )

                        content_elements = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located(
                                (By.CLASS_NAME, "board_contents p")
                            )
                        )

                        title = title_element.text.strip()
                        content = "\n".join(
                            [element.text.strip() for element in content_elements]
                        )

                        # '☞' 이후의 내용 제거
                        content = content.split("☞")[0].strip()

                        faq_data.append({"Title": title, "Content": content})

                        driver.back()
                        time.sleep(2)  # 페이지 로딩 대기
                    except Exception as e:
                        logging.error(f"데이터 수집 실패: {e}")
                break  # 모든 branch 요소를 처리한 후 while 루프 탈출
            except Exception as e:
                logging.error(f"branch_wrap 요소 로딩 실패: {e}")
                break

    # 페이지 순회하며 데이터 수집
    for page_number in range(1, 5):
        click_page(page_number)
        collect_faq_data()

    # 수집한 데이터를 XLSX 파일로 저장
    xlsx_file_path = (
        r"C:\Users\minkw\Desktop\workspace01\crawling_project\data\faq_data.xlsx"
    )

    workbook = xlsxwriter.Workbook(xlsx_file_path)
    worksheet = workbook.add_worksheet()

    # 열 제목 작성
    worksheet.write("A1", "Title")
    worksheet.write("B1", "Content")

    # 데이터 작성
    for row_num, data in enumerate(faq_data, 1):
        worksheet.write(row_num, 0, data["Title"])
        worksheet.write(row_num, 1, data["Content"])

    workbook.close()
    driver.quit()

    print("Data saved successfully into the XLSX file.")
