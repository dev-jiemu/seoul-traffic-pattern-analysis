#!/usr/bin/env python3

import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data_collection.topis_data_collector import TopisDataCollector


def main():
    """
    메인 실행 함수
    """
    print("🚗 TOPIS 실시간 도로 속도 데이터 수집기")
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
    collector = TopisDataCollector(api_key)

    print("\n" + "=" * 50)
    print("💡 안내사항")
    print("=" * 50)
    print("• TOPIS 실시간 도로 속도 정보를 수집합니다.")
    print("• 이 데이터는 현재 시점의 도로 소통 상황을 나타냅니다.")
    print("• 데이터는 '실시간'으로 제공되며, 특정 과거 시점을 조회하는 기능은 지원하지 않습니다.")
    print()


    print("\n" + "=" * 50)
    print("📊 수집 정보")
    print("=" * 50)
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
    df = collector.get_road_speed_data()

    # 결과 확인
    if df is not None:
        print("\n" + "=" * 50)
        print("✅ 데이터 수집 성공!")
        print("=" * 50)

        # 간단한 데이터 탐색
        if not df.empty:
            print(f"🔍 데이터 크기: {df.shape[0]:,}행 × {df.shape[1]}열")
            print(f"\n📋 컬럼 목록:")
            for i, col in enumerate(df.columns):
                print(f"   {i+1}. {col}")

            print(f"\n📋 샘플 데이터 (처음 3행):")
            print(df.head(3).to_string())

    else:
        print("\n" + "=" * 50)
        print("❌ 데이터 수집 실패")
        print("=" * 50)

if __name__ == "__main__":
    main()
