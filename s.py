import streamlit as st
import math
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# 페이지 설정
st.set_page_config(page_title="멀티 툴 앱", page_icon="🎲")

# 사이드바 메인 메뉴
st.sidebar.title("🛠️ 메뉴 선택")
app_mode = st.sidebar.selectbox("사용할 기능을 선택하세요", ["계산기 모드", "확률 시뮬레이터", "그래프 생성기"])

# --- 1. 계산기 모드 로직 ---
if app_mode == "계산기 모드":
    st.title("🧮 Advanced Calculator")
    
    calc_operation = st.sidebar.radio(
        "연산 종류",
        ("사칙연산 & 나머지", "지수 & 로그", "삼각함수")
    )

    def display_result(result):
        st.success(f"### 결과: {result}")

    if calc_operation == "사칙연산 & 나머지":
        col1, col2 = st.columns(2)
        with col1: num1 = st.number_input("첫 번째 숫자(a)", value=0.0)
        with col2: num2 = st.number_input("두 번째 숫자(b)", value=0.0)
        op = st.selectbox("연산자", ("+", "-", "*", "/", "% (나머지)"))
        if st.button("계산하기"):
            if op == "+": display_result(num1 + num2)
            elif op == "-": display_result(num1 - num2)
            elif op == "*": display_result(num1 * num2)
            elif op == "/":
                if num2 != 0: display_result(num1 / num2)
                else: st.error("0으로 나눌 수 없습니다.")
            elif op == "% (나머지)": display_result(num1 % num2)

    elif calc_operation == "지수 & 로그":
        mode = st.radio("선택", ("지수 연산 (a^b)", "로그 연산"))
        if mode == "지수 연산 (a^b)":
            base = st.number_input("밑(a)", value=2.0)
            exp = st.number_input("지수(b)", value=10.0)
            if st.button("계산하기"): display_result(math.pow(base, exp))
        elif mode == "로그 연산":
            x = st.number_input("진수(x)", value=100.0)
            base = st.number_input("밑(base)", value=10.0)
            if st.button("계산하기"):
                if x > 0 and base > 0 and base != 1: display_result(math.log(x, base))
                else: st.error("로그 조건을 확인하세요.")

    elif calc_operation == "삼각함수":
        angle_type = st.radio("각도 단위", ("Degree (도)", "Radian (라디안)"))
        angle = st.number_input("각도 입력", value=0.0)
        func = st.selectbox("함수 선택", ("sin", "cos", "tan"))
        rad = math.radians(angle) if angle_type == "Degree (도)" else angle
        if st.button("계산하기"):
            if func == "sin": display_result(math.sin(rad))
            elif func == "cos": display_result(math.cos(rad))
            elif func == "tan":
                if angle_type == "Degree (도)" and (angle % 180 == 90): st.error("정의되지 않는 값입니다.")
                else: display_result(math.tan(rad))

# --- 2. 확률 시뮬레이터 모드 로직 ---
elif app_mode == "확률 시뮬레이터":
    st.title("🎲 확률 시뮬레이터")
    st.write("동전과 주사위를 던져 확률적 결과를 확인해보세요.")

    sim_type = st.selectbox("시뮬레이션 종류 선택", ["동전 던지기", "주사위 던지기"])

    if sim_type == "동전 던지기":
        st.subheader("🪙 동전 던지기")
        trials = st.number_input("던질 횟수를 입력하세요", min_value=1, max_value=10000, value=100)
        
        if st.button("시뮬레이션 실행"):
            results = [random.choice(["앞면", "뒷면"]) for _ in range(trials)]
            heads = results.count("앞면")
            tails = results.count("뒷면")
            
            # 결과 요약
            col1, col2 = st.columns(2)
            col1.metric("앞면 (Heads)", f"{heads}회", f"{heads/trials*100:.1f}%")
            col2.metric("뒷면 (Tails)", f"{tails}회", f"{tails/trials*100:.1f}%")
            
            # 차트 표시 - 막대 그래프
            st.subheader("📊 결과 분석")
            df = pd.DataFrame({"결과": ["앞면", "뒷면"], "횟수": [heads, tails]})
            
            col1, col2 = st.columns(2)
            with col1:
                fig_bar = px.bar(df, x="결과", y="횟수", title="막대 그래프", color="결과")
                st.plotly_chart(fig_bar, use_container_width=True)
            with col2:
                fig_pie = px.pie(df, values="횟수", names="결과", title="원형 그래프")
                st.plotly_chart(fig_pie, use_container_width=True)

    elif sim_type == "주사위 던지기":
        st.subheader("🎲 주사위 던지기")
        trials = st.number_input("던질 횟수를 입력하세요", min_value=1, max_value=10000, value=100)
        
        if st.button("시뮬레이션 실행"):
            results = [random.randint(1, 6) for _ in range(trials)]
            
            counts = {i: results.count(i) for i in range(1, 7)}
            
            # 결과 데이터프레임 및 차트
            df = pd.DataFrame(list(counts.items()), columns=["눈금", "횟수"])
            
            st.subheader("📊 결과 분석")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**상세 결과**")
                st.dataframe(df, hide_index=True)
            with col2:
                fig = px.bar(df, x="눈금", y="횟수", title="주사위 눈금별 빈도", 
                            labels={"눈금": "주사위 눈금", "횟수": "횟수"},
                            color="횟수", color_continuous_scale="Viridis")
                st.plotly_chart(fig, use_container_width=True)
            
            # 추가 그래프
            col1, col2 = st.columns(2)
            with col1:
                fig_pie = px.pie(df, values="횟수", names="눈금", title="눈금별 비율")
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                fig_line = px.line(df, x="눈금", y="횟수", title="눈금별 빈도 추이",
                                  markers=True, line_shape="spline")
                st.plotly_chart(fig_line, use_container_width=True)
            
            st.info(f"가장 많이 나온 눈금: {df.loc[df['횟수'].idxmax(), '눈금']}")

