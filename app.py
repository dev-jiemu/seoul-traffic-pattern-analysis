"""
서울시 지하철 이용 패턴 분석 대시보드
Streamlit 기반 인터랙티브 웹 애플리케이션
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.analysis.subway_pattern_analyzer import SubwayPatternAnalyzer
from src.config.settings import DATA_DIR

# 페이지 설정
st.set_page_config(
    page_title="서울시 지하철 분석 대시보드",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 제목
st.title("🚇 서울시 지하철 이용 패턴 분석 대시보드")
st.markdown("---")


@st.cache_data
def load_subway_data():
    """
    지하철 데이터 로드 (캐싱)
    """
    # data/raw 폴더에서 가장 최근 CSV 파일 찾기
    raw_data_path = os.path.join(DATA_DIR, 'raw')
    
    if not os.path.exists(raw_data_path):
        return None
    
    csv_files = [f for f in os.listdir(raw_data_path) if f.endswith('.csv')]
    
    if not csv_files:
        return None
    
    # 가장 최근 파일 선택
    latest_file = sorted(csv_files)[-1]
    filepath = os.path.join(raw_data_path, latest_file)
    
    # 분석기로 데이터 로드
    analyzer = SubwayPatternAnalyzer(filepath)
    analyzer.load_data()
    df = analyzer.preprocess_data()
    
    return df, analyzer


# 사이드바 - 필터링 옵션
st.sidebar.header("📊 필터 옵션")

# 데이터 로드
data_load_state = st.sidebar.text('데이터 로딩 중...')
result = load_subway_data()

if result is None:
    st.error("❌ 데이터를 찾을 수 없습니다. 먼저 데이터를 수집해주세요.")
    st.stop()

df, analyzer = result
data_load_state.text('데이터 로드 완료! ✅')

# 필터 - 날짜 범위
if 'USE_DT' in df.columns:
    min_date = df['USE_DT'].min()
    max_date = df['USE_DT'].max()
    
    date_range = st.sidebar.date_input(
        "📅 날짜 범위",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        df = df[(df['USE_DT'] >= pd.Timestamp(date_range[0])) & 
                (df['USE_DT'] <= pd.Timestamp(date_range[1]))]

# 필터 - 노선 선택
if 'LN_NM' in df.columns:
    lines = ['전체'] + sorted(df['LN_NM'].unique().tolist())
    selected_line = st.sidebar.selectbox("🚉 노선 선택", lines)
    
    if selected_line != '전체':
        df = df[df['LN_NM'] == selected_line]

# 필터 - 평일/주말
if 'DAY_TYPE' in df.columns:
    day_type = st.sidebar.radio("📆 요일 구분", ['전체', '평일', '주말'])
    
    if day_type == '평일':
        df = df[df['DAY_TYPE'] == '평일']
    elif day_type == '주말':
        df = df[df['DAY_TYPE'] == '주말']

st.sidebar.markdown("---")

# 메인 대시보드
col1, col2, col3, col4 = st.columns(4)

# KPI 지표
with col1:
    total_stations = df['STATN_NM'].nunique() if 'STATN_NM' in df.columns else 0
    st.metric("총 역 수", f"{total_stations:,}")

with col2:
    total_lines = df['LN_NM'].nunique() if 'LN_NM' in df.columns else 0
    st.metric("총 노선 수", f"{total_lines}")

with col3:
    # 승차 인원 계산
    boarding_cols = [col for col in df.columns if 'GET_ON_NOPE' in col]
    if boarding_cols:
        total_boarding = df[boarding_cols].sum().sum()
        st.metric("총 승차 인원", f"{total_boarding:,.0f}")
    else:
        st.metric("총 승차 인원", "N/A")

with col4:
    # 하차 인원 계산
    alighting_cols = [col for col in df.columns if 'GET_OFF_NOPE' in col]
    if alighting_cols:
        total_alighting = df[alighting_cols].sum().sum()
        st.metric("총 하차 인원", f"{total_alighting:,.0f}")
    else:
        st.metric("총 하차 인원", "N/A")

st.markdown("---")

# 탭으로 구분된 분석 뷰
tab1, tab2, tab3, tab4 = st.tabs(["📈 시간대별 분석", "📊 요일별 분석", "🏆 역별 순위", "🔥 히트맵"])

with tab1:
    st.subheader("⏰ 시간대별 이용 패턴")
    
    # 시간대별 데이터 집계
    boarding_cols = [col for col in df.columns if 'GET_ON_NOPE' in col]
    alighting_cols = [col for col in df.columns if 'GET_OFF_NOPE' in col]
    
    if boarding_cols and alighting_cols:
        hourly_data = []
        for hour in range(4, 25):  # 4시~24시
            hour_str = f"{hour:02d}"
            boarding_col = f'HR_{hour_str}_GET_ON_NOPE'
            alighting_col = f'HR_{hour_str}_GET_OFF_NOPE'
            
            if boarding_col in df.columns and alighting_col in df.columns:
                hourly_data.append({
                    '시간대': f'{hour}시',
                    '승차': df[boarding_col].sum(),
                    '하차': df[alighting_col].sum()
                })
        
        hourly_df = pd.DataFrame(hourly_data)
        
        # Plotly 라인 차트
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hourly_df['시간대'], 
            y=hourly_df['승차'],
            mode='lines+markers',
            name='승차',
            line=dict(color='#1f77b4', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=hourly_df['시간대'], 
            y=hourly_df['하차'],
            mode='lines+markers',
            name='하차',
            line=dict(color='#ff7f0e', width=3)
        ))
        
        fig.update_layout(
            title="시간대별 승하차 인원",
            xaxis_title="시간대",
            yaxis_title="인원 (명)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 데이터 테이블
        with st.expander("📋 상세 데이터 보기"):
            st.dataframe(hourly_df, use_container_width=True)

with tab2:
    st.subheader("📅 요일별 이용 패턴")
    
    if 'WEEKDAY_KR' in df.columns and boarding_cols:
        weekday_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        
        weekday_data = []
        for weekday in weekday_order:
            weekday_df = df[df['WEEKDAY_KR'] == weekday]
            if len(weekday_df) > 0:
                total_boarding = weekday_df[boarding_cols].sum().sum()
                total_alighting = weekday_df[alighting_cols].sum().sum()
                weekday_data.append({
                    '요일': weekday,
                    '승차': total_boarding,
                    '하차': total_alighting,
                    '총합': total_boarding + total_alighting
                })
        
        weekday_df = pd.DataFrame(weekday_data)
        
        # Plotly 바 차트
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weekday_df['요일'],
            y=weekday_df['승차'],
            name='승차',
            marker_color='#1f77b4'
        ))
        fig.add_trace(go.Bar(
            x=weekday_df['요일'],
            y=weekday_df['하차'],
            name='하차',
            marker_color='#ff7f0e'
        ))
        
        fig.update_layout(
            title="요일별 승하차 인원",
            xaxis_title="요일",
            yaxis_title="인원 (명)",
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 상세 데이터 보기"):
            st.dataframe(weekday_df, use_container_width=True)

with tab3:
    st.subheader("🏆 역별 이용 순위 TOP 20")
    
    if 'STATN_NM' in df.columns and boarding_cols:
        # 역별 총 승하차 인원 계산
        station_data = df.groupby('STATN_NM').agg({
            **{col: 'sum' for col in boarding_cols},
            **{col: 'sum' for col in alighting_cols}
        }).reset_index()
        
        station_data['총승차'] = station_data[boarding_cols].sum(axis=1)
        station_data['총하차'] = station_data[alighting_cols].sum(axis=1)
        station_data['총이용'] = station_data['총승차'] + station_data['총하차']
        
        # TOP 20
        top20 = station_data.nlargest(20, '총이용')[['STATN_NM', '총승차', '총하차', '총이용']]
        top20 = top20.sort_values('총이용', ascending=True)  # 수평 막대 그래프용
        
        # Plotly 수평 막대 그래프
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=top20['STATN_NM'],
            x=top20['총승차'],
            name='승차',
            orientation='h',
            marker_color='#1f77b4'
        ))
        fig.add_trace(go.Bar(
            y=top20['STATN_NM'],
            x=top20['총하차'],
            name='하차',
            orientation='h',
            marker_color='#ff7f0e'
        ))
        
        fig.update_layout(
            title="역별 이용 순위 TOP 20",
            xaxis_title="인원 (명)",
            yaxis_title="역명",
            barmode='stack',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 상세 데이터 보기"):
            st.dataframe(top20.sort_values('총이용', ascending=False), use_container_width=True)

with tab4:
    st.subheader("🔥 역별 시간대별 히트맵 (TOP 30)")
    
    if 'STATN_NM' in df.columns and boarding_cols:
        # TOP 30 역 선택
        station_totals = df.groupby('STATN_NM')[boarding_cols + alighting_cols].sum().sum(axis=1)
        top30_stations = station_totals.nlargest(30).index.tolist()
        
        # 히트맵 데이터 준비
        heatmap_data = []
        for station in top30_stations:
            station_df = df[df['STATN_NM'] == station]
            row = {'역명': station}
            for hour in range(4, 25):
                boarding_col = f'HR_{hour:02d}_GET_ON_NOPE'
                alighting_col = f'HR_{hour:02d}_GET_OFF_NOPE'
                if boarding_col in df.columns and alighting_col in df.columns:
                    total = station_df[boarding_col].sum() + station_df[alighting_col].sum()
                    row[f'{hour}시'] = total
            heatmap_data.append(row)
        
        heatmap_df = pd.DataFrame(heatmap_data)
        heatmap_df = heatmap_df.set_index('역명')
        
        # Plotly 히트맵
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_df.values,
            x=heatmap_df.columns,
            y=heatmap_df.index,
            colorscale='YlOrRd',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="역별 시간대별 이용 패턴",
            xaxis_title="시간대",
            yaxis_title="역명",
            height=800
        )
        
        st.plotly_chart(fig, use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>서울시 지하철 이용 패턴 분석 대시보드 v1.0</p>
        <p>데이터 출처: 서울 열린데이터광장</p>
    </div>
""", unsafe_allow_html=True)
