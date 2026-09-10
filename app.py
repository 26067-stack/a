import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. 페이지 기본 설정 & 커스텀 CSS (게임풍 테마)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Plague Simulator Web",
    page_icon="☣️",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        color: #FF2B2B;
        text-align: center;
        font-weight: bold;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #AAAAAA;
        margin-bottom: 25px;
    }
    .stMetric {
        background-color: #1E1E2E;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #333344;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>☣️ Plague Simulator (전염병 시뮬레이터)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>전염병 주식회사 모티브: 변수를 조절하여 전 세계 감염 및 인류 대응을 시뮬레이션하세요.</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 사이드바 - 변인 설정 (Plague Inc. 특성 시스템)
# ---------------------------------------------------------
st.sidebar.header("🔬 1. 병원체 기본 설정")
pathogen_type = st.sidebar.selectbox("병원체 종류", ["박테리아", "바이러스", "곰팡이", "변종 프리온"])

# 병원체 기본 패시브 데이터
type_mods = {
    "박테리아": {"trans": 1.0, "incub": 1.0, "cure": 1.0},
    "바이러스": {"trans": 1.3, "incub": 0.8, "cure": 0.9},  # 빠른 전파력
    "곰팡이": {"trans": 0.7, "incub": 1.5, "cure": 1.2},    # 느리지만 생존력 높음
    "변종 프리온": {"trans": 0.9, "incub": 2.0, "cure": 0.6} # 치료제 개발 어려움
}
mod = type_mods[pathogen_type]

st.sidebar.header("🧬 2. 전파 & 증상 변인")
transmissibility = st.sidebar.slider("전염성 (Transmission)", 0.1, 3.0, 1.2) * mod["trans"]
incubation_period = st.sidebar.slider("잠복기 (일 수)", 1, 14, 5) * mod["incub"]
lethality = st.sidebar.slider("치사율 (%)", 0.0, 10.0, 1.5) / 100.0
heat_cold_resistance = st.sidebar.slider("기후/환경 저항성", 0.5, 2.0, 1.0)

st.sidebar.header("🌐 3. 인류의 대응 (방역 & 치료제)")
initial_pop = st.sidebar.number_input("전 세계 인구 수", value=10000000, step=1000000)
cure_research_speed = st.sidebar.slider("치료제 기본 연구 속도", 0.1, 2.0, 1.0) / mod["cure"]
lockdown_threshold = st.sidebar.slider("봉쇄령 발동 기준 (감염자 비율 %)", 1, 50, 10) / 100.0
simulation_days = st.sidebar.slider("시뮬레이션 기간 (일)", 30, 365, 180)

# ---------------------------------------------------------
# 3. SEIRD + Cure 수식 시뮬레이션 엔진
# ---------------------------------------------------------
def run_simulation():
    dt = 1 # 1일 단위
    days = np.arange(0, simulation_days, dt)
    
    # 초기 인구 배분
    S = initial_pop - 100 # 건강한 대상자
    E = 100               # 노출/잠복자
    I = 0                 # 증상 발현 감염자
    R = 0                 # 회복/면역자
    D = 0                 # 사망자
    
    cure_progress = 0.0   # 백신 개발률 (0% ~ 100%)
    
    history = {
        "Day": [], "Susceptible": [], "Exposed": [], 
        "Infected": [], "Recovered": [], "Deceased": [], "Cure": []
    }
    
    sigma = 1.0 / incubation_period # 잠복기 -> 감염자 전환율
    gamma = 0.1                      # 기본 회복률 (평균 10일 후 회복)
    
    for day in days:
        total_pop = S + E + I + R
        if total_pop <= 0:
            break
            
        current_infected_ratio = (E + I) / initial_pop
        
        # 1. 인류 방역 개입 (봉쇄령 영향)
        effective_trans = transmissibility * heat_cold_resistance
        if current_infected_ratio > lockdown_threshold:
            effective_trans *= 0.4 # 봉쇄령 발동 시 전염성 60% 감소
            
        # 2. 치료제 개발 알고리즘
        if current_infected_ratio > 0.01: # 감염률 1% 이상 시 개발 시작
            cure_increment = (cure_research_speed * (1 + current_infected_ratio * 2)) * 0.5
            cure_progress = min(100.0, cure_progress + cure_increment)
            
        # 치료제 완충 효과 (개발률이 올라갈수록 회복률 증가 & 전염성 감소)
        cure_effect = cure_progress / 100.0
        current_gamma = gamma + (cure_effect * 0.3)
        effective_trans *= (1.0 - cure_effect * 0.7)
        
        # 3. 미분 방정식 미세 업데이트 (SEIRD)
        beta = effective_trans
        mu = lethality # 치사율
        
        new_exposed = beta * S * I / initial_pop
        new_infected = sigma * E
        new_recovered = current_gamma * I * (1 - mu)
        new_deaths = current_gamma * I * mu
        
        S = max(0, S - new_exposed)
        E = max(0, E + new_exposed - new_infected)
        I = max(0, I + new_infected - new_recovered - new_deaths)
        R = min(initial_pop, R + new_recovered)
        D = min(initial_pop, D + new_deaths)
        
        # 기록 저장
        history["Day"].append(day)
        history["Susceptible"].append(int(S))
        history["Exposed"].append(int(E))
        history["Infected"].append(int(I))
        history["Recovered"].append(int(R))
        history["Deceased"].append(int(D))
        history["Cure"].append(round(cure_progress, 1))

    return pd.DataFrame(history)

# 시뮬레이션 실행
df = run_simulation()

# ---------------------------------------------------------
# 4. 결과 메트릭 카드 표시
# ---------------------------------------------------------
final_row = df.iloc[-1]
max_infected = df["Infected"].max()
max_infected_day = df.loc[df["Infected"] == max_infected, "Day"].values[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("총 사망자 수", f"{final_row['Deceased']:,} 명", delta_color="inverse")
col2.metric("최고 동시 감염자", f"{max_infected:,} 명 (Day {max_infected_day})")
col3.metric("최종 완치자 수", f"{final_row['Recovered']:,} 명")
col4.metric("치료제 개발률", f"{final_row['Cure']}%")

st.markdown("---")

# ---------------------------------------------------------
# 5. 시각화 (Plotly 인터랙티브 그래프)
# ---------------------------------------------------------
col_left, col_right = st.columns([3, 1])

with col_left:
    st.subheader("📈 인구 변화 추이 그래프")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Day"], y=df["Susceptible"], name="생존자 (S)", line=dict(color='#2B5C8F')))
    fig.add_trace(go.Scatter(x=df["Day"], y=df["Exposed"], name="잠복기 (E)", line=dict(color='#E59866')))
    fig.add_trace(go.Scatter(x=df["Day"], y=df["Infected"], name="감염자 (I)", line=dict(color='#E74C3C', width=3)))
    fig.add_trace(go.Scatter(x=df["Day"], y=df["Recovered"], name="완치자 (R)", line=dict(color='#27AE60')))
    fig.add_trace(go.Scatter(x=df["Day"], y=df["Deceased"], name="사망자 (D)", line=dict(color='#7F8C8D')))
    
    fig.update_layout(
        xaxis_title="경과 일수 (Day)",
        yaxis_title="인구 수",
        template="plotly_dark",
        height=450,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🚨 주요 사건 로그")
    log_box = []
    
    # 주요 이벤트 체크
    lockdown_day = df[df["Infected"] >= initial_pop * lockdown_threshold]["Day"].min()
    cure_50_day = df[df["Cure"] >= 50.0]["Day"].min()
    cure_100_day = df[df["Cure"] >= 100.0]["Day"].min()
    
    if pd.notna(lockdown_day):
        log_box.append(f"🔒 **Day {int(lockdown_day)}**: 감염률 기준치 도달! 전 세계 **국경 봉쇄령** 발동.")
    if pd.notna(cure_50_day):
        log_box.append(f"🧪 **Day {int(cure_50_day)}**: 치료제 개발 **50%** 완료.")
    if pd.notna(cure_100_day):
        log_box.append(f"💉 **Day {int(cure_100_day)}**: **치료제 완제 개발!** 백신 보급 시작.")
    else:
        log_box.append("⚠️ **경고**: 백신이 개발되기 전에 피해가 극대화되었습니다.")
        
    for log in log_box:
        st.warning(log)

# 데이터 프레임 다운로드 기능
st.download_button(
    label="📥 시뮬레이션 결과 CSV 다운로드",
    data=df.to_csv(index=False).encode('utf-8-sig'),
    file_name="plague_simulation_result.csv",
    mime="text/csv"
)