# --- 3. 그래프 생성기 모드 ---
elif app_mode == "그래프 생성기":
    st.title("📈 그래프 생성기")
    st.write("다양한 함수와 데이터를 시각화하세요.")
    
    graph_type = st.selectbox("그래프 종류를 선택하세요", 
                              ["함수 그래프 (sin, cos, tan)", "다항식 그래프", "산점도", "히스토그램"])
    
    if graph_type == "함수 그래프 (sin, cos, tan)":
        st.subheader("삼각함수 시각화")
        func_type = st.selectbox("함수 선택", ["sin", "cos", "tan"])
        
        col1, col2 = st.columns(2)
        with col1:
            x_min = st.number_input("X 최솟값", value=-10.0)
        with col2:
            x_max = st.number_input("X 최댓값", value=10.0)
        
        x = np.linspace(x_min, x_max, 1000)
        
        if func_type == "sin":
            y = np.sin(x)
            title = "y = sin(x)"
        elif func_type == "cos":
            y = np.cos(x)
            title = "y = cos(x)"
        else:  # tan
            y = np.tan(x)
            # tan 함수의 불연속점 처리
            y = np.where(np.abs(y) > 100, np.nan, y)
            title = "y = tan(x)"
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=func_type,
                                line=dict(color='blue', width=2)))
        fig.update_layout(title=title, xaxis_title="X", yaxis_title="Y", 
                         hovermode='x unified', height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "다항식 그래프":
        st.subheader("다항식 시각화")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("a (x² 계수)", value=1.0)
        with col2:
            b = st.number_input("b (x 계수)", value=0.0)
        with col3:
            c = st.number_input("c (상수항)", value=0.0)
        
        col1, col2 = st.columns(2)
        with col1:
            x_min = st.number_input("X 최솟값", value=-10.0, key="poly_min")
        with col2:
            x_max = st.number_input("X 최댓값", value=10.0, key="poly_max")
        
        x = np.linspace(x_min, x_max, 1000)
        y = a * x**2 + b * x + c
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='함수',
                                line=dict(color='green', width=2)))
        
        # 꼭짓점 표시
        if a != 0:
            x_vertex = -b / (2 * a)
            y_vertex = a * x_vertex**2 + b * x_vertex + c
            fig.add_trace(go.Scatter(x=[x_vertex], y=[y_vertex], mode='markers',
                                    marker=dict(size=10, color='red'),
                                    name='꼭짓점'))
        
        fig.update_layout(title=f"y = {a}x² + {b}x + {c}", xaxis_title="X", 
                         yaxis_title="Y", hovermode='x unified', height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "산점도":
        st.subheader("산점도 생성")
        
        num_points = st.number_input("데이터 포인트 개수", min_value=10, max_value=1000, value=100)
        noise_level = st.slider("노이즈 수준", 0.0, 2.0, 0.5)
        
        x = np.random.uniform(0, 10, num_points)
        y = 2 * x + 5 + np.random.normal(0, noise_level, num_points)
        
        df = pd.DataFrame({"X": x, "Y": y})
        
        fig = px.scatter(df, x="X", y="Y", title="산점도",
                        trendline="ols", trendline_color_override="red")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "히스토그램":
        st.subheader("히스토그램")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            num_data = st.number_input("데이터 개수", min_value=100, max_value=10000, value=1000)
        with col2:
            bins = st.number_input("구간 개수", min_value=5, max_value=100, value=30)
        with col3:
            distribution = st.selectbox("분포", ["정규분포", "균등분포", "지수분포"])
        
        if distribution == "정규분포":
            data = np.random.normal(50, 15, num_data)
            dist_name = "정규분포 (μ=50, σ=15)"
        elif distribution == "균등분포":
            data = np.random.uniform(0, 100, num_data)
            dist_name = "균등분포 (0-100)"
        else:
            data = np.random.exponential(20, num_data)
            dist_name = "지수분포 (λ=0.05)"
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=data, nbinsx=bins, name='빈도',
                                  marker=dict(color='skyblue', line=dict(color='navy', width=1))))
        
        fig.update_layout(title=f"히스토그램 ({dist_name})", xaxis_title="값", 
                         yaxis_title="빈도", height=500)
        st.plotly_chart(fig, use_container_width=True)

# 하단 공통 정보
st.sidebar.markdown("---")
st.sidebar.info("버전: 3.0 (그래프 생성기 추가)")
