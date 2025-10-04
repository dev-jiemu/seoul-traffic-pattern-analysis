#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timedelta

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data_collection.seoul_subway_data_collector import SeoulSubwayDataCollector


def main():
    """
    메인 실행 함수
    """
    print("🚇 서울시 지하철 승하차 데이터 수집기")
    print("=" * 50)

    # 환경변수에서 API 키 가져오기
    api_key = os.getenv("SEOUL_API_KEY")

    if not api_key:
        print("❌ API 키가 설정되지 않았습니다.")
        print("💡 터미널에서 다음 명령어를 실행하세요:")
        print("   export SEOUL_API_KEY='여기에_API_키_입력'")
        return

    # 데이터 수집기 초기화
    collector = SeoulSubwayDataCollector(api_key)

    # 수집할 기간 설정 (최근 1주일)
    end_date = datetime.now() - timedelta(days=3)  # 3일전까지 (데이터 갱신 지연 고려)
    start_date = end_date - timedelta(days=7)  # 1주일치

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    print(f"📅 수집 기간: {start_date_str} ~ {end_date_str}")

    # 데이터 수집
    df = collector.get_subway_hourly_data(start_date_str, end_date_str)

    # 데이터 구조 탐색
    if df is not None:
        collector.explore_data_structure(df)


if __name__ == "__main__":
    main()#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timedelta

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data_collection.seoul_subway_data_collector import SeoulSubwayDataCollector


def main():
    """
    메인 실행 함수
    """
    print("🚇 서울시 지하철 승하차 데이터 수집기")
    print("=" * 50)

    # 환경변수에서 API 키 가져오기
    api_key = os.getenv("SEOUL_API_KEY")

    if not api_key:
        print("❌ API 키가 설정되지 않았습니다.")
        print("💡 터미널에서 다음 명령어를 실행하세요:")
        print("   export SEOUL_API_KEY='여기에_API_키_입력'")
        return

    # 데이터 수집기 초기화
    collector = SeoulSubwayDataCollector(api_key)

    # 수집할 기간 설정 (최근 1주일)
    end_date = datetime.now() - timedelta(days=3)  # 3일전까지 (데이터 갱신 지연 고려)
    start_date = end_date - timedelta(days=7)  # 1주일치

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    print(f"📅 수집 기간: {start_date_str} ~ {end_date_str}")

    # 데이터 수집
    df = collector.get_subway_hourly_data(start_date_str, end_date_str)

    # 데이터 구조 탐색
    if df is not None:
        collector.explore_data_structure(df)


if __name__ == "__main__":
    main()