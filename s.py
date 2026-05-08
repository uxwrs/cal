import streamlit as st
import math
import random
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="멀티 툴 앱", page_icon="🎲")

# 사이드바 메인 메뉴
st.sidebar.title("🛠️ 메뉴 선택")
app_mode = st.sidebar.selectbox("사용할 기능을 선택하세요", ["계산기 모드", "확률 시뮬레이터"])

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
            
            # 차트 표시
            df = pd.DataFrame({"결과": ["앞면", "뒷면"], "횟수": [heads, tails]})
            st.bar_chart(df.set_index("결과"))

    elif sim_type == "주사위 던지기":
        st.subheader("🎲 주사위 던지기")
        trials = st.number_input("던질 횟수를 입력하세요", min_value=1, max_value=10000, value=100)
        
        if st.button("시뮬레이션 실행"):
            results = [random.randint(1, 6) for _ in range(trials)]
            
            counts = {i: results.count(i) for i in range(1, 7)}
            
            # 결과 데이터프레임 및 차트
            df = pd.DataFrame(list(counts.items()), columns=["눈금", "횟수"])
            
            # 표와 차트 배치
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write("**상세 결과**")
                st.dataframe(df, hide_index=True)
            with col2:
                st.bar_chart(df.set_index("눈금"))
            
            st.info(f"가장 많이 나온 눈금: {df.loc[df['횟수'].idxmax(), '눈금']}")

# 하단 공통 정보
st.sidebar.markdown("---")
st.sidebar.info("버전: 2.0 (확률 시뮬레이터 추가)")
