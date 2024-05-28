# 통계청 KOSIS OPEN API 이용

# https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=ZGY3YjAzMmVhYTM1NTY2ZjVjOTdkZjBkM2VkMzM2YzU=&itmId=13103873443T1+13103873443T2+13103873443T3+13103873443T4+&objL1=ALL&objL2=13102873443B.0002+&objL3=ALL&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&newEstPrdCnt=1&outputFields=TBL_NM+NM+ITM_NM+&orgId=116&tblId=DT_MLTM_5498

import requests
import pandas as pd
import os


def car_crawling():
    # OPEN API에서 데이터 가져오기
    url = "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=ZGY3YjAzMmVhYTM1NTY2ZjVjOTdkZjBkM2VkMzM2YzU=&itmId=13103873443T1+13103873443T2+13103873443T3+13103873443T4+&objL1=ALL&objL2=13102873443B.0002+&objL3=ALL&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&newEstPrdCnt=1&outputFields=TBL_NM+NM+ITM_NM+&orgId=116&tblId=DT_MLTM_5498"
    response = requests.get(url)
    data = response.json()
    #  print(data)

    # 엑셀 저장 경로 생성
    if not os.path.exists(r"../data"):
        os.mkdir(r"../data")
        print("Storage dir is not exists... Makeing dir...")
    else:
        print("storage dir is alread exists!")

    # 상태코드 확인
    print(" 상태 코드 : ", response.status_code)
    print()

    # 변수 저장 : 테이블 칼럼 리스트
    region_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    region_name = [
        item["C1_NM"]
        for item in data
        if item["ITM_NM"] == "관용" and item["C3_NM"] == "승용"
    ]
    print("지역명 : ", region_name)

    승용차지역 = [
        item["C1_NM"]
        for item in data
        if item["ITM_NM"] == "관용" and item["C3_NM"] == "승용"
    ]
    print("승용차지역 : ", 승용차지역)
    승용차관용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "관용" and item["C3_NM"] == "승용"
    ]
    print("승용차관용 : ", 승용차관용)
    승용차자가용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "자가용" and item["C3_NM"] == "승용"
    ]
    print("승용차자가용 : ", 승용차자가용)
    승용차영업용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "영업용" and item["C3_NM"] == "승용"
    ]
    print("승용차영업용 : ", 승용차영업용)
    승용차계 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "계" and item["C3_NM"] == "승용"
    ]
    print("승용차계 : ", 승용차계)
    print()

    승합차지역 = [
        item["C1_NM"]
        for item in data
        if item["ITM_NM"] == "관용" and item["C3_NM"] == "승합"
    ]
    print("승합차지역 : ", 승합차지역)
    승합차관용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "관용" and item["C3_NM"] == "승합"
    ]
    print("승합차관용 : ", 승합차관용)
    승합차자가용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "자가용" and item["C3_NM"] == "승합"
    ]
    print("승합차자가용 : ", 승합차자가용)
    승합차영업용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "영업용" and item["C3_NM"] == "승합"
    ]
    print("승합차영업용 : ", 승합차영업용)
    승합차계 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "계" and item["C3_NM"] == "승합"
    ]
    print("승합차계 : ", 승합차계)
    print()

    화물차지역 = [
        item["C1_NM"]
        for item in data
        if item["ITM_NM"] == "관용" and item["C3_NM"] == "화물"
    ]
    print("화물차지역 : ", 화물차지역)
    화물차관용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "관용" and item["C3_NM"] == "화물"
    ]
    print("화물차관용 : ", 화물차관용)
    화물차자가용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "자가용" and item["C3_NM"] == "화물"
    ]
    print("화물차자가용 : ", 화물차자가용)
    화물차영업용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "영업용" and item["C3_NM"] == "화물"
    ]
    print("화물차영업용 : ", 화물차영업용)
    화물차계 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "계" and item["C3_NM"] == "화물"
    ]
    print("화물차계 : ", 화물차계)
    print()

    특수차지역 = [
        item["C1_NM"]
        for item in data
        if item["ITM_NM"] == "관용" and item["C3_NM"] == "특수"
    ]
    print("특수차지역 : ", 특수차지역)
    특수차관용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "관용" and item["C3_NM"] == "특수"
    ]
    print("특수차관용 : ", 특수차관용)
    특수차자가용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "자가용" and item["C3_NM"] == "특수"
    ]
    print("특수차자가용 : ", 특수차자가용)
    특수차영업용 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "영업용" and item["C3_NM"] == "특수"
    ]
    print("특수차영업용 : ", 특수차영업용)
    특수차계 = [
        item["DT"]
        for item in data
        if item["ITM_NM"] == "계" and item["C3_NM"] == "특수"
    ]
    print("특수차계 : ", 특수차계)
    print()
    print("데이터 타입 : ", type(특수차계[0]))

    # data 디렉토리에 파일 떨구기
    df_region = pd.DataFrame(
        zip(region_id, region_name),
        columns=["id", "name"],
    )
    df_region.to_excel(r"../data/region_table.xlsx", engine="openpyxl")

    df_car = pd.DataFrame(
        zip(region_id, 승용차지역, 승용차관용, 승용차자가용, 승용차영업용, 승용차계),
        columns=[
            "region_id",
            "district",
            "gov_car",
            "private_car",
            "commercial_car",
            "total_car",
        ],
    )
    df_car.to_excel(r"../data/car_table.xlsx", engine="openpyxl")

    df_van = pd.DataFrame(
        zip(region_id, 승합차지역, 승합차관용, 승합차자가용, 승합차영업용, 승합차계),
        columns=[
            "region_id",
            "district",
            "gov_van",
            "private_van",
            "commercial_van",
            "total_van",
        ],
    )
    df_van.to_excel(r"../data/van_table.xlsx", engine="openpyxl")

    df_truck = pd.DataFrame(
        zip(region_id, 화물차지역, 화물차관용, 화물차자가용, 화물차영업용, 화물차계),
        columns=[
            "region_id",
            "district",
            "gov_truck",
            "private_truck",
            "commercial_truck",
            "total_truck",
        ],
    )
    df_truck.to_excel(r"../data/truck_table.xlsx", engine="openpyxl")

    df_special = pd.DataFrame(
        zip(region_id, 특수차지역, 특수차관용, 특수차자가용, 특수차영업용, 특수차계),
        columns=[
            "region_id",
            "district",
            "gov_special",
            "private_special",
            "commercial_special",
            "total_special",
        ],
    )
    df_special.to_excel(r"../data/special_vehicle_table.xlsx", engine="openpyxl")
