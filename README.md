# seoul-traffic-pattern-analysis

## Project Information
- 서울시와 수도권의 교통 데이터를 수집하고 분석하여 요일별, 시간대별 교통 패턴의 차이를 규명하는 프로젝트

## 데이터 소스
- **서울시 지하철 승하차 데이터** (서울 열린데이터광장)
- **서울시 버스 승하차 데이터** (서울 열린데이터광장)  
- **TOPIS 교통정보** (서울시 교통정보 시스템)

## Stack
- **Language**: Python 3
- **Library**: 
  - pandas (데이터 처리)
  - matplotlib, seaborn (시각화)
  - requests (API 호출)

## ⚙️ 프로젝트 구조
```
seoul-traffic-pattern-analysis/
├── data/
│   ├── raw/              # 원본 데이터
│   └── processed/        # 전처리된 데이터
├── src/
│   ├── data_collection/  # 데이터 수집 스크립트
│   ├── analysis/         # 분석 코드
│   └── visualization/    # 시각화 코드
├── notebooks/           # Jupyter 노트북
└── results/            # 분석 결과
```


---

## Phase 1: 데이터 수집
- 서울시 지하철/버스 승하차 데이터와 TOPIS 교통정보를 수집하는 코드 개발

### 수집 대상 데이터
1. **지하철 승하차 데이터**
   - 역별, 시간대별, 요일별 승하차 인원
   - 1-9호선 + 신분당선 등 모든 노선
   
2. **버스 승하차 데이터**
   - 정류장별 이용객 수
   - 노선별 이용 패턴
   
3. **TOPIS 교통정보**
   - 주요 간선도로 통행속도
   - 교차로별 신호 및 대기시간




## 🛠️ Install
```bash
git clone https://github.com/your-username/seoul-traffic-pattern-analysis.git
cd seoul-traffic-pattern-analysis

pip install -r requirements.txt

python src/data_collection/collect_subway_data.py
```

   
