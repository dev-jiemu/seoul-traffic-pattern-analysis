"""
서울시 지하철 승하차 데이터 수집 클래스 (월 단위)
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime
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

    def get_subway_monthly_data(self, year_month, save_path="data/raw/"):
        """
        지하철 월별 승하차 인원 데이터 수집

        Args:
            year_month (str): 수집할 년월 (YYYY-MM)
            save_path (str): 데이터 저장 경로
        """

        # 데이터 저장 디렉토리 생성
        os.makedirs(save_path, exist_ok=True)

        # 서비스명
        service_name = "CardSubwayTime"

        # 년월을 YYYYMM 형식으로 변환
        ym_str = year_month.replace("-", "")  # 2024-08 -> 202408

        print(f"\n📅 {year_month} 데이터 수집 중...")

        try:
            # API 호출
            data = self._fetch_data_by_month(service_name, ym_str)

            if data:
                print(f"✅ {year_month} 데이터 수집 완료 ({len(data)}건)")

                # DataFrame으로 변환
                df = pd.DataFrame(data)

                # CSV 파일로 저장
                filename = f"subway_hourly_{year_month}.csv"
                filepath = os.path.join(save_path, filename)
                df.to_csv(filepath, index=False, encoding='utf-8-sig')

                print(f"\n📊 데이터 수집 완료!")
                print(f"   파일: {filepath}")
                print(f"   총 {len(df):,}건의 데이터")

                return df
            else:
                print(f"❌ {year_month} 데이터 없음")
                return None

        except Exception as e:
            print(f"❌ {year_month} 데이터 수집 실패: {str(e)}")
            return None

    def _fetch_data_by_month(self, service_name, ym_str):
        """
        특정 년월의 데이터를 API로 가져오기

        Args:
            service_name (str): API 서비스명
            ym_str (str): 년월 (YYYYMM 형식)
        """
        start_index = 1
        end_index = 1000
        all_results = []

        while True:
            # API URL 구성 (년월을 URL 경로에 포함)
            url = f"{self.base_url}/{self.api_key}/json/{service_name}/{start_index}/{end_index}/{ym_str}"

            print(f"   요청 중... [{start_index}~{end_index}]")

            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                data = response.json()

                # 응답 구조 확인
                if service_name in data:
                    # 에러 체크
                    if 'RESULT' in data[service_name]:
                        result_code = data[service_name]['RESULT']['CODE']
                        result_msg = data[service_name]['RESULT']['MESSAGE']

                        if result_code == 'INFO-000':  # 정상
                            pass
                        elif result_code == 'INFO-200':  # 데이터 없음
                            print(f"   ℹ️  해당 구간에 데이터가 없습니다.")
                            break
                        else:
                            print(f"   ⚠️  API 응답: [{result_code}] {result_msg}")
                            break

                    # 데이터 추출
                    if 'row' in data[service_name]:
                        rows = data[service_name]['row']
                        all_results.extend(rows)

                        # 가져온 데이터가 1000개 미만이면 마지막 페이지
                        if len(rows) < 1000:
                            break

                        # 다음 페이지
                        start_index += 1000
                        end_index += 1000

                        # API 호출 제한 방지
                        time.sleep(0.1)
                    else:
                        break
                else:
                    print(f"   ❌ 예상치 못한 응답 구조입니다.")
                    print(f"   응답 키: {list(data.keys())}")
                    break

            except requests.RequestException as e:
                print(f"   ❌ API 요청 오류: {str(e)}")
                break
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON 파싱 오류: {str(e)}")
                break

        return all_results

    def explore_data_structure(self, df):
        """
        수집된 데이터의 구조 탐색
        """
        if df is None or df.empty:
            print("❌ 탐색할 데이터가 없습니다.")
            return

        print("\n📊 === 데이터 구조 탐색 ===\n")

        # 기본 정보
        print(f"🔍 데이터 크기: {df.shape[0]:,}행 × {df.shape[1]}열")

        # 컬럼 정보
        print(f"\n📋 컬럼 목록:")
        for i, col in enumerate(df.columns):
            print(f"   {i+1}. {col}")

        # 날짜 정보 확인
        if 'USE_DT' in df.columns:
            print(f"\n🗓️ 날짜 범위: {df['USE_DT'].min()} ~ {df['USE_DT'].max()}")
            print(f"   총 일수: {df['USE_DT'].nunique()}일")

        # 지하철 노선 확인
        if 'LINE_NUM' in df.columns:
            print(f"\n🚇 지하철 노선:")
            lines = sorted(df['LINE_NUM'].unique())
            for line in lines:
                count = len(df[df['LINE_NUM'] == line])
                print(f"   {line}: {count:,}건")

        # 역 정보
        if 'SUB_STA_NM' in df.columns:
            print(f"\n🚉 총 역 수: {df['SUB_STA_NM'].nunique()}개")

        # 샘플 데이터 출력
        print(f"\n📋 샘플 데이터 (처음 3행):")
        print(df.head(3).to_string())

        return df