#!/usr/bin/env python3
"""
서울시 지하철 패턴 시각화 실행 스크립트
"""

import sys
import io
import os
from glob import glob

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Windows 콘솔 인코딩 문제 해결
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.analysis.subway_pattern_analyzer import SubwayPatternAnalyzer
from src.visualization.subway_visualizer import SubwayVisualizer


def find_latest_data_file(data_path="data/raw/"):
    """
    가장 최근 데이터 파일 찾기
    """
    pattern = os.path.join(data_path, "subway_hourly_*.csv")
    files = glob(pattern)
    
    if not files:
        return None
    
    latest_file = sorted(files)[-1]
    return latest_file


def main():
    """
    메인 실행 함수
    """
    print("📊 서울시 지하철 패턴 시각화")
    print("="*60)
    
    # 데이터 파일 찾기
    print("\n🔍 데이터 파일 검색 중...")
    data_file = find_latest_data_file()
    
    if not data_file:
        print("\n❌ 데이터 파일을 찾을 수 없습니다.")
        print("💡 먼저 데이터를 수집하세요:")
        print("   python scripts/collect_subway_data.py")
        return
    
    print(f"✅ 데이터 파일 발견: {data_file}")
    
    # 분석기 초기화
    print("\n📂 데이터 로딩 및 전처리 중...")
    analyzer = SubwayPatternAnalyzer(data_file)
    analyzer.load_data()
    analyzer.preprocess_data()
    
    if analyzer.df_processed is None:
        print("❌ 데이터 전처리 실패")
        return
    
    # 시각화 도구 초기화
    visualizer = SubwayVisualizer(save_path="results/charts/")
    
    print("\n" + "="*60)
    print("시각화 옵션을 선택하세요:")
    print("="*60)
    print("  1. 시간대별 이용 패턴 그래프")
    print("  2. 요일별 이용 패턴 그래프")
    print("  3. 역별 TOP 20 그래프")
    print("  4. 역별 시간대별 히트맵")
    print("  5. 모든 차트 생성 (1~4 전체)")
    print("  0. 종료")
    
    while True:
        choice = input("\n선택 (0-5): ").strip()
        
        if choice == "0":
            print("\n👋 프로그램을 종료합니다.")
            break
        
        elif choice == "1":
            # 시간대별 패턴
            print("\n" + "="*60)
            hourly_df = analyzer.analyze_time_pattern()
            if hourly_df is not None:
                visualizer.plot_hourly_pattern(hourly_df)
            print("\n계속하려면 다른 옵션을 선택하세요...")
        
        elif choice == "2":
            # 요일별 패턴
            print("\n" + "="*60)
            weekday_df = analyzer.analyze_weekday_pattern()
            if weekday_df is not None:
                visualizer.plot_weekday_pattern(weekday_df)
            print("\n계속하려면 다른 옵션을 선택하세요...")
        
        elif choice == "3":
            # 역별 TOP 20
            print("\n" + "="*60)
            station_df = analyzer.analyze_station_characteristics(top_n=20)
            if station_df is not None:
                visualizer.plot_top_stations(station_df, top_n=20)
            print("\n계속하려면 다른 옵션을 선택하세요...")
        
        elif choice == "4":
            # 히트맵
            print("\n" + "="*60)
            visualizer.plot_station_heatmap(analyzer.df_processed, top_n=30)
            print("\n계속하려면 다른 옵션을 선택하세요...")
        
        elif choice == "5":
            # 모든 차트 생성
            charts = visualizer.generate_all_charts(analyzer)
            print("\n✅ 모든 차트가 생성되었습니다!")
            print(f"📁 저장 경로: results/charts/")
            print("\n계속하려면 다른 옵션을 선택하세요...")
        
        else:
            print("❌ 잘못된 선택입니다. 0-5 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    main()
