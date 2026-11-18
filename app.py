import streamlit as st
import pandas as pd

# =========================================================
# 1. 페이지 설정 및 디자인
# =========================================================
st.set_page_config(
    page_title="LOVE TYPE TEST",
    page_icon="💜",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #F8F5FF 0%, #FDFBFF 100%);
    }
    .main .block-container {
        max-width: 850px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 { color: #4B347A; }
    .main-title {
        text-align: center;
        color: #6941A5;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #8876A8;
        font-size: 15px;
        margin-bottom: 30px;
    }
    .question-card {
        background-color: #FFFFFF;
        border: 1px solid #E8DDF9;
        border-radius: 16px;
        padding: 20px 22px;
        margin: 14px 0 8px 0;
        box-shadow: 0 3px 12px rgba(105, 65, 165, 0.06);
    }
    .question-number {
        color: #9671C9;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 7px;
    }
    .question-text {
        color: #35264D;
        font-size: 17px;
        font-weight: 700;
        line-height: 1.5;
    }
    .type-code {
        text-align: center;
        color: #7546B8;
        font-size: 54px;
        font-weight: 900;
        letter-spacing: 5px;
        padding: 15px;
    }
    .result-card {
        background: white;
        border: 1px solid #E6D9F7;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(105, 65, 165, 0.07);
    }
    .small-caption {
        color: #8B7AA5;
        font-size: 13px;
    }
    div.stButton > button {
        background-color: #8054BD;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 22px;
        font-weight: 700;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #68409F;
        color: white;
        border: none;
    }
    [data-testid="stProgressBar"] > div > div {
        background-color: #9569CF;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. 성향 축 및 질문 데이터
# 각 축 점수 50 이상이면 첫 번째 성향, 미만이면 두 번째 성향
# =========================================================
AXES = {
    "E": {
        "name": "표현 방식",
        "first": "Expressive",
        "second": "Introverted",
        "first_desc": "감정과 애정을 적극적으로 표현",
        "second_desc": "감정을 신중하고 조용하게 표현"
    },
    "A": {
        "name": "친밀감 형성",
        "first": "Attached",
        "second": "Self-directed",
        "first_desc": "정서적 친밀감과 확인을 중시",
        "second_desc": "독립성과 개인 공간을 중시"
    },
    "C": {
        "name": "갈등 대응",
        "first": "Communicative",
        "second": "Deliberate",
        "first_desc": "대화와 조율로 갈등 해결",
        "second_desc": "시간을 두고 생각한 후 대응"
    },
    "B": {
        "name": "관계 자율성",
        "first": "Bond-oriented",
        "second": "Trust-oriented",
        "first_desc": "함께하는 경험과 공동체 중시",
        "second_desc": "자율성과 상호 신뢰 중시"
    }
}

# 라디오 11문항 + 슬라이더 4문항 = 총 15문항
QUESTIONS = [
    {
        "axis": "E", "kind": "radio", "reverse": False,
        "question": "연인에게 좋아하는 마음이 생기면?",
        "options": [
            "먼저 적극적으로 표현하는 편이다",
            "비교적 자연스럽게 표현한다",
            "상황에 따라 다르다",
            "상대방의 반응을 살펴보는 편이다",
            "마음이 있어도 표현하는 데 시간이 걸린다"
        ]
    },
    {
        "axis": "E", "kind": "radio", "reverse": False,
        "question": "연인과 하루 동안 연락이 뜸했다면?",
        "options": [
            "먼저 연락해서 대화를 이어간다",
            "가볍게 안부를 묻는다",
            "크게 신경 쓰지 않는다",
            "상대방이 연락하기를 기다린다",
            "연락을 먼저 시작하는 일이 많지 않다"
        ]
    },
    {
        "axis": "E", "kind": "radio", "reverse": False,
        "question": "연인에게 서운한 일이 생겼을 때?",
        "options": [
            "바로 감정을 표현한다",
            "가능하면 빠르게 이야기한다",
            "상황을 보고 결정한다",
            "혼자 생각을 정리한 뒤 말한다",
            "굳이 말하지 않고 넘기는 편이다"
        ]
    },
    {
        "axis": "E", "kind": "slider", "reverse": False,
        "question": "연인에게 애정 표현을 얼마나 자주 하는 편인가요?",
        "min": 0, "max": 100, "default": 50,
        "left": "거의 표현하지 않음",
        "right": "매우 자주 표현함"
    },
    {
        "axis": "A", "kind": "radio", "reverse": False,
        "question": "연인과 연락이 평소보다 줄어들면?",
        "options": [
            "관계에 문제가 생겼는지 걱정된다",
            "조금 신경 쓰이고 이유가 궁금하다",
            "상황에 따라 다르다",
            "상대방에게 개인적인 시간이 필요하다고 생각한다",
            "각자 시간을 보내는 것이 자연스럽다"
        ]
    },
    {
        "axis": "A", "kind": "radio", "reverse": False,
        "question": "연인과 함께하는 시간에 대해?",
        "options": [
            "가능하면 많은 시간을 함께 보내고 싶다",
            "자주 만나는 것이 좋다",
            "적당한 균형이 중요하다",
            "각자의 일정도 충분히 중요하다",
            "각자 시간을 보내는 것이 더 편할 때가 많다"
        ]
    },
    {
        "axis": "A", "kind": "radio", "reverse": False,
        "question": "연인이 혼자만의 시간을 원한다고 하면?",
        "options": [
            "나와 멀어지는 것 같아 서운하다",
            "조금 아쉽지만 이해하려고 한다",
            "상황에 따라 다르다",
            "개인 시간이 필요할 수 있다고 생각한다",
            "당연히 존중해야 한다고 생각한다"
        ]
    },
    {
        "axis": "A", "kind": "slider", "reverse": False,
        "question": "연애에서 정서적 친밀감과 애착을 얼마나 중요하게 생각하나요?",
        "min": 0, "max": 100, "default": 50,
        "left": "개인적인 독립성이 더 중요함",
        "right": "정서적 친밀감이 더 중요함"
    },
    {
        "axis": "C", "kind": "radio", "reverse": False,
        "question": "연인과 다툰 직후 가장 원하는 것은?",
        "options": [
            "바로 대화해서 해결하는 것",
            "가능한 빨리 서로의 입장을 확인하는 것",
            "상황에 따라 다르다",
            "잠시 시간을 갖고 생각하는 것",
            "감정이 가라앉을 때까지 대화를 미루는 것"
        ]
    },
    {
        "axis": "C", "kind": "radio", "reverse": False,
        "question": "갈등 상황에서 상대방이 대화를 피한다면?",
        "options": [
            "대화를 계속 시도한다",
            "이유를 물어보고 대화를 요청한다",
            "상대방의 반응을 살펴본다",
            "일단 시간을 준다",
            "상대방이 준비될 때까지 기다린다"
        ]
    },
    {
        "axis": "C", "kind": "radio", "reverse": False,
        "question": "연인과 의견이 다를 때?",
        "options": [
            "서로 이야기하며 합의점을 찾는다",
            "내 의견을 설명하고 조율한다",
            "상황에 따라 다르다",
            "각자의 생각을 정리할 시간이 필요하다",
            "굳이 결론을 내지 않아도 된다고 생각한다"
        ]
    },
    {
        "axis": "C", "kind": "slider", "reverse": False,
        "question": "갈등이 생겼을 때 즉시 대화로 해결하고 싶은 정도는?",
        "min": 0, "max": 100, "default": 50,
        "left": "시간을 두고 생각하고 싶음",
        "right": "바로 대화하고 싶음"
    },
    {
        "axis": "B", "kind": "radio", "reverse": False,
        "question": "연애를 시작한 후에도 친구와의 약속은?",
        "options": [
            "연인과 보내는 시간을 우선한다",
            "연인과 친구 모두 중요하다",
            "일정에 따라 조정한다",
            "연애 전과 비슷하게 유지한다",
            "개인적인 인간관계를 독립적으로 유지한다"
        ]
    },
    {
        "axis": "B", "kind": "radio", "reverse": False,
        "question": "연인이 나와 다른 취미나 생활방식을 가지고 있다면?",
        "options": [
            "가능하면 함께하고 싶다",
            "서로 공유할 수 있는 부분을 찾는다",
            "상황에 따라 다르다",
            "각자의 취향을 존중한다",
            "서로의 영역을 간섭하지 않는 것이 좋다"
        ]
    },
    {
        "axis": "B", "kind": "slider", "reverse": True,
        "question": "연애 중에도 개인의 자유와 독립성을 얼마나 중요하게 생각하나요?",
        "min": 0, "max": 100, "default": 50,
        "left": "함께하는 생활이 더 중요함",
        "right": "개인의 자율성이 더 중요함"
    }
]

# =========================================================
# 3. 16가지 유형 설명
# 유형 코드 순서: E/A/C/B
# =========================================================
TYPE_INFO = {
    "EACB": ("다정한 소통가", "애정 표현과 정서적 교류가 풍부하고, 갈등도 대화로 풀어가는 편이에요. 함께하는 시간을 소중하게 생각하는 따뜻한 유형이에요."),
    "EACT": ("자유로운 동반자", "애정을 적극적으로 표현하면서도 서로의 자율성을 존중해요. 가까우면서도 각자의 삶을 지켜가는 관계를 선호해요."),
    "EADB": ("신중한 애정파", "마음을 적극적으로 표현하지만 갈등이 생기면 생각할 시간이 필요해요. 관계의 안정감과 함께하는 경험을 중요하게 여겨요."),
    "EADT": ("독립적인 표현가", "애정 표현은 솔직하지만 갈등 상황에서는 한 걸음 물러서서 생각해요. 서로의 영역을 존중하는 관계를 선호해요."),
    "ASCB": ("밀착형 해결사", "정서적 친밀감을 중요하게 생각하고 문제가 생기면 대화로 해결하려 해요. 함께 문제를 극복하는 관계를 지향해요."),
    "ASCT": ("자율적인 공감가", "친밀한 정서적 유대감을 원하면서도 서로의 자유를 존중해요. 대화를 통해 건강한 관계를 만들어가는 편이에요."),
    "ASDB": ("깊은 유대형", "깊은 애착과 함께하는 시간을 중요하게 여기지만 갈등은 충분히 생각한 뒤 해결하고 싶어 해요."),
    "ASDT": ("조용한 동반자", "정서적 연결을 소중히 여기면서도 갈등 상황에서는 차분한 시간이 필요해요. 친밀함과 독립성의 균형을 추구해요."),
    "IECB": ("차분한 소통가", "감정을 조용히 표현하지만 갈등이 생기면 대화를 통해 풀고 싶어 해요. 관계 안에서 안정적인 교류를 선호해요."),
    "IECT": ("담백한 파트너", "감정을 과하게 드러내기보다 차분하게 표현해요. 대화와 자율성을 바탕으로 편안한 관계를 만들어가요."),
    "IEDB": ("생각하는 애정파", "감정을 신중하게 표현하고 갈등도 충분히 생각한 뒤 해결해요. 함께하는 안정적인 관계를 중요하게 생각해요."),
    "IEDT": ("독립적인 사색가", "감정을 천천히 표현하고 혼자 생각하는 시간을 중요하게 여겨요. 서로를 신뢰하고 간섭하지 않는 관계를 선호해요."),
    "ISCB": ("배려 깊은 조율가", "감정을 조용히 표현하지만 상대와의 정서적 유대감을 중요하게 생각해요. 갈등은 대화로 조심스럽게 풀어가요."),
    "ISCT": ("여유로운 조율가", "개인의 시간을 존중하면서도 갈등은 대화로 해결하려 해요. 부담스럽지 않고 안정적인 관계를 선호해요."),
    "ISDB": ("내면의 동반자", "깊은 정서적 유대를 원하지만 감정 표현은 신중해요. 갈등이 생기면 생각을 정리한 뒤 관계를 회복하려 해요."),
    "ISDT": ("자유로운 관찰자", "감정 표현과 관계 모두에서 신중하고 독립적인 편이에요. 서로를 믿고 각자의 삶을 존중하는 관계를 선호해요.")
}

# =========================================================
# 4. 세션 상태 초기화 및 재검사 함수
# =========================================================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

def reset_test():
    """응답 위젯 상태와 결과를 초기화한다."""
    for i in range(len(QUESTIONS)):
        key = f"q_{i}"
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.submitted = False

# =========================================================
# 5. 점수 계산 함수
# =========================================================
def calculate_scores():
    """축별 문항 점수의 평균을 0~100 범위로 계산한다."""
    axis_scores = {axis: [] for axis in AXES}

    for i, q in enumerate(QUESTIONS):
        answer = st.session_state.get(f"q_{i}")
        if answer is None:
            continue

        if q["kind"] == "radio":
            # 첫 번째 선택지 100점, 마지막 선택지 0점
            score = (4 - answer) * 25
        else:
            score = answer

        if q.get("reverse", False):
            score = 100 - score

        axis_scores[q["axis"]].append(score)

    return {
        axis: (sum(values) / len(values) if values else 50)
        for axis, values in axis_scores.items()
    }

def get_type_code(scores):
    """각 축의 50점 기준으로 4자리 유형 코드를 생성한다."""
    code = ""
    opposite_letters = {"E": "I", "A": "S", "C": "D", "B": "T"}

    for axis in ["E", "A", "C", "B"]:
        code += axis if scores[axis] >= 50 else opposite_letters[axis]

    return code

# =========================================================
# 6. 상단 헤더
# =========================================================
st.markdown('<div class="main-title">💜 LOVE TYPE TEST</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">15개의 질문으로 알아보는 나의 연애 성향</div>', unsafe_allow_html=True)

st.markdown("""
<div class="result-card">
    <b style="color:#6941A5;">나의 연애 스타일은?</b>
    <p style="color:#76688A; margin-bottom:0;">
        정답은 없어요. 평소 연애 상황에서 나에게 더 가까운 선택지를 골라주세요.
        솔직하게 답할수록 나의 연애 성향을 더 잘 살펴볼 수 있어요.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 7. 질문 화면
# =========================================================
if not st.session_state.submitted:
    # 라디오 문항 응답 수를 진행률로 표시한다.
    # 슬라이더는 기본값이 있어도 사용자가 직접 조작하기 전까지 미응답으로 처리한다.
    answered = 0
    for i, q in enumerate(QUESTIONS):
        key = f"q_{i}"
        if q["kind"] == "radio":
            if st.session_state.get(key) is not None:
                answered += 1
        elif key in st.session_state:
            answered += 1

    progress = answered / len(QUESTIONS)
    st.markdown(f"**검사 진행률: {answered} / {len(QUESTIONS)}**")
    st.progress(progress)
    st.caption("각 질문에 가장 가까운 답변을 선택해주세요.")

    for i, q in enumerate(QUESTIONS):
        st.markdown(f"""
        <div class="question-card">
            <div class="question-number">QUESTION {i + 1:02d} / 15</div>
            <div class="question-text">{q["question"]}</div>
        </div>
        """, unsafe_allow_html=True)

        if q["kind"] == "radio":
            st.radio(
                label=f"질문 {i + 1} 선택",
                options=list(range(5)),
                format_func=lambda x, opts=q["options"]: opts[x],
                index=None,
                key=f"q_{i}",
                label_visibility="collapsed"
            )
        else:
            st.markdown(
                f"<div style='display:flex; justify-content:space-between;"
                f"color:#8B7AA5;font-size:13px;'>"
                f"<span>{q['left']}</span><span>{q['right']}</span></div>",
                unsafe_allow_html=True
            )
            st.slider(
                label=f"질문 {i + 1} 점수",
                min_value=q["min"],
                max_value=q["max"],
                value=q["default"],
                key=f"q_{i}",
                label_visibility="collapsed"
            )

    # 모든 라디오 질문에 응답했는지 확인
    all_answered = all(
        st.session_state.get(f"q_{i}") is not None
        for i, q in enumerate(QUESTIONS)
        if q["kind"] == "radio"
    )

    st.divider()
    if not all_answered:
        st.info("아직 답하지 않은 질문이 있어요. 모든 질문에 답해주세요.")

    if st.button("💜 나의 연애 유형 확인하기", disabled=not all_answered):
        st.session_state.submitted = True
        st.rerun()

# =========================================================
# 8. 결과 화면
# =========================================================
else:
    scores = calculate_scores()
    type_code = get_type_code(scores)
    type_name, type_description = TYPE_INFO[type_code]

    st.balloons()
    st.markdown(
        '<div style="text-align:center; color:#9671C9; font-weight:700;">YOUR LOVE TYPE</div>',
        unsafe_allow_html=True
    )
    st.markdown(f'<div class="type-code">{type_code}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="result-card" style="text-align:center;">'
        f'<h2 style="color:#6941A5;">{type_name}</h2>'
        f'<p style="color:#76688A; line-height:1.8;">{type_description}</p></div>',
        unsafe_allow_html=True
    )

    # 네 가지 성향을 가로 막대그래프로 표시
    st.subheader("💜 나의 연애 성향 분석")
    chart_data = []
    for axis, info in AXES.items():
        chart_data.append({
            "성향": info["name"],
            info["first"]: scores[axis],
            info["second"]: 100 - scores[axis]
        })

    chart_df = pd.DataFrame(chart_data).set_index("성향")
    st.bar_chart(chart_df, horizontal=True, height=280)
    st.caption("각 항목은 두 성향의 상대적인 점수를 나타내요. 50점을 기준으로 유형이 구분돼요.")

    # 축별 점수와 설명
    st.subheader("나의 4가지 성향")
    for axis, info in AXES.items():
        score = scores[axis]

        if score >= 50:
            selected = info["first"]
            description = info["first_desc"]
            opposite = info["second"]
        else:
            selected = info["second"]
            description = info["second_desc"]
            opposite = info["first"]

        st.markdown(f"""
        <div class="question-card">
            <div class="question-number">{info["name"]}</div>
            <b style="color:#6941A5; font-size:18px;">{selected}</b>
            <p style="color:#76688A; margin:7px 0;">{description}</p>
            <div style="background:#EEE7F8; height:8px; border-radius:10px;">
                <div style="background:#9569CF; width:{score}%;
                height:8px; border-radius:10px;"></div>
            </div>
            <div class="small-caption" style="margin-top:6px;">
                {selected} {score:.0f}% / {opposite} {100-score:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="result-card">
        <b style="color:#6941A5;">💡 결과를 해석할 때</b>
        <p style="color:#76688A; line-height:1.8;">
            이 결과는 현재 응답을 바탕으로 구성한 연애 성향 참고 자료예요.
            사람의 연애 방식은 상대방과의 관계, 경험, 상황에 따라 달라질 수 있어요.
            특정 유형이 더 좋거나 나쁜 것은 아니에요.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 다시 검사하기"):
        reset_test()
        st.rerun()
