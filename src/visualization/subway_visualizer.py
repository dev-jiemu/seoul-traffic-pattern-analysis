"""
서울시 지하철 데이터 시각화 클래스
"""

import pandas as pd
import numpy as np
import platform
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import matplotlib.font_manager as fm

# 운영체제별 한글 폰트 자동 설정
system = platform.system()
if system == 'Windows':
    font_path = r'C:\Windows\Fonts\malgun.ttf'  # Malgun Gothic 경로
    if os.path.exists(font_path):
        fontprop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = fontprop.get_name()
    else:
        print("⚠️ Malgun Gothic 폰트를 찾을 수 없습니다.")
elif system == 'Darwin':  # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False


class SubwayVisualizer:
    """
    지하철 패턴 시각화 클래스
    """
    
    def __init__(self, save_path="results/charts/"):
        """
        시각화 도구 초기화
        
        Args:
            save_path (str): 그래프 저장 경로
        """
        self.save_path = save_path
        os.makedirs(save_path, exist_ok=True)
        
        # seaborn 스타일 설정
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        
        print(f"📊 시각화 도구 초기화 완료")
        print(f"💾 저장 경로: {save_path}")
    
    def plot_hourly_pattern(self, hourly_df, save_filename=None):
        """
        시간대별 이용 패턴 그래프
        
        Args:
            hourly_df (DataFrame): 시간대별 데이터
                필수 컬럼: HOUR, BOARDING, ALIGHTING, TOTAL
            save_filename (str): 저장할 파일명 (None이면 자동 생성)
        """
        print("\n📈 시간대별 이용 패턴 그래프 생성 중...")
        
        # 그래프 크기 설정
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # 시간대(x축) 데이터
        hours = hourly_df['HOUR']
        
        # 라인 플롯
        ax.plot(hours, hourly_df['TOTAL'], 
                marker='o', linewidth=2, markersize=6,
                label='총 이용객', color='#2E86AB')
        
        ax.plot(hours, hourly_df['BOARDING'], 
                marker='s', linewidth=1.5, markersize=4, 
                label='승차', color='#A23B72', alpha=0.7)
        
        ax.plot(hours, hourly_df['ALIGHTING'], 
                marker='^', linewidth=1.5, markersize=4,
                label='하차', color='#F18F01', alpha=0.7)
        
        # 출퇴근 시간대 강조 (배경색)
        ax.axvspan(7, 9, alpha=0.2, color='yellow', label='출근시간 (07-09시)')
        ax.axvspan(18, 20, alpha=0.2, color='orange', label='퇴근시간 (18-20시)')
        
        # 그래프 꾸미기
        ax.set_xlabel('시간대', fontsize=12, fontweight='bold')
        ax.set_ylabel('이용객 수 (명)', fontsize=12, fontweight='bold')
        ax.set_title('서울시 지하철 시간대별 이용 패턴', fontsize=16, fontweight='bold', pad=20)
        
        # x축 설정 (0시~23시)
        ax.set_xticks(range(0, 24, 2))
        ax.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)], rotation=45)
        
        # y축 숫자 포맷 (천 단위 콤마)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        # 범례
        ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
        
        # 그리드
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 레이아웃 조정
        plt.tight_layout()
        
        # 저장
        if save_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_filename = f"hourly_pattern_{timestamp}.png"
        
        filepath = os.path.join(self.save_path, save_filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✅ 저장 완료: {filepath}")
        
        plt.close()
        
        return filepath
    
    def plot_weekday_pattern(self, weekday_df, save_filename=None):
        """
        요일별 이용 패턴 막대 그래프
        
        Args:
            weekday_df (DataFrame): 요일별 데이터
                인덱스: 요일명 (월요일, 화요일, ...)
                필수 컬럼: 평균_총이용
            save_filename (str): 저장할 파일명
        """
        print("\n📊 요일별 이용 패턴 그래프 생성 중...")
        
        # 그래프 크기
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 요일 순서 (월~일)
        weekday_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        weekday_df = weekday_df.reindex(weekday_order)
        
        # 평일/주말 색상 구분
        colors = ['#3498db'] * 5 + ['#e74c3c', '#e74c3c']  # 평일: 파랑, 주말: 빨강
        
        # 막대 그래프
        bars = ax.bar(range(len(weekday_df)), 
                      weekday_df['평균_총이용'],
                      color=colors, 
                      alpha=0.8,
                      edgecolor='black',
                      linewidth=1.2)
        
        # 막대 위에 숫자 표시
        for i, (idx, row) in enumerate(weekday_df.iterrows()):
            value = row['평균_총이용']
            ax.text(i, value, f'{value:,.0f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # 그래프 꾸미기
        ax.set_xlabel('요일', fontsize=12, fontweight='bold')
        ax.set_ylabel('평균 이용객 수 (명)', fontsize=12, fontweight='bold')
        ax.set_title('서울시 지하철 요일별 평균 이용 패턴', fontsize=16, fontweight='bold', pad=20)
        
        # x축 라벨
        ax.set_xticks(range(len(weekday_df)))
        ax.set_xticklabels(weekday_order, fontsize=11)
        
        # y축 포맷
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        # 범례
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#3498db', alpha=0.8, label='평일'),
            Patch(facecolor='#e74c3c', alpha=0.8, label='주말')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
        
        # 그리드
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        
        # 레이아웃
        plt.tight_layout()
        
        # 저장
        if save_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_filename = f"weekday_pattern_{timestamp}.png"
        
        filepath = os.path.join(self.save_path, save_filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✅ 저장 완료: {filepath}")
        
        plt.close()
        
        return filepath
    
    def plot_top_stations(self, station_df, top_n=20, save_filename=None):
        """
        역별 TOP N 수평 막대 그래프
        
        Args:
            station_df (DataFrame): 역별 특성 데이터
                인덱스: 역명
                필수 컬럼: TOTAL, TYPE
            top_n (int): 상위 N개 역
            save_filename (str): 저장할 파일명
        """
        print(f"\n🏆 역별 TOP {top_n} 그래프 생성 중...")
        
        # 상위 N개 역 추출
        top_stations = station_df.nlargest(top_n, 'TOTAL')
        
        # 그래프 크기 (역이 많으면 세로 크기 늘리기)
        fig, ax = plt.subplots(figsize=(12, max(8, top_n * 0.4)))
        
        # 역 타입별 색상
        color_map = {
            '출근형': '#3498db',  # 파랑
            '퇴근형': '#e74c3c',  # 빨강
            '혼합형': '#95a5a6'   # 회색
        }
        colors = [color_map.get(t, '#95a5a6') for t in top_stations['TYPE']]
        
        # 수평 막대 그래프
        y_pos = range(len(top_stations))
        bars = ax.barh(y_pos, top_stations['TOTAL'], 
                       color=colors, alpha=0.8,
                       edgecolor='black', linewidth=1)
        
        # 막대 끝에 숫자 표시
        for i, (station, row) in enumerate(top_stations.iterrows()):
            value = row['TOTAL']
            ax.text(value, i, f' {value:,.0f}',
                   va='center', fontsize=9, fontweight='bold')
        
        # 그래프 꾸미기
        ax.set_xlabel('총 이용객 수 (명)', fontsize=12, fontweight='bold')
        ax.set_ylabel('역명', fontsize=12, fontweight='bold')
        ax.set_title(f'서울시 지하철 이용객 TOP {top_n} 역', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # y축 라벨 (역 이름)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_stations.index, fontsize=10)
        
        # x축 포맷
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        # 범례
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#3498db', alpha=0.8, label='출근형 역'),
            Patch(facecolor='#e74c3c', alpha=0.8, label='퇴근형 역'),
            Patch(facecolor='#95a5a6', alpha=0.8, label='혼합형 역')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
        
        # 그리드
        ax.grid(True, alpha=0.3, linestyle='--', axis='x')
        
        # 레이아웃
        plt.tight_layout()
        
        # 저장
        if save_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_filename = f"top_stations_{timestamp}.png"
        
        filepath = os.path.join(self.save_path, save_filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✅ 저장 완료: {filepath}")
        
        plt.close()
        
        return filepath
    
    def plot_station_heatmap(self, df, top_n=30, save_filename=None):
        """
        역별 시간대별 히트맵 (심화)
        
        Args:
            df (DataFrame): 전처리된 데이터프레임
            top_n (int): 상위 N개 역만 표시
            save_filename (str): 저장할 파일명
        """
        print(f"\n🔥 역별 시간대별 히트맵 생성 중 (TOP {top_n})...")
        
        # 시간대별 컬럼 찾기
        boarding_cols = [col for col in df.columns if 'GET_ON_NOPE' in col]
        
        if not boarding_cols:
            print("⚠️  시간대별 데이터를 찾을 수 없습니다.")
            return None
        
        # 역별 시간대별 합계
        station_hourly = df.groupby('STTN')[boarding_cols].sum()
        
        # 총 이용객 기준 상위 N개 역
        station_hourly['TOTAL'] = station_hourly.sum(axis=1)
        top_stations = station_hourly.nlargest(top_n, 'TOTAL').drop('TOTAL', axis=1)
        
        # 컬럼명을 시간대로 변환 (HR_0_GET_ON_NOPE -> 0)
        hour_cols = {}
        for col in top_stations.columns:
            hour = int(col.split('_')[1])
            hour_cols[col] = hour
        
        top_stations = top_stations.rename(columns=hour_cols)
        top_stations = top_stations.sort_index(axis=1)  # 시간 순서로 정렬
        
        # 그래프 크기
        fig, ax = plt.subplots(figsize=(16, max(10, top_n * 0.3)))
        
        # 히트맵 생성
        sns.heatmap(top_stations, 
                    cmap='YlOrRd',  # 노랑-주황-빨강
                    annot=False,     # 숫자 표시 안함 (너무 많아서)
                    fmt=',',
                    cbar_kws={'label': '승차 인원 (명)'},
                    linewidths=0.5,
                    linecolor='white',
                    ax=ax)
        
        # 그래프 꾸미기
        ax.set_xlabel('시간대', fontsize=12, fontweight='bold')
        ax.set_ylabel('역명', fontsize=12, fontweight='bold')
        ax.set_title(f'서울시 지하철 역별 시간대별 승차 패턴 (TOP {top_n})', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # x축 라벨 (시간대)
        ax.set_xticklabels([f'{h:02d}' for h in range(24)], rotation=0, fontsize=9)
        
        # y축 라벨 (역 이름)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=9, rotation=0)
        
        # 레이아웃
        plt.tight_layout()
        
        # 저장
        if save_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_filename = f"station_heatmap_{timestamp}.png"
        
        filepath = os.path.join(self.save_path, save_filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✅ 저장 완료: {filepath}")
        
        plt.close()
        
        return filepath
    
    def generate_all_charts(self, analyzer):
        """
        모든 차트 일괄 생성
        
        Args:
            analyzer (SubwayPatternAnalyzer): 분석 객체
        
        Returns:
            dict: 생성된 차트 파일 경로들
        """
        print("\n" + "="*60)
        print("📊 모든 차트 생성 시작")
        print("="*60)
        
        charts = {}
        
        # 1. 시간대별 패턴
        if analyzer.df_processed is not None:
            hourly_df = analyzer.analyze_time_pattern()
            if hourly_df is not None:
                charts['hourly'] = self.plot_hourly_pattern(hourly_df)
        
        # 2. 요일별 패턴
        if analyzer.df_processed is not None:
            weekday_df = analyzer.analyze_weekday_pattern()
            if weekday_df is not None:
                charts['weekday'] = self.plot_weekday_pattern(weekday_df)
        
        # 3. 역별 TOP 20
        if analyzer.df_processed is not None:
            station_df = analyzer.analyze_station_characteristics(top_n=20)
            if station_df is not None:
                charts['stations'] = self.plot_top_stations(station_df, top_n=20)
        
        # 4. 히트맵
        if analyzer.df_processed is not None:
            charts['heatmap'] = self.plot_station_heatmap(analyzer.df_processed, top_n=30)
        
        print("\n" + "="*60)
        print(f"🎉 차트 생성 완료! 총 {len(charts)}개")
        print("="*60)
        
        for chart_type, filepath in charts.items():
            if filepath:
                print(f"  📈 {chart_type}: {filepath}")
        
        return charts
