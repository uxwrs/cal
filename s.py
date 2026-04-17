import streamlit as st
import math

# 페이지 설정
st.set_page_config(page_title="멀티 기능 계산기", page_icon="🧮")

st.title("🧮 Advanced Calculator")
st.write("사칙연산부터 삼각함수까지 가능한 계산기입니다.")

# 사이드바에서 연산 종류 선택
operation = st.sidebar.selectbox(
    "연산 종류를 선택하세요",
    ("사칙연산 & 나머지", "지수 & 로그", "삼각함수")
)

# 결과 출력을 위한 함수
def display_result(result):
    st.success(f"### 결과: {result}")

# 1. 사칙연산 및 모듈러(나머지) 연산
if operation == "사칙연산 & 나머지":
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("첫 번째 숫자(a)", value=0.0)
    with col2:
        num2 = st.number_input("두 번째 숫자(b)", value=0.0)
    
    op = st.selectbox("연산자", ("+", "-", "*", "/", "% (나머지)"))
    
    if st.button("계산하기"):
        if op == "+":
            display_result(num1 + num2)
        elif op == "-":
            display_result(num1 - num2)
        elif op == "*":
            display_result(num1 * num2)
        elif op == "/":
            if num2 != 0:
                display_result(num1 / num2)
            else:
                st.error("0으로 나눌 수 없습니다.")
        elif op == "% (나머지)":
            display_result(num1 % num2)

# 2. 지수 및 로그 연산
elif operation == "지수 & 로그":
    col1, col2 = st.columns(2)
    mode = st.radio("선택", ("지수 연산 (a^b)", "로그 연산"))
    
    if mode == "지수 연산 (a^b)":
        base = st.number_input("밑(a)", value=2.0)
        exp = st.number_input("지수(b)", value=10.0)
        if st.button("계산하기"):
            display_result(math.pow(base, exp))
            
    elif mode == "로그 연산":
        x = st.number_input("진수(x)", value=100.0)
        base = st.number_input("밑(base) - 상용로그는 10, 자연로그는 e(2.718...)", value=10.0)
        if st.button("계산하기"):
            if x > 0 and base > 0 and base != 1:
                display_result(math.log(x, base))
            else:
                st.error("로그 조건을 확인하세요 (진수 > 0, 밑 > 0 및 밑 != 1)")

# 3. 삼각함수 연산
elif operation == "삼각함수":
    angle_type = st.radio("각도 단위 선택", ("Degree (도)", "Radian (라디안)"))
    angle = st.number_input("각도를 입력하세요", value=0.0)
    func = st.selectbox("함수 선택", ("sin", "cos", "tan"))
    
    # 계산을 위해 라디안으로 변환
    rad = math.radians(angle) if angle_type == "Degree (도)" else angle
    
    if st.button("계산하기"):
        if func == "sin":
            display_result(math.sin(rad))
        elif func == "cos":
            display_result(math.cos(rad))
        elif func == "tan":
            # tan(90도) 등 정의되지 않는 구간 처리
            if angle_type == "Degree (도)" and (angle % 180 == 90):
                st.error("해당 각도에서 tan 값은 정의되지 않습니다.")
            else:
                display_result(math.tan(rad))

st.sidebar.markdown("---")
st.sidebar.write("Created with Streamlit")
