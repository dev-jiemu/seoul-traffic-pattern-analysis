#!/usr/bin/env python3
"""
서울시 지하철 패턴 분석 실행 스크립트
"""

import sys
import os
from glob import glob

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.analysis.subway_pattern_analyzer import SubwayPatternAnalyzer


def find_latest_data_file(data_path="data/raw/"):
    """
    가장 최근 데이터 파일 찾기
    """
    pattern = os.path.join(data_path, "subway_hourly_*.csv")
    files = glob(pattern)
    
    if not files:
        return None
    
    # 파일명으로 정렬하여 가장 최근 파일 반환
    latest_file = sorted(files)[-1]
    return latest_file


def main():
    """
    메인 실행 함수
    """
    print("📊 서울시 지하철 패턴 분석기")
    print("=" * 60)
    
    # 데이터 파일 찾기
    print("\n🔍 데이터 파일 검색 중...")
    
    data_file = find_latest_data_file()
    
    if not data_file:
        print("\n❌ 데이터 파일을 찾을 수 없습니다.")
        print("\n💡 다음 순서로 진행하세요:")
        print("   1. python scripts/collect_subway_data.py  # 데이터 수집")
        print("   2. python scripts/analyze_patterns.py     # 패턴 분석")
        return
    
    print(f"✅ 데이터 파일 발견: {data_file}")
    
    # 사용자 확인
    print("\n" + "=" * 60)
    print("분석 옵션을 선택하세요:")
    print("  1. 빠른 분석 (기본 통계만)")
    print("  2. 상세 분석 (시간대/요일별 패턴)")
    print("  3. 전체 분석 (역별 특성 포함)")
    print("  4. 종합 보고서 생성 (CSV 파일 저장)")
    
    choice = input("\n선택 (1-4): ").strip()
    
    # 분석기 초기화
    analyzer = SubwayPatternAnalyzer(data_file)
    
    # 데이터 로드
    print("\n" + "=" * 60)
    analyzer.load_data()
    
    # 전처리
    analyzer.preprocess_data()
    
    # 선택에 따른 분석 실행
    print("\n" + "=" * 60)
    
    if choice == "1":
        print("🚀 빠른 분석 실행 중...\n")
        analyzer.analyze_basic_stats()
        
    elif choice == "2":
        print("🚀 상세 분석 실행 중...\n")
        analyzer.analyze_basic_stats()
        analyzer.analyze_time_pattern()
        analyzer.analyze_weekday_pattern()
        
    elif choice == "3":
        print("🚀 전체 분석 실행 중...\n")
        analyzer.analyze_basic_stats()
        analyzer.analyze_time_pattern()
        analyzer.analyze_weekday_pattern()
        analyzer.analyze_station_characteristics(top_n=20)
        
    elif choice == "4":
        print("🚀 종합 보고서 생성 중...\n")
        results = analyzer.generate_summary_report()
        
    else:
        print("❌ 잘못된 선택입니다.")
        return
    
    print("\n" + "=" * 60)
    print("✅ 분석 완료!")
    print("=" * 60)
    
    if choice != "4":
        print("\n💡 다음 단계:")
        print("   python scripts/visualize_patterns.py  # 시각화 생성")


if __name__ == "__main__":
    main()
