"""
K-EXAONE 채팅 UI 예제
Streamlit을 사용한 간단한 채팅 인터페이스

설치 방법:
pip install streamlit openai

실행 방법:
streamlit run app.py
"""

import streamlit as st
from openai import OpenAI
import os

# 페이지 설정
st.set_page_config(page_title="K-EXAONE Chat", page_icon="🤖", layout="wide")

# API 설정
BASE_URL = "https://api.friendli.ai/serverless/v1"
MODEL = "LGAI-EXAONE/K-EXAONE-236B-A23B"

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thinking_mode" not in st.session_state:
    st.session_state.thinking_mode = True

if "auto_send" not in st.session_state:
    st.session_state.auto_send = False

if "api_key" not in st.session_state:
    st.session_state.api_key = ""


# OpenAI 클라이언트 초기화
@st.cache_resource
def get_client(api_key):
    return OpenAI(
        api_key=api_key,
        base_url=BASE_URL,
    )


# 프롬프트 예제
PROMPT_EXAMPLES = {
    "🧠 추론 능력 테스트": """다음 논리 퍼즐을 단계별로 해결해주세요:

문제: 5명의 사람(A, B, C, D, E)가 일렬로 서 있습니다.
- A는 C의 바로 옆에 서 있습니다.
- B는 D의 왼쪽에 서 있습니다.
- E는 양 끝 중 한 곳에 서 있습니다.
- C는 E의 오른쪽에 서 있습니다.

정확한 서 있는 순서를 대로로 설명하고, 각 단계의 추론 과정을 보여주세요.""",
    "📊 수학 문제 해결": """다음 수학 문제를 단계별로 해결해주세요:

문제: 한 회사에서 직원들에게 보너스를 분배하려고 합니다.
- 첫 번째 직원은 전체 보너스의 1/3을 받습니다.
- 두 번째 직원은 남은 금액의 1/4을 받습니다.
- 세 번째 직원은 그 다음 남은 금액의 1/5를 받습니다.
- 마지막으로 남은 금액은 $120,000입니다.

초기 전체 보너스 금액과 각 직원이 받은 금액을 계산해주세요.""",
    "📚 장문서 요약 테스트": """다음 긴 텍스트를 읽고 핵심 내용을 3문장으로 요약해주세요:

[텍스트 시작]
인공지능(AI)은 컴퓨터 시스템이 인간의 지능을 모방하도록 만드는 기술입니다. 기계학습, 딥러닝, 자연어 처리 등 다양한 하위 분야를 포함합니다. 최근 대규모 언어 모델(LLM)의 발전으로 AI는 텍스트 생성, 번역, 요약, 질문 답변 등 다양한 작업에서 인간 수준 이상의 성능을 보이고 있습니다. 특히 OpenAI의 GPT 시리즈, 구글의 Gemini, 알리바바의 Qwen, 그리고 LG의 K-EXAONE 등 경쟁 모델들이 속속 등장하며 AI 기술 경쟁이 치열해지고 있습니다. 한편으로는 AI가 일자리를 대체할 것이라는 우려와 함께, 다른 한편으로는 새로운 기회를 창출할 것이라는 기대가 공존합니다. 전문가들은 AI 활용 능력이 미래 직업 시장에서 핵심 역량이 될 것이라고 전망합니다.
[텍스트 끝]

이 텍스트를 바탕으로: 1) AI 기술의 현 상황, 2) 주요 모델들, 3) 사회적 영향을 포함하여 요약해주세요.""",
    "🇰🇷 한국어 문화 맥락 이해": """다음 질문에 한국의 문화적, 역사적 맥락을 반영하여 답변해주세요:

질문: 한국의 '정월대보름'에 대해 설명해주세요. 다음 내용을 포함해 주세요:
1. 음력으로 언제인지
2. 전통적으로 먹는 음식과 그 의미
3. 하는 놀이와 풍습
4. 현대 한국 사회에서의 의미

가능한한 한국인의 관점에서 자연스럽게 설명해주세요.""",
    "💻 코딩 문제 해결": """다음 파이썬 코딩 문제를 해결해주세요:

문제:
1. 주어진 정수 리스트에서 연속된 부분 리스트의 합이 최대가 되는 부분 리스트를 찾는 함수를 작성하세요.
2. 예를 들어, [-2, 1, -3, 4, -1, 2, 1, -5, 4]에서 최대 합을 갖는 부분 리스트는 [4, -1, 2, 1]이고 합은 6입니다.
3. 시간 복잡도는 O(n)이어야 합니다.
4. 함수뿐만 아니라 테스트 코드와 설명도 포함해주세요.
5. 코드에 대한 설명을 한국어로 해주세요.""",
}

