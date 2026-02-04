# seoul-traffic-pattern-analysis

## Project Information
- 서울시와 수도권의 교통 데이터를 수집하고 분석하여 요일별, 시간대별 교통 패턴의 차이를 규명하는 프로젝트

## 데이터 소스
- **서울시 지하철 승하차 데이터** (서울 열린데이터광장)
  - https://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do?tab=A
- **서울시 버스 승하차 데이터** (서울 열린데이터광장)  
- **TOPIS 교통정보** (서울시 교통정보 시스템)

## Stack
- **Language**: Python 3
- **Library**: 
  - pandas (데이터 처리)
  - matplotlib, seaborn (정적 시각화)
  - plotly (인터랙티브 차트)
  - streamlit (웹 대시보드)
  - requests (API 호출)

## ⚙️ 프로젝트 구조
```
seoul-traffic-pattern-analysis/
├── app.py               # Streamlit 대시보드 메인 ✅ NEW!
├── data/
│   ├── raw/              # 원본 데이터 (CSV)
│   └── processed/        # 전처리된 데이터
├── src/
│   ├── data_collection/  # 데이터 수집 스크립트
│   │   └── seoul_subway_data_collector.py  ✅
│   ├── analysis/         # 분석 코드 ✅
│   │   └── subway_pattern_analyzer.py
│   ├── visualization/    # 시각화 코드 ✅
│   │   └── subway_visualizer.py
│   └── config/          # 설정 파일
│       └── settings.py   ✅
├── scripts/             # 실행 스크립트
│   ├── collect_subway_data.py  ✅
│   ├── analyze_patterns.py     ✅
│   └── visualize_patterns.py   ✅
├── examples/            # 예제 코드 ✅
│   ├── analyze_example.py
│   └── visualize_example.py    ✅
└── results/
    ├── *.csv            # 분석 결과 (CSV)
    └── charts/          # 시각화 차트 (PNG) ✅
```


---

## 📌 개발 진행 상황

### ✅ Phase 1: 데이터 수집 (완료)
- [x] 서울시 지하철 승하차 데이터 수집 API 개발
- [x] 월별 데이터 수집 및 CSV 저장 기능
- [x] 사용자 친화적 CLI 인터페이스
- [ ] 버스 승하차 데이터 수집 (예정)
- [x] TOPIS 교통정보 수집 (예정)

### ✅ Phase 2: 데이터 분석 (완료) 🎉
- [x] 기본 통계 분석 (노선별, 역별, 기간별)
- [x] 시간대별 패턴 분석 (출퇴근 시간, 심야 시간)
- [x] 요일별 패턴 분석 (평일 vs 주말)
- [x] 역별 특성 분석 (출근형/퇴근형/혼합형 역 분류)
- [x] 종합 보고서 생성 기능

### 🚧 Phase 3: 데이터 시각화 (완료)
- [x] 시간대별 이용 패턴 그래프
- [x] 요일별 비교 차트
- [x] 역별 TOP 20 수평 막대 그래프
- [x] 역별 시간대별 히트맵
- [x] 차트 자동 저장 기능 (PNG, 300 DPI)

### ✅ Phase 4: 대시보드 (완료) 🎉 NEW!
- [x] Streamlit 기반 웹 대시보드
- [x] 인터랙티브 Plotly 차트
- [x] 실시간 필터링 (날짜, 노선, 요일)
- [x] KPI 지표 표시
- [x] 4가지 분석 탭 (시간대별, 요일별, 역별 순위, 히트맵)

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

### 4. 패턴 분석 ✨
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

### 5. 데이터 시각화 🎨 NEW!
```bash
# 대화형 시각화 실행
python3 scripts/visualize_patterns.py

# 또는 예제 코드 실행 (모든 차트 자동 생성)
python3 examples/visualize_example.py
```

**시각화 옵션:**
- 옵션 1: 시간대별 이용 패턴 그래프 (라인 차트)
- 옵션 2: 요일별 이용 패턴 그래프 (막대 차트)
- 옵션 3: 역별 TOP 20 그래프 (수평 막대 차트)
- 옵션 4: 역별 시간대별 히트맵 (30개 역)
- 옵션 5: 모든 차트 생성 (1~4 전체)

**시각화 결과:**
- `results/charts/hourly_pattern_YYYYMMDD_HHMMSS.png` - 시간대별 그래프
- `results/charts/weekday_pattern_YYYYMMDD_HHMMSS.png` - 요일별 그래프
- `results/charts/top_stations_YYYYMMDD_HHMMSS.png` - 역별 TOP 20
- `results/charts/station_heatmap_YYYYMMDD_HHMMSS.png` - 히트맵

**특징:**
- 🎨 한글 폰트 지원 (맑은 고딕)
- 📊 깔끔한 색상 구분 (평일/주말, 출근형/퇴근형 역)
- 💾 고해상도 저장 (300 DPI)
- 🔍 대화형 선택 메뉴

### 6. 대시보드 실행 🚀 NEW!
```bash
# Streamlit 대시보드 실행
streamlit run app.py
```

대시보드가 자동으로 브라우저에서 열립니다! (기본: http://localhost:8501)

**대시보드 기능:**
- 📊 **KPI 지표**: 총 역 수, 노선 수, 승하차 인원
- 🔍 **실시간 필터링**: 
  - 날짜 범위 선택
  - 노선 선택
  - 평일/주말 구분
- 📈 **4가지 분석 탭**:
  - 시간대별 이용 패턴 (인터랙티브 라인 차트)
  - 요일별 이용 패턴 (막대 차트)
  - 역별 순위 TOP 20 (수평 막대 차트)
  - 역별 시간대별 히트맵 (TOP 30)

**특징:**
- 🎨 Plotly 인터랙티브 차트 (줌, 호버 등)
- 💾 데이터 캐싱으로 빠른 로딩
- 📱 반응형 레이아웃
- 🖱️ 클릭만으로 필터 적용


