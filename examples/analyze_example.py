#!/usr/bin/env python3
"""
지하철 패턴 분석 예제 코드
"""

import sys
import os

# 프로젝트 루트 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.analysis.subway_pattern_analyzer import SubwayPatternAnalyzer


def example_basic_analysis():
    """
    예제 1: 기본 통계 분석
    """
    print("=" * 70)
    print("예제 1: 기본 통계 분석")
    print("=" * 70)
    
    # 데이터 파일 경로 (실제 파일로 교체하세요)
    data_file = "data/raw/subway_hourly_2024-08.csv"
    
    # 분석기 생성
    analyzer = SubwayPatternAnalyzer(data_file)
    
    # 데이터 로드 및 전처리
    analyzer.load_data()
    analyzer.preprocess_data()
    
    # 기본 통계 분석
    analyzer.analyze_basic_stats()


def example_time_analysis():
    """
    예제 2: 시간대별 패턴 분석
    """
    print("\n" + "=" * 70)
    print("예제 2: 시간대별 패턴 분석")
    print("=" * 70)
    
    data_file = "data/raw/subway_hourly_2024-08.csv"
    
    analyzer = SubwayPatternAnalyzer(data_file)
    analyzer.load_data()
    analyzer.preprocess_data()
    
    # 시간대별 분석
    hourly_df = analyzer.analyze_time_pattern()
    
    # 결과 데이터프레임 활용 가능
    if hourly_df is not None:
        print("\n💡 피크 시간대 (TOP 3):")
        top3 = hourly_df.nlargest(3, 'TOTAL')
        for _, row in top3.iterrows():
            print(f"   {row['TIME']}: {row['TOTAL']:,}명")


def example_weekday_analysis():
    """
    예제 3: 요일별 패턴 분석
    """
    print("\n" + "=" * 70)
    print("예제 3: 요일별 패턴 분석")
    print("=" * 70)
    
    data_file = "data/raw/subway_hourly_2024-08.csv"
    
    analyzer = SubwayPatternAnalyzer(data_file)
    analyzer.load_data()
    analyzer.preprocess_data()
    
    # 요일별 분석
    weekday_df = analyzer.analyze_weekday_pattern()


def example_station_analysis():
    """
    예제 4: 역별 특성 분석
    """
    print("\n" + "=" * 70)
    print("예제 4: 역별 특성 분석")
    print("=" * 70)
    
    data_file = "data/raw/subway_hourly_2024-08.csv"
    
    analyzer = SubwayPatternAnalyzer(data_file)
    analyzer.load_data()
    analyzer.preprocess_data()
    
    # 역별 특성 분석 (TOP 15개 역)
    station_df = analyzer.analyze_station_characteristics(top_n=15)


def example_full_report():
    """
    예제 5: 종합 보고서 생성
    """
    print("\n" + "=" * 70)
    print("예제 5: 종합 보고서 생성")
    print("=" * 70)
    
    data_file = "data/raw/subway_hourly_2024-08.csv"
    
    analyzer = SubwayPatternAnalyzer(data_file)
    analyzer.load_data()
    analyzer.preprocess_data()
    
    # 종합 보고서 생성
    results = analyzer.generate_summary_report(save_path="results/")
    
    print("\n💡 분석 결과가 results/ 폴더에 저장되었습니다!")


if __name__ == "__main__":
    print("🚇 서울시 지하철 패턴 분석 예제 모음\n")
    
    # 실행할 예제 선택
    print("실행할 예제를 선택하세요:")
    print("  1. 기본 통계 분석")
    print("  2. 시간대별 패턴 분석")
    print("  3. 요일별 패턴 분석")
    print("  4. 역별 특성 분석")
    print("  5. 종합 보고서 생성")
    print("  6. 모든 예제 실행")
    
    choice = input("\n선택 (1-6): ").strip()
    
    try:
        if choice == "1":
            example_basic_analysis()
        elif choice == "2":
            example_time_analysis()
        elif choice == "3":
            example_weekday_analysis()
        elif choice == "4":
            example_station_analysis()
        elif choice == "5":
            example_full_report()
        elif choice == "6":
            example_basic_analysis()
            example_time_analysis()
            example_weekday_analysis()
            example_station_analysis()
            example_full_report()
        else:
            print("❌ 잘못된 선택입니다.")
            
    except FileNotFoundError:
        print("\n❌ 데이터 파일을 찾을 수 없습니다.")
        print("💡 먼저 데이터를 수집하세요:")
        print("   python scripts/collect_subway_data.py")
