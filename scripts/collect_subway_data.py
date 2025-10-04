#!/usr/bin/env python3

import sys
import os
from datetime import datetime, timedelta

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data_collection.seoul_subway_data_collector import SeoulSubwayDataCollector


def get_year_month_input(prompt, default_ym=None):
    """
    년월 입력받기 (YYYY-MM 형식)
    """
    while True:
        if default_ym:
            user_input = input(f"{prompt} (기본값: {default_ym}, Enter로 건너뛰기): ").strip()
            if not user_input:
                return default_ym
        else:
            user_input = input(f"{prompt}: ").strip()

        try:
            # 날짜 형식 검증
            datetime.strptime(user_input, "%Y-%m")
            return user_input
        except ValueError:
            print("❌ 잘못된 형식입니다. YYYY-MM 형식으로 입력하세요. (예: 2024-08)")


def main():
    """
    메인 실행 함수
    """
    print("🚇 서울시 지하철 승하차 데이터 수집기")
    print("=" * 50)

    # API 키 환경변수에서 가져오기
    api_key = os.getenv("SEOUL_API_KEY")

    if not api_key:
        print("❌ API 키가 설정되지 않았습니다.")
        print("💡 터미널에서 다음 명령어를 실행하세요:")
        print("   export SEOUL_API_KEY='여기에_API_키_입력'")
        return

    print("✅ API 키 확인 완료")

    # 데이터 수집기 초기화
    collector = SeoulSubwayDataCollector(api_key)

    print("\n" + "=" * 50)
    print("💡 안내사항")
    print("=" * 50)
    print("• 서울 열린데이터광장은 매달 5일에 전달 데이터를 갱신합니다.")
    print("• 예: 10월 5일에 9월 데이터가 업데이트됩니다.")
    print("• 데이터는 '월' 단위로 제공됩니다.")
    print()

    # 추천 년월 계산 (전전달)
    today = datetime.now()
    # 2달 전 데이터 추천 (안전하게)
    recommended_date = today - timedelta(days=60)
    recommended_ym = recommended_date.strftime("%Y-%m")

    print(f"📅 추천 년월: {recommended_ym} ({recommended_date.strftime('%Y년 %m월')})")
    print()

    # 수집 모드 선택
    print("수집 모드를 선택하세요:")
    print("  1. 추천 년월로 수집 (빠른 시작)")
    print("  2. 직접 년월 입력")

    mode = input("\n선택 (1/2): ").strip()

    if mode == "1":
        # 추천 년월 사용
        year_month = recommended_ym
        print(f"\n✅ 추천 년월 선택: {year_month}")

    elif mode == "2":
        # 직접 입력
        print("\n📅 수집할 년월을 입력하세요:")
        year_month = get_year_month_input("   년월 (YYYY-MM)")

    else:
        print("❌ 잘못된 선택입니다.")
        return

    print("\n" + "=" * 50)
    print("📊 수집 정보")
    print("=" * 50)
    print(f"📅 년월: {year_month}")
    print(f"💾 저장 경로: data/raw/")
    print()

    # 최종 확인
    confirm = input("수집을 시작하시겠습니까? (y/n): ").strip().lower()

    if confirm != 'y':
        print("❌ 수집이 취소되었습니다.")
        return

    print("\n🚀 데이터 수집 시작...")
    print("=" * 50)

    # 데이터 수집
    df = collector.get_subway_monthly_data(year_month)

    # 결과 확인
    if df is not None:
        print("\n" + "=" * 50)
        print("✅ 데이터 수집 성공!")
        print("=" * 50)
        collector.explore_data_structure(df)

        print("\n💡 다음 단계:")
        print("   python scripts/analyze_patterns.py  # 패턴 분석 실행")
    else:
        print("\n" + "=" * 50)
        print("❌ 데이터 수집 실패")
        print("=" * 50)
        print("\n💡 문제 해결:")
        print("   1. API 키가 올바른지 확인하세요")
        print("   2. 더 이전 년월로 시도해보세요 (예: 2024-08)")
        print("   3. 서울 열린데이터광장에서 데이터 제공 여부를 확인하세요")
        print("      → https://data.seoul.go.kr")


if __name__ == "__main__":
    main()