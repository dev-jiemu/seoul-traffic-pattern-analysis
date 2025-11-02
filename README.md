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
│   ├── raw/              # 원본 데이터 (CSV)
│   └── processed/        # 전처리된 데이터
├── src/
│   ├── data_collection/  # 데이터 수집 스크립트
│   │   └── seoul_subway_data_collector.py  ✅
│   ├── analysis/         # 분석 코드 ✅ NEW!
│   │   └── subway_pattern_analyzer.py
│   ├── visualization/    # 시각화 코드 (예정)
│   └── config/          # 설정 파일
│       └── settings.py   ✅
├── scripts/             # 실행 스크립트
│   ├── collect_subway_data.py  ✅
│   └── analyze_patterns.py     ✅ NEW!
├── examples/            # 예제 코드 ✅ NEW!
│   └── analyze_example.py
├── notebooks/           # Jupyter 노트북 (예정)
└── results/            # 분석 결과 (CSV)
```


---

## 📌 개발 진행 상황

### ✅ Phase 1: 데이터 수집 (완료)
- [x] 서울시 지하철 승하차 데이터 수집 API 개발
- [x] 월별 데이터 수집 및 CSV 저장 기능
- [x] 사용자 친화적 CLI 인터페이스
- [ ] 버스 승하차 데이터 수집 (예정)
- [ ] TOPIS 교통정보 수집 (예정)

### ✅ Phase 2: 데이터 분석 (완료) 🎉
- [x] 기본 통계 분석 (노선별, 역별, 기간별)
- [x] 시간대별 패턴 분석 (출퇴근 시간, 심야 시간)
- [x] 요일별 패턴 분석 (평일 vs 주말)
- [x] 역별 특성 분석 (출근형/퇴근형/혼합형 역 분류)
- [x] 종합 보고서 생성 기능

### 🚧 Phase 3: 데이터 시각화 (다음 단계)
- [ ] 시간대별 이용 패턴 그래프
- [ ] 요일별 비교 차트
- [ ] 역별 특성 히트맵
- [ ] 노선별 이용 추이

### 📋 Phase 4: 대시보드 (계획)
- [ ] 인터랙티브 웹 대시보드
- [ ] 실시간 데이터 업데이트
- [ ] 사용자 정의 필터링

---

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


### 📊 분석 계획
#### 1. 기본 통계 분석
- 역별 총 이용객 수
- 노선별 이용 패턴
- 시간대별 승하차 인원

#### 2. 시간대별 패턴 분석
- 출근 시간대 (07-09시) vs 퇴근 시간대 (18-20시)
- 심야 시간대 이용 패턴
- 시간대별 승하차 비율

#### 3. 요일별 패턴 분석
- 평일 vs 주말 차이
- 요일별 이용객 수 변화
- 요일별 피크 시간대 차이

#### 4. 역별 특성 분석
- 출근형 역 (아침 승차 많음)
- 퇴근형 역 (저녁 하차 많음)
- 상업지구 vs 주거지구



## 🛠️ Install & Usage

### 1. 설치
```bash
git clone https://github.com/your-username/seoul-traffic-pattern-analysis.git
cd seoul-traffic-pattern-analysis

pip install -r requirements.txt
```

### 2. API 키 설정
```bash
# 서울 열린데이터광장에서 발급받은 API KEY 등록
export SEOUL_API_KEY='여기에_발급받은_API_키'
```

### 3. 데이터 수집
```bash
# 지하철 승하차 데이터 수집
python3 scripts/collect_subway_data.py
```

### 4. 패턴 분석 ✨ NEW!
```bash
# 대화형 분석 실행
python3 scripts/analyze_patterns.py

# 또는 예제 코드 실행
python3 examples/analyze_example.py
```

**분석 옵션:**
- 옵션 1: 빠른 분석 (기본 통계만)
- 옵션 2: 상세 분석 (시간대/요일별 패턴)
- 옵션 3: 전체 분석 (역별 특성 포함)
- 옵션 4: 종합 보고서 생성 (CSV 파일 저장)

**분석 결과:**
- `results/hourly_pattern_YYYYMMDD_HHMMSS.csv` - 시간대별 분석
- `results/weekday_pattern_YYYYMMDD_HHMMSS.csv` - 요일별 분석
- `results/station_characteristics_YYYYMMDD_HHMMSS.csv` - 역별 특성

   
