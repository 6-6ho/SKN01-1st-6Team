import pandas as pd
from sqlalchemy import create_engine, text


def insert_db():
    # 엑셀 파일 경로
    region_table_xlsx_file_path = (
        r"C:\Users\minkw\Desktop\workspace01\crawling_project\data\region_table.xlsx"
    )
    df_region = pd.read_excel(region_table_xlsx_file_path, engine="openpyxl")

    car_table_xlsx_file_path = (
        r"C:\Users\minkw\Desktop\workspace01\crawling_project\data\car_table.xlsx"
    )
    df_car = pd.read_excel(car_table_xlsx_file_path, engine="openpyxl")

    van_table_xlsx_file_path = (
        r"C:\Users\minkw\Desktop\workspace01\crawling_project\data\van_table.xlsx"
    )
    df_van = pd.read_excel(van_table_xlsx_file_path, engine="openpyxl")

    truck_table_xlsx_file_path = (
        r"C:\Users\minkw\Desktop\workspace01\crawling_project\data\truck_table.xlsx"
    )
    df_truck = pd.read_excel(truck_table_xlsx_file_path, engine="openpyxl")

    special_vehicle_table_xlsx_file_path = r"C:\Users\minkw\Desktop\workspace01\crawling_project\data\special_vehicle_table.xlsx"
    df_special_vehicle = pd.read_excel(
        special_vehicle_table_xlsx_file_path, engine="openpyxl"
    )

    faq_data_xlsx_file_path = (
        r"C:\Users\minkw\Desktop\workspace01\crawling_project\data\faq_data.xlsx"
    )
    df_faq = pd.read_excel(faq_data_xlsx_file_path, engine="openpyxl")

    # 필요 없는 'Unnamed: 0' 열 제거
    if "Unnamed: 0" in df_region.columns:
        df_region = df_region.drop(columns=["Unnamed: 0"])

    if "Unnamed: 0" in df_car.columns:
        df_car = df_car.drop(columns=["Unnamed: 0"])

    if "Unnamed: 0" in df_van.columns:
        df_van = df_van.drop(columns=["Unnamed: 0"])

    if "Unnamed: 0" in df_truck.columns:
        df_truck = df_truck.drop(columns=["Unnamed: 0"])

    if "Unnamed: 0" in df_special_vehicle.columns:
        df_special_vehicle = df_special_vehicle.drop(columns=["Unnamed: 0"])

    # MySQL 연결 설정
    db_user = "root"
    db_password = ""
    db_host = "localhost"
    db_port = "3306"
    db_name = "scrawling"

    # SQLAlchemy 엔진 생성 (데이터베이스 생성 전용)
    create_engine_without_db = create_engine(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}"
    )

    # 데이터베이스 생성
    with create_engine_without_db.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name};"))

    # SQLAlchemy 엔진 생성
    engine = create_engine(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    try:
        with engine.connect() as connection:
            connection.execute(text("USE scrawling;"))
            connection.execute(
                text("DROP TABLE IF EXISTS car, van, truck, special_vehicle;")
            )
            connection.execute(text("DROP TABLE IF EXISTS region;"))
            connection.execute(text("DROP TABLE IF EXISTS faq;"))

            create_region_table_query = """
            CREATE TABLE IF NOT EXISTS region (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            );
            """

            create_car_table_query = """
            CREATE TABLE IF NOT EXISTS car (
                id INT AUTO_INCREMENT PRIMARY KEY,
                region_id INT,
                district VARCHAR(50),
                gov_car VARCHAR(50),
                private_car VARCHAR(50),
                commercial_car VARCHAR(50),
                total_car VARCHAR(50),
                FOREIGN KEY (region_id) REFERENCES region(id)
            );
            """

            create_van_table_query = """
            CREATE TABLE IF NOT EXISTS van (
                id INT AUTO_INCREMENT PRIMARY KEY,
                region_id INT,
                district VARCHAR(50),
                gov_van VARCHAR(50),
                private_van VARCHAR(50),
                commercial_van VARCHAR(50),
                total_van VARCHAR(50),
                FOREIGN KEY (region_id) REFERENCES region(id)
            );
            """

            create_truck_table_query = """
            CREATE TABLE IF NOT EXISTS truck (
                id INT AUTO_INCREMENT PRIMARY KEY,
                region_id INT,
                district VARCHAR(50),
                gov_truck VARCHAR(50),
                private_truck VARCHAR(50),
                commercial_truck VARCHAR(50),
                total_truck VARCHAR(50),
                FOREIGN KEY (region_id) REFERENCES region(id)
            );
            """

            create_special_vehicle_table_query = """
            CREATE TABLE IF NOT EXISTS special_vehicle (
                id INT AUTO_INCREMENT PRIMARY KEY,
                region_id INT,
                district VARCHAR(50),
                gov_special VARCHAR(50),
                private_special VARCHAR(50),
                commercial_special VARCHAR(50),
                total_special VARCHAR(50),
                FOREIGN KEY (region_id) REFERENCES region(id)
            );
            """

            create_faq_table_query = """
            CREATE TABLE IF NOT EXISTS faq (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            );
            """

            connection.execute(text(create_region_table_query))
            connection.execute(text(create_car_table_query))
            connection.execute(text(create_van_table_query))
            connection.execute(text(create_truck_table_query))
            connection.execute(text(create_special_vehicle_table_query))
            connection.execute(text(create_faq_table_query))

            # 데이터 삽입 시도
            df_region.to_sql(
                "region", con=engine, index=False, if_exists="append", method="multi"
            )
            df_car.to_sql(
                "car", con=engine, index=False, if_exists="append", method="multi"
            )
            df_van.to_sql(
                "van", con=engine, index=False, if_exists="append", method="multi"
            )
            df_truck.to_sql(
                "truck", con=engine, index=False, if_exists="append", method="multi"
            )
            df_special_vehicle.to_sql(
                "special_vehicle",
                con=engine,
                index=False,
                if_exists="append",
                method="multi",
            )
            df_faq.to_sql(
                "faq", con=engine, index=False, if_exists="append", method="multi"
            )

    except Exception as e:
        print(f"An error occurred: {e}")

    # engine.dispose()를 사용하여 연결 닫기
    engine.dispose()
