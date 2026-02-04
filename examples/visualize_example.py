#!/usr/bin/env python3
"""
시각화 예제 코드
간단하게 차트를 생성하는 예제입니다.
"""

import sys
import os
import platform
import matplotlib.pyplot as plt

# 운영체제별 한글 폰트 자동 설정
system = platform.system()
if system == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif system == 'Darwin':  # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

# 프로젝트 루트 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.analysis.subway_pattern_analyzer import SubwayPatternAnalyzer
from src.visualization.subway_visualizer import SubwayVisualizer


def main():
    """
    시각화 예제
    """
    # 데이터 파일 경로 (실제 파일명으로 수정하세요)
    data_file = "data/raw/subway_hourly_202410.csv"
    
    print("📊 시각화 예제 시작")
    print("="*60)
    
    # 1. 분석기 초기화 및 데이터 로드
    print("\n1️⃣ 데이터 로딩...")
    analyzer = SubwayPatternAnalyzer(data_file)
    analyzer.load_data()
    analyzer.preprocess_data()
    
    # 2. 시각화 도구 초기화
    print("\n2️⃣ 시각화 도구 초기화...")
    visualizer = SubwayVisualizer(save_path="results/charts/")
    
    # 3. 시간대별 패턴 그래프
    print("\n3️⃣ 시간대별 패턴 그래프 생성...")
    hourly_df = analyzer.analyze_time_pattern()
    visualizer.plot_hourly_pattern(hourly_df)
    
    # 4. 요일별 패턴 그래프
    print("\n4️⃣ 요일별 패턴 그래프 생성...")
    weekday_df = analyzer.analyze_weekday_pattern()
    visualizer.plot_weekday_pattern(weekday_df)
    
    # 5. 역별 TOP 20 그래프
    print("\n5️⃣ 역별 TOP 20 그래프 생성...")
    station_df = analyzer.analyze_station_characteristics(top_n=20)
    visualizer.plot_top_stations(station_df, top_n=20)
    
    print("\n" + "="*60)
    print("🎉 시각화 완료!")
    print("📁 results/charts/ 폴더를 확인하세요.")
    print("="*60)


if __name__ == "__main__":
    main()
