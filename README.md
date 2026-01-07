# K-EXAONE Chat

K-EXAONE 대규모 언어 모델과 상호작용하는 웹 기반 채팅 인터페이스

## 기능

- **대화형 채팅**: K-EXAONE 모델과 자연스러운 대화
- **추론 모드**: 모델의 사고 과정을 실시간으로 확인
- **스트리밍 응답**: 실시간 응답 생성
- **프롬프트 예제**: 추론, 수학, 요약, 코딩 등 다양한 예제 제공
- **한국어 특화**: 한국어 처리에 최적화된 모델
- **256K 컨텍스트**: 대규모 문서 처리 가능

## 사전 요구사항

- Python 3.8 이상
- FriendliAI API 키 (https://friendli.ai/ 에서 발급 가능)

## 설치 방법

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 패키지 설치
pip install streamlit openai
```

## 실행 방법

```bash
streamlit run app.py
```

브라우저에서 자동으로 열리며, 사이드바에서 API 키를 입력하세요.

## 사용 방법

1. 사이드바에서 FriendliAI API 키 입력
2. 추론 모드(Thinking Mode) 설정 (선택사항)
3. 메시지를 입력하거나 프롬프트 예제 클릭
4. 전송 버튼을 클릭하여 모델과 대화

## 프롬프트 예제

- 🧠 추론 능력 테스트: 논리 퍼즐 단계별 해결
- 📊 수학 문제 해결: 복잡한 수학 문제 단계별 계산
- 📚 장문서 요약 테스트: 긴 텍스트 핵심 내용 요약
- 🇰🇷 한국어 문화 맥락 이해: 한국 문화적 맥락 반영 답변
- 💻 코딩 문제 해결: 파이썬 코딩 문제와 테스트 코드 작성

## 모델 정보

- **모델**: LGAI-EXAONE/K-EXAONE-236B-A23B
- **총 파라미터**: 236B (활성: 23B)
- **컨텍스트 길이**: 256K 토큰
- **지원 언어**: 한국어, 영어, 스페인어, 독일어, 일본어, 베트남어
- **특화 분야**: 추론, 수학, 코딩, 장문서 처리

## API 키 발급

FriendliAI에서 API 키를 발급받으세요:

1. [FriendliAI](https://friendli.ai/) 가입
2. 대시보드에서 API 키 생성
3. 발급받은 API 키를 사이드바에 입력

## 관련 링크

- [Hugging Face 모델](https://huggingface.co/LGAI-EXAONE/K-EXAONE-236B-A23B)
- [GitHub 저장소](https://github.com/LG-AI-EXAONE/K-EXAONE)
- [기술 보고서](https://arxiv.org/pdf/2601.01739)

## 라이선스

MIT License