# 사이드바
with st.sidebar:
    st.title("🤖 K-EXAONE Chat")
    st.markdown("---")

    # API 키 입력
    st.subheader("🔑 API 키 설정")
    api_key_input = st.text_input(
        "FRIENDLI_TOKEN (API Key)",
        type="password",
        placeholder="FriendliAI API 키를 입력하세요...",
        value=st.session_state.api_key,
        help="FriendliAI에서 발급받은 API 키를 입력하세요",
    )
    st.session_state.api_key = api_key_input

    st.markdown("---")

    # 모델 설정
    st.subheader("⚙️ 설정")
    thinking_mode = st.checkbox(
        "추론 모드 (Thinking Mode)", value=True, help="모델의 사고 과정을 표시합니다"
    )
    st.session_state.thinking_mode = thinking_mode

    st.markdown("---")

    # 프롬프트 예제
    st.subheader("📝 프롬프트 예제")
    st.markdown("아래 예제를 클릭하면 입력창에 자동으로 입력됩니다:")

    for title, prompt in PROMPT_EXAMPLES.items():
        if st.button(
            title, key=f"btn_{title}_{hash(prompt)}", use_container_width=True
        ):
            st.session_state.messages = []
            st.session_state.user_input = prompt
            st.session_state.auto_send = True
            st.rerun()

    st.markdown("---")

    # 초기화 버튼
    if st.button("🗑️ 대화 내용 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.user_input = ""
        st.rerun()

    st.markdown("---")
    st.markdown("""
    ### 💡 사용 팁
    - K-EXAONE은 **256K 컨텍스트**를 지원합니다
    - **한국어** 처리에 특화되어 있습니다
    - **추론 모드**에서 사고 과정을 볼 수 있습니다
    - **수학**, **코딩**, **장문서 이해**에 강점이 있습니다
    """)

# 메인 영역
st.title("🤖 K-EXAONE 대화하기")
st.markdown(f"**모델**: {MODEL} | **추론 모드**: {'✅' if thinking_mode else '❌'}")

# API 키 확인
if not st.session_state.api_key:
    st.warning("⚠️ 사이드바에서 FriendliAI API 키를 입력해주세요.")
    st.stop()

# 채팅 history 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            # 추론 내용이 있다면 먼저 표시
            if "reasoning" in message and thinking_mode:
                with st.expander("🧠 사고 과정 (Reasoning)", expanded=False):
                    st.markdown(message["reasoning"])
            st.markdown(message["content"])

# 사용자 입력 영역
st.markdown("---")

# 세션 상태 초기화 (입력값 관리용)
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# 입력창과 전송 버튼을 col으로 나누기
col1, col2 = st.columns([4, 1])

with col1:
    # 입력창 초기값 설정 (세션 상태에서 값 가져오기)
    input_value = st.session_state.get("user_input", "")

    user_input = st.text_area(
        "메시지를 입력하세요...", height=35, value=input_value, key="user_input"
    )

with col2:
    st.markdown(f'<div style="margin-top: 55px;"></div>', unsafe_allow_html=True)
    send_button = st.button("전송", use_container_width=True, type="primary")

# 페이지 로드 시 자동 전송 확인
if (
    st.session_state.auto_send
    and st.session_state.user_input
    and st.session_state.user_input.strip()
):
    # 자동 전송 플래그 초기화
    st.session_state.auto_send = False

    # 입력값 저장 (입력창 초기화 전에)
    current_input = st.session_state.user_input

    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": current_input})

    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(current_input)

    # 입력창 초기화
    st.session_state.user_input = ""

    # 어시스턴트 응답 생성 (스트리밍)
    with st.chat_message("assistant"):
        try:
            client = get_client(st.session_state.api_key)
            extra_body = {
                "parse_reasoning": True,
                "chat_template_kwargs": {"enable_thinking": thinking_mode},
            }

            # 스트리밍 응답 생성
            stream = client.chat.completions.create(
                model=MODEL,
                extra_body=extra_body,
                messages=st.session_state.messages,
                stream=True,
            )

            # 추론 내용과 최종 응답을 저장할 변수
            full_reasoning = ""
            full_content = ""

            # placeholder 생성
            reasoning_placeholder = st.empty() if thinking_mode else None
            content_placeholder = st.empty()

            # 스트리밍 응답 처리
            for chunk in stream:
                delta = chunk.choices[0].delta

                reasoning_content = getattr(delta, "reasoning_content", None)
                content = getattr(delta, "content", None)

                if reasoning_content:
                    full_reasoning += reasoning_content
                    if thinking_mode and reasoning_placeholder:
                        reasoning_placeholder.markdown(full_reasoning)

                if content:
                    full_content += content
                    content_placeholder.markdown(full_content)

            # 메시지 저장
            message_data = {"role": "assistant", "content": full_content}
            if full_reasoning:
                message_data["reasoning"] = full_reasoning
            st.session_state.messages.append(message_data)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
            st.markdown("💡 **해결 방법**:")
            st.markdown("- API 키가 올바른지 확인하세요")
            st.markdown("- 인터넷 연결을 확인하세요")
            st.markdown("- FriendliAI 서비스 상태를 확인하세요")

    st.rerun()

# 전송 버튼 클릭 또는 Enter 키 처리
if send_button and user_input and user_input.strip():
    # 입력값 세션 상태에 저장
    st.session_state.user_input = user_input

    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(user_input)

    # 입력창 초기화
    st.session_state.user_input = ""

    # 어시스턴트 응답 생성 (스트리밍)
    with st.chat_message("assistant"):
        try:
            client = get_client(st.session_state.api_key)
            extra_body = {
                "parse_reasoning": True,
                "chat_template_kwargs": {"enable_thinking": thinking_mode},
            }

            # 스트리밍 응답 생성
            stream = client.chat.completions.create(
                model=MODEL,
                extra_body=extra_body,
                messages=st.session_state.messages,
                stream=True,
            )

            # 추론 내용과 최종 응답을 저장할 변수
            full_reasoning = ""
            full_content = ""

            # 스트리밍 응답 처리
            for chunk in stream:
                delta = chunk.choices[0].delta

                reasoning_content = getattr(delta, "reasoning_content", None)
                content = getattr(delta, "content", None)

                if reasoning_content:
                    full_reasoning += reasoning_content
                    if st.session_state.thinking_mode:
                        st.write(reasoning_content)

                if content:
                    full_content += content
                    st.write(content)

            # 메시지 저장
            message_data = {"role": "assistant", "content": full_content}
            if full_reasoning:
                message_data["reasoning"] = full_reasoning
            st.session_state.messages.append(message_data)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
            st.markdown("💡 **해결 방법**:")
            st.markdown("- API 키가 올바른지 확인하세요")
            st.markdown("- 인터넷 연결을 확인하세요")
            st.markdown("- FriendliAI 서비스 상태를 확인하세요")

    st.rerun()

# 하단 정보
st.markdown("---")
st.markdown("""
### 📊 K-EXAONE 핵심 성능
- **총 파라미터**: 236B (활성: 23B)
- **컨텍스트 길이**: 256K 토큰
- **지원 언어**: 한국어, 영어, 스페인어, 독일어, 일본어, 베트남어
- **특화 분야**: 추론, 수학, 코딩, 장문서 처리

### 🔗 관련 링크
- [Hugging Face](https://huggingface.co/LGAI-EXAONE/K-EXAONE-236B-A23B)
- [GitHub](https://github.com/LG-AI-EXAONE/K-EXAONE)
- [기술 보고서](https://arxiv.org/pdf/2601.01739)
""")

# CSS 스타일
st.markdown(
    """
<style>
    .stChatMessage {
        background-color: #f0f7ff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .stTextArea {
        background-color: #ffffff;
    }
    .stButton>button {
        border-radius: 5px;
    }
</style>
""",
    unsafe_allow_html=True,
)
