"""
서울시 지하철 이용 패턴 분석 클래스
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os


class SubwayPatternAnalyzer:
    def __init__(self, data_path=None):
        """
        지하철 패턴 분석기 초기화
        
        Args:
            data_path (str): 분석할 CSV 파일 경로
        """
        self.data_path = data_path
        self.df = None
        self.df_processed = None
        
    def load_data(self, filepath=None):
        """
        CSV 데이터 로드
        
        Args:
            filepath (str): CSV 파일 경로 (기본값: self.data_path)
        """
        if filepath:
            self.data_path = filepath
            
        if not self.data_path:
            raise ValueError("데이터 파일 경로가 지정되지 않았습니다.")
            
        print(f"📂 데이터 로딩 중: {self.data_path}")
        
        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
            print(f"✅ 데이터 로드 완료: {len(self.df):,}건")
            return self.df
        except Exception as e:
            print(f"❌ 데이터 로드 실패: {str(e)}")
            return None
    
    def preprocess_data(self):
        """
        데이터 전처리
        - 날짜 형식 변환
        - 요일 추가
        - 시간대별 컬럼 정리
        """
        if self.df is None:
            print("❌ 먼저 데이터를 로드하세요.")
            return None
            
        print("\n🔧 데이터 전처리 시작...")
        
        df = self.df.copy()
        
        # 날짜 형식 변환
        if 'USE_DT' in df.columns:
            df['USE_DT'] = pd.to_datetime(df['USE_DT'], format='%Y%m%d')
            df['YEAR'] = df['USE_DT'].dt.year
            df['MONTH'] = df['USE_DT'].dt.month
            df['DAY'] = df['USE_DT'].dt.day
            df['WEEKDAY'] = df['USE_DT'].dt.dayofweek  # 0=월요일, 6=일요일
            df['WEEKDAY_NAME'] = df['USE_DT'].dt.day_name()
            
            # 한글 요일명
            weekday_kr = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 
                         4: '금요일', 5: '토요일', 6: '일요일'}
            df['WEEKDAY_KR'] = df['WEEKDAY'].map(weekday_kr)
            
            # 평일/주말 구분
            df['IS_WEEKEND'] = df['WEEKDAY'].isin([5, 6])
            df['DAY_TYPE'] = df['IS_WEEKEND'].map({True: '주말', False: '평일'})
            
        print("   ✅ 날짜 처리 완료")
        
        # 시간대별 승하차 컬럼 찾기
        boarding_cols = [col for col in df.columns if 'GTON_TNOPE' in col or col.endswith('승차')]
        alighting_cols = [col for col in df.columns if 'GTOFF_TNOPE' in col or col.endswith('하차')]
        
        if boarding_cols:
            print(f"   ✅ 승차 컬럼: {len(boarding_cols)}개")
        if alighting_cols:
            print(f"   ✅ 하차 컬럼: {len(alighting_cols)}개")
        
        self.df_processed = df
        print("✅ 전처리 완료\n")
        
        return df
    
    def analyze_basic_stats(self):
        """
        기본 통계 분석
        """
        if self.df_processed is None:
            print("❌ 먼저 데이터를 전처리하세요.")
            return None
            
        df = self.df_processed
        
        print("\n" + "="*60)
        print("📊 기본 통계 분석")
        print("="*60)
        
        # 전체 기간
        print(f"\n📅 분석 기간: {df['USE_DT'].min().date()} ~ {df['USE_DT'].max().date()}")
        print(f"   총 일수: {df['USE_DT'].nunique()}일")
        
        # 노선별 통계
        if 'LINE_NUM' in df.columns:
            print(f"\n🚇 노선별 데이터 건수:")
            line_stats = df.groupby('LINE_NUM').size().sort_index()
            for line, count in line_stats.items():
                print(f"   {line}: {count:,}건")
        
        # 역 통계
        if 'SUB_STA_NM' in df.columns:
            print(f"\n🚉 역 통계:")
            print(f"   총 역 수: {df['SUB_STA_NM'].nunique()}개")
            print(f"   가장 많은 데이터를 가진 역 TOP 5:")
            top_stations = df['SUB_STA_NM'].value_counts().head(5)
            for station, count in top_stations.items():
                print(f"      {station}: {count:,}건")
        
        # 평일/주말 통계
        if 'DAY_TYPE' in df.columns:
            print(f"\n📆 평일/주말 분포:")
            daytype_stats = df.groupby('DAY_TYPE').size()
            for daytype, count in daytype_stats.items():
                print(f"   {daytype}: {count:,}건 ({count/len(df)*100:.1f}%)")
        
        return df
    
    def analyze_time_pattern(self):
        """
        시간대별 이용 패턴 분석
        """
        if self.df_processed is None:
            print("❌ 먼저 데이터를 전처리하세요.")
            return None
            
        df = self.df_processed
        
        print("\n" + "="*60)
        print("⏰ 시간대별 이용 패턴 분석")
        print("="*60)
        
        # 시간대별 승하차 컬럼 찾기
        # 서울 열린데이터광장 API는 00~23시까지 시간대별로 컬럼을 제공
        # 예: HR_4_GTON_TNOPE (4시 승차), HR_4_GTOFF_TNOPE (4시 하차)
        
        time_cols = {}
        for hour in range(24):
            boarding_col = f'HR_{hour}_GTON_TNOPE'
            alighting_col = f'HR_{hour}_GTOFF_TNOPE'
            
            if boarding_col in df.columns and alighting_col in df.columns:
                time_cols[hour] = {
                    'boarding': boarding_col,
                    'alighting': alighting_col
                }
        
        if not time_cols:
            print("⚠️  시간대별 컬럼을 찾을 수 없습니다.")
            print("   데이터 구조를 확인하세요.")
            return None
        
        print(f"✅ {len(time_cols)}개 시간대 데이터 확인")
        
        # 시간대별 총 이용객 계산
        hourly_stats = []
        
        for hour, cols in time_cols.items():
            total_boarding = df[cols['boarding']].sum()
            total_alighting = df[cols['alighting']].sum()
            total_passengers = total_boarding + total_alighting
            
            hourly_stats.append({
                'HOUR': hour,
                'TIME': f"{hour:02d}:00",
                'BOARDING': total_boarding,
                'ALIGHTING': total_alighting,
                'TOTAL': total_passengers
            })
        
        hourly_df = pd.DataFrame(hourly_stats)
        
        # 시간대 구분
        def classify_time_period(hour):
            if 7 <= hour <= 9:
                return '출근시간'
            elif 18 <= hour <= 20:
                return '퇴근시간'
            elif 0 <= hour <= 5:
                return '심야시간'
            else:
                return '일반시간'
        
        hourly_df['PERIOD'] = hourly_df['HOUR'].apply(classify_time_period)
        
        # 결과 출력
        print(f"\n📊 시간대별 총 이용객 (TOP 10):")
        top_hours = hourly_df.nlargest(10, 'TOTAL')
        for _, row in top_hours.iterrows():
            print(f"   {row['TIME']}: {row['TOTAL']:>12,}명 "
                  f"(승차 {row['BOARDING']:>10,}, 하차 {row['ALIGHTING']:>10,}) - {row['PERIOD']}")
        
        # 시간대 구분별 통계
        print(f"\n📊 시간대 구분별 이용 현황:")
        period_stats = hourly_df.groupby('PERIOD').agg({
            'TOTAL': 'sum',
            'BOARDING': 'sum',
            'ALIGHTING': 'sum'
        }).sort_values('TOTAL', ascending=False)
        
        for period, row in period_stats.iterrows():
            print(f"   {period:8s}: {row['TOTAL']:>12,}명 "
                  f"(승차 {row['BOARDING']:>10,}, 하차 {row['ALIGHTING']:>10,})")
        
        return hourly_df
    
    def analyze_weekday_pattern(self):
        """
        요일별 이용 패턴 분석
        """
        if self.df_processed is None:
            print("❌ 먼저 데이터를 전처리하세요.")
            return None
            
        df = self.df_processed
        
        print("\n" + "="*60)
        print("📆 요일별 이용 패턴 분석")
        print("="*60)
        
        # 시간대별 컬럼 찾기
        boarding_cols = [col for col in df.columns if 'GTON_TNOPE' in col]
        alighting_cols = [col for col in df.columns if 'GTOFF_TNOPE' in col]
        
        if not boarding_cols or not alighting_cols:
            print("⚠️  승하차 데이터 컬럼을 찾을 수 없습니다.")
            return None
        
        # 일별 총 이용객 계산
        df['DAILY_BOARDING'] = df[boarding_cols].sum(axis=1)
        df['DAILY_ALIGHTING'] = df[alighting_cols].sum(axis=1)
        df['DAILY_TOTAL'] = df['DAILY_BOARDING'] + df['DAILY_ALIGHTING']
        
        # 요일별 평균 계산
        weekday_stats = df.groupby('WEEKDAY_KR').agg({
            'DAILY_BOARDING': 'mean',
            'DAILY_ALIGHTING': 'mean',
            'DAILY_TOTAL': 'mean',
            'USE_DT': 'count'
        }).round(0)
        
        weekday_stats.columns = ['평균_승차', '평균_하차', '평균_총이용', '데이터_일수']
        
        # 요일 순서 정렬
        weekday_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        weekday_stats = weekday_stats.reindex(weekday_order)
        
        print(f"\n📊 요일별 평균 이용객:")
        for day, row in weekday_stats.iterrows():
            print(f"   {day}: {row['평균_총이용']:>12,.0f}명 "
                  f"(승차 {row['평균_승차']:>10,.0f}, 하차 {row['평균_하차']:>10,.0f}) "
                  f"[{int(row['데이터_일수'])}일]")
        
        # 평일 vs 주말 비교
        if 'DAY_TYPE' in df.columns:
            print(f"\n📊 평일 vs 주말 비교:")
            daytype_stats = df.groupby('DAY_TYPE').agg({
                'DAILY_BOARDING': 'mean',
                'DAILY_ALIGHTING': 'mean',
                'DAILY_TOTAL': 'mean'
            }).round(0)
            
            for daytype, row in daytype_stats.iterrows():
                print(f"   {daytype:4s}: {row['DAILY_TOTAL']:>12,.0f}명 "
                      f"(승차 {row['DAILY_BOARDING']:>10,.0f}, 하차 {row['DAILY_ALIGHTING']:>10,.0f})")
            
            # 차이 계산
            if '평일' in daytype_stats.index and '주말' in daytype_stats.index:
                weekday_total = daytype_stats.loc['평일', 'DAILY_TOTAL']
                weekend_total = daytype_stats.loc['주말', 'DAILY_TOTAL']
                diff_pct = ((weekday_total - weekend_total) / weekend_total * 100)
                print(f"\n   💡 평일이 주말보다 {diff_pct:.1f}% {'많음' if diff_pct > 0 else '적음'}")
        
        return weekday_stats
    
    def analyze_station_characteristics(self, top_n=10):
        """
        역별 특성 분석 (출근형/퇴근형 역 분류)
        
        Args:
            top_n (int): 상위 N개 역 분석
        """
        if self.df_processed is None:
            print("❌ 먼저 데이터를 전처리하세요.")
            return None
            
        df = self.df_processed
        
        print("\n" + "="*60)
        print(f"🚉 역별 특성 분석 (TOP {top_n})")
        print("="*60)
        
        # 출근시간(7-9시) vs 퇴근시간(18-20시) 승하차 비교
        morning_boarding = []
        morning_alighting = []
        evening_boarding = []
        evening_alighting = []
        
        for hour in range(7, 10):  # 7, 8, 9시
            col_b = f'HR_{hour}_GTON_TNOPE'
            col_a = f'HR_{hour}_GTOFF_TNOPE'
            if col_b in df.columns:
                morning_boarding.append(col_b)
            if col_a in df.columns:
                morning_alighting.append(col_a)
        
        for hour in range(18, 21):  # 18, 19, 20시
            col_b = f'HR_{hour}_GTON_TNOPE'
            col_a = f'HR_{hour}_GTOFF_TNOPE'
            if col_b in df.columns:
                evening_boarding.append(col_b)
            if col_a in df.columns:
                evening_alighting.append(col_a)
        
        if not morning_boarding or not evening_boarding:
            print("⚠️  출퇴근 시간대 데이터를 찾을 수 없습니다.")
            return None
        
        # 역별 집계
        df['MORNING_BOARDING'] = df[morning_boarding].sum(axis=1)
        df['MORNING_ALIGHTING'] = df[morning_alighting].sum(axis=1)
        df['EVENING_BOARDING'] = df[evening_boarding].sum(axis=1)
        df['EVENING_ALIGHTING'] = df[evening_alighting].sum(axis=1)
        
        station_stats = df.groupby('SUB_STA_NM').agg({
            'MORNING_BOARDING': 'sum',
            'MORNING_ALIGHTING': 'sum',
            'EVENING_BOARDING': 'sum',
            'EVENING_ALIGHTING': 'sum'
        })
        
        # 특성 지표 계산
        station_stats['TOTAL'] = station_stats.sum(axis=1)
        station_stats['MORNING_RATIO'] = (
            station_stats['MORNING_BOARDING'] / 
            (station_stats['MORNING_BOARDING'] + station_stats['MORNING_ALIGHTING'] + 1)
        )
        station_stats['EVENING_RATIO'] = (
            station_stats['EVENING_ALIGHTING'] / 
            (station_stats['EVENING_BOARDING'] + station_stats['EVENING_ALIGHTING'] + 1)
        )
        
        # 역 유형 분류
        def classify_station_type(row):
            if row['MORNING_RATIO'] > 0.6:
                return '출근형'  # 아침에 승차 많음
            elif row['EVENING_RATIO'] > 0.6:
                return '퇴근형'  # 저녁에 하차 많음
            else:
                return '혼합형'
        
        station_stats['TYPE'] = station_stats.apply(classify_station_type, axis=1)
        
        # 상위 역 출력
        top_stations = station_stats.nlargest(top_n, 'TOTAL')
        
        print(f"\n📊 총 이용객 TOP {top_n} 역:")
        print(f"{'순위':<4} {'역명':<15} {'총이용객':>12} {'유형':>8} "
              f"{'아침승차비':>10} {'저녁하차비':>10}")
        print("-" * 75)
        
        for idx, (station, row) in enumerate(top_stations.iterrows(), 1):
            print(f"{idx:<4} {station:<15} {row['TOTAL']:>12,.0f} {row['TYPE']:>8} "
                  f"{row['MORNING_RATIO']:>9.1%} {row['EVENING_RATIO']:>9.1%}")
        
        # 유형별 통계
        print(f"\n📊 역 유형별 분포:")
        type_counts = station_stats['TYPE'].value_counts()
        for station_type, count in type_counts.items():
            pct = count / len(station_stats) * 100
            print(f"   {station_type:8s}: {count:>4}개 ({pct:>5.1f}%)")
        
        return station_stats
    
    def generate_summary_report(self, save_path="results/"):
        """
        종합 분석 보고서 생성
        
        Args:
            save_path (str): 보고서 저장 경로
        """
        os.makedirs(save_path, exist_ok=True)
        
        print("\n" + "="*60)
        print("📄 종합 분석 보고서 생성")
        print("="*60)
        
        # 모든 분석 실행
        self.analyze_basic_stats()
        hourly_df = self.analyze_time_pattern()
        weekday_df = self.analyze_weekday_pattern()
        station_df = self.analyze_station_characteristics(top_n=20)
        
        # 보고서 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if hourly_df is not None:
            hourly_path = os.path.join(save_path, f"hourly_pattern_{timestamp}.csv")
            hourly_df.to_csv(hourly_path, index=False, encoding='utf-8-sig')
            print(f"\n✅ 시간대별 분석 저장: {hourly_path}")
        
        if weekday_df is not None:
            weekday_path = os.path.join(save_path, f"weekday_pattern_{timestamp}.csv")
            weekday_df.to_csv(weekday_path, encoding='utf-8-sig')
            print(f"✅ 요일별 분석 저장: {weekday_path}")
        
        if station_df is not None:
            station_path = os.path.join(save_path, f"station_characteristics_{timestamp}.csv")
            station_df.to_csv(station_path, encoding='utf-8-sig')
            print(f"✅ 역별 특성 분석 저장: {station_path}")
        
        print(f"\n🎉 분석 완료!")
        
        return {
            'hourly': hourly_df,
            'weekday': weekday_df,
            'station': station_df
        }
