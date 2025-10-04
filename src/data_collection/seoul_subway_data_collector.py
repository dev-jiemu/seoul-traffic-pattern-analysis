"""
서울시 지하철 승하차 데이터 수집 클래스
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
import os


class SeoulSubwayDataCollector:
    def __init__(self, api_key):
        """
        서울시 지하철 데이터 수집기 초기화
        
        Args:
            api_key (str): 서울 열린데이터광장에서 발급받은 API 키
        """
        self.api_key = api_key
        self.base_url = "http://openapi.seoul.go.kr:8088"
        
    def get_subway_hourly_data(self, start_date, end_date, save_path="data/raw/"):
        """
        지하철 시간대별 승하차 인원 데이터 수집
        
        Args:
            start_date (str): 시작 날짜 (YYYY-MM-DD)
            end_date (str): 종료 날짜 (YYYY-MM-DD)
            save_path (str): 데이터 저장 경로
        """
        
        # 데이터 저장 디렉토리 생성
        os.makedirs(save_path, exist_ok=True)
        
        # API URL 구성 (실제 서비스명은 API 문서에서 확인 필요)
        service_name = "CardSubwayTime"  # 실제 서비스명으로 수정 필요
        
        all_data = []
        
        # 날짜별로 데이터 수집
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current_date <= end_date_obj:
            date_str = current_date.strftime("%Y%m%d")
            
            try:
                # API 호출
                data = self._fetch_data_by_date(service_name, date_str)
                if data:
                    all_data.extend(data)
                    print(f"✅ {date_str} 데이터 수집 완료 ({len(data)}건)")
                else:
                    print(f"❌ {date_str} 데이터 없음")
                
                # API 호출 제한을 위한 대기
                time.sleep(0.1)
                
            except Exception as e:
                print(f"❌ {date_str} 데이터 수집 실패: {str(e)}")
            
            current_date += timedelta(days=1)
        
        # DataFrame으로 변환 및 저장
        if all_data:
            df = pd.DataFrame(all_data)
            
            # CSV 파일로 저장
            filename = f"subway_hourly_{start_date}_{end_date}.csv"
            filepath = os.path.join(save_path, filename)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            print(f"\n📊 데이터 수집 완료!")
            print(f"   파일: {filepath}")
            print(f"   총 {len(df)}건의 데이터")
            
            return df
        else:
            print("❌수집된 데이터가 없습니다.")
            return None
    
    def _fetch_data_by_date(self, service_name, date_str):
        """
        특정 날짜의 데이터를 API로 가져오기
        """
        start_index = 1
        end_index = 1000  # 한 번에 최대 1000건
        all_results = []
        
        while True:
            # API URL 구성
            url = f"{self.base_url}/{self.api_key}/json/{service_name}/{start_index}/{end_index}/"
            
            # 날짜 파라미터가 필요한 경우 추가
            params = {
                "USE_DT": date_str  # 실제 파라미터명은 API 문서 확인 필요
            }
            
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                # 응답 구조에 따라 데이터 추출 (실제 응답 구조에 맞게 수정 필요)
                if 'CardSubwayTime' in data and 'row' in data['CardSubwayTime']:
                    rows = data['CardSubwayTime']['row']
                    all_results.extend(rows)
                    
                    # 더 이상 데이터가 없으면 종료
                    if len(rows) < 1000:
                        break
                    
                    # 다음 페이지를 위한 인덱스 업데이트
                    start_index += 1000
                    end_index += 1000
                    
                else:
                    break
                    
            except requests.RequestException as e:
                print(f"API 요청 오류: {str(e)}")
                break
            except json.JSONDecodeError as e:
                print(f"JSON 파싱 오류: {str(e)}")
                break
        
        return all_results
    
    def explore_data_structure(self, df):
        """
        수집된 데이터의 구조 탐색
        """
        if df is None or df.empty:
            print("❌ 탐색할 데이터가 없습니다.")
            return
            
        print("📊 === 데이터 구조 탐색 ===\n")
        
        # 기본 정보
        print(f"🔍 데이터 크기: {df.shape[0]:,}행 × {df.shape[1]}열")
        print(f"🗓️ 기간: {df['USE_DT'].min()} ~ {df['USE_DT'].max()}")
        
        # 컬럼 정보
        print(f"\n📋 컬럼 목록:")
        for i, col in enumerate(df.columns):
            print(f"   {i+1}. {col}")
        
        # 지하철 노선 확인
        if 'LINE_NUM' in df.columns:
            print(f"\n🚇 지하철 노선:")
            lines = df['LINE_NUM'].unique()
            for line in sorted(lines):
                count = len(df[df['LINE_NUM'] == line])
                print(f"   {line}호선: {count:,}건")
        
        # 요일별 데이터 확인
        if 'USE_DT' in df.columns:
            df['weekday'] = pd.to_datetime(df['USE_DT']).dt.day_name()
            print(f"\n📅 요일별 데이터:")
            weekday_counts = df['weekday'].value_counts()
            for day, count in weekday_counts.items():
                print(f"   {day}: {count:,}건")
        
        # 샘플 데이터 출력
        print(f"\n📋 샘플 데이터 (처음 5행):")
        print(df.head())
        
        return df
