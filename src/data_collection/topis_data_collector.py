"""
서울시 TOPIS 교통 정보 수집 클래스
"""
import requests
import pandas as pd
import json
import time
from datetime import datetime
import os

class TopisDataCollector:
    def __init__(self, api_key):
        """
        서울시 TOPIS 데이터 수집기 초기화

        Args:
            api_key (str): 서울 열린데이터광장에서 발급받은 API 키
        """
        self.api_key = api_key
        self.base_url = "http://openapi.seoul.go.kr:8088"

    def get_road_speed_data(self, save_path="data/raw/"):
        """
        TOPIS 도로 속도 데이터 수집 (실시간)

        Args:
            save_path (str): 데이터 저장 경로
        """
        os.makedirs(save_path, exist_ok=True)
        service_name = "spotSpeedInfo"
        
        print(f"🚗 TOPIS 실시간 도로 속도 데이터 수집 중...")

        try:
            data = self._fetch_all_data(service_name)

            if data:
                print(f"✅ 데이터 수집 완료 ({len(data)}건)")
                df = pd.DataFrame(data)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"topis_road_speed_{timestamp}.csv" # 뒤에 timestamp
                filepath = os.path.join(save_path, filename)
                df.to_csv(filepath, index=False, encoding='utf-8-sig')

                print(f"\n📊 데이터 수집 완료!")
                print(f"   파일: {filepath}")
                print(f"   총 {len(df):,}건의 데이터")

                return df
            else:
                print(f"❌ 수집된 데이터가 없습니다.")
                return None

        except Exception as e:
            print(f"❌ 데이터 수집 실패: {str(e)}")
            return None

    def _fetch_all_data(self, service_name):
        """
        특정 서비스의 모든 데이터를 API로 가져오기
        """
        start_index = 1
        end_index = 1000
        all_results = []

        while True:
            url = f"{self.base_url}/{self.api_key}/json/{service_name}/{start_index}/{end_index}"
            print(f"   요청 중... [{start_index}~{end_index}]")

            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                data = response.json()

                if service_name in data:
                    if 'RESULT' in data[service_name]:
                        result_code = data[service_name]['RESULT']['CODE']
                        result_msg = data[service_name]['RESULT']['MESSAGE']

                        if result_code == 'INFO-000':
                            pass
                        elif result_code == 'INFO-200':
                            print(f"   ℹ️  해당 구간에 데이터가 없습니다.")
                            break
                        else:
                            print(f"   ⚠️  API 응답: [{result_code}] {result_msg}")
                            break

                    if 'row' in data[service_name]:
                        rows = data[service_name]['row']
                        all_results.extend(rows)

                        if len(rows) < 1000:
                            break

                        start_index += 1000
                        end_index += 1000
                        time.sleep(0.1)
                    else:
                        break
                else:
                    print(f"   ❌ 예상치 못한 응답 구조입니다.")
                    break

            except requests.RequestException as e:
                print(f"   ❌ API 요청 오류: {str(e)}")
                break
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON 파싱 오류: {str(e)}")
                break

        return all_results
