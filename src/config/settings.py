import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 설정
SEOUL_OPEN_DATA_API_KEY = os.getenv('SEOUL_OPEN_DATA_API_KEY')
SEOUL_OPEN_DATA_BASE_URL = "http://openapi.seoul.go.kr:8088"

# 데이터 저장 경로
DATA_RAW_PATH = "data/raw/"
DATA_PROCESSED_PATH = "data/processed/"

# API 호출 설정
API_REQUEST_DELAY = 0.1  # 초
API_TIMEOUT = 30  # 초
MAX_RECORDS_PER_REQUEST = 1000

# 지하철 노선 정보
SUBWAY_LINES = {
    "1호선": "1",
    "2호선": "2", 
    "3호선": "3",
    "4호선": "4",
    "5호선": "5",
    "6호선": "6",
    "7호선": "7",
    "8호선": "8",
    "9호선": "9"
}
