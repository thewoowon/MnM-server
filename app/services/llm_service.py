"""
OpenAI를 사용한 LLM 서비스
일기와 purpose에서 영화 추천을 위한 키워드를 추출합니다.
"""
from openai import OpenAI
from typing import List, Dict
from app.core.config import settings
import json


client = OpenAI(api_key=settings.OPENAI_API_KEY)

KEYWORDS_LIST = ["가족","갈등","감금","감성","감시","감정","강박","각성","거래","거짓","계급","고독","고립","공동체","공포","관계","관찰","광기","권력","규범","기록","기억","기회","긴박","긴장","낙인","논란","누명","도덕","동료애","몰락","무력감","미래","미디어","미스터리","배신","변화","보호","복수","분노","불균형","불신","불안","붕괴","비극","비리","빈곤","사기","사랑","상실","생존","성공","성실","성장","선택","설렘","속죄","수용","순수","시대","시간","신념","실종","억압","연결","연대","열정","영화산업","욕망","용기","우연","유대","유랑","유머","윤리","의문","의심","의식","이념","이동","이별","이주","인간성","인내","일상","일탈","자유","자아","저항","정체성","정의","정착","정치","조작","종말","존엄","존재","죄책감","질문","집단심리","집착","차별","창작","책임","천재성","침묵","침투","통제","트라우마","폭력","풍자","허무","현실","환각","해방","행복","향수","회복","희망",]

def extract_keywords_from_diary(diary_content: str, purpose: str) -> Dict[str, any]:
    """
    일기 내용과 목적(purpose)을 분석하여 영화 추천을 위한 키워드와 설명을 추출합니다.

    Args:
        diary_content: 일기 내용
        purpose: 영화를 보려는 목적

    Returns:
        dict: {
            "keywords": ["키워드1", "키워드2", ...],
            "explanation": "따뜻한 톤의 설명 멘트"
        }
    """
    prompt = f"""
            당신은 영화 추천 전문가입니다. 사용자의 일기와 영화를 보려는 목적을 분석하여
            적합한 영화를 추천하기 위한 키워드를 추출하고, 따뜻한 설명을 작성해주세요.

            # 일기 내용:
            {diary_content}

            # 영화를 보려는 목적:
            {purpose}

            # 지시사항:
            1. 일기에서 드러나는 사용자의 감정, 상황, 욕구를 파악하세요
            2. 목적을 고려하여 사용자가 어떤 종류의 영화를 원하는지 추론하세요
            3. 영화 추천에 적합한 키워드를 최대 10개까지 추출하세요
            4. **중요**: 키워드는 반드시 아래 목록에서만 선택하세요:
            {KEYWORDS_LIST}
            5. 목록에 없는 키워드는 절대 사용하지 마세요
            6. 사용자에게 보여줄 따뜻하고 공감적인 설명 멘트를 작성하세요
            - 일기에서 포착한 감정이나 상황을 언급
            - 왜 이런 키워드/영화를 선택했는지 친근하게 설명
            - 2-3문장 정도의 자연스러운 톤

            # 출력 형식 (반드시 JSON만 출력):
            {{
            "keywords": ["키워드1", "키워드2", "키워드3"],
            "explanation": "오늘 기록에서는 힘든 하루 속에서도 누군가와 나눈 대화가 큰 위로가 된 점이 눈에 띄었어요. 그래서 따뜻한 관계와 감정을 느낄 수 있는 작품들을 골랐답니다. 또 글의 분위기가 조금 지쳐 있는 느낌이었기에, 보면서 기분을 부드럽게 풀어줄 수 있는 영화들을 함께 제안했어요."
            }}
            """

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "당신은 영화 추천을 위한 키워드 추출 전문가입니다. 사용자의 일기와 목적을 분석하여 정확한 키워드와 따뜻한 설명을 JSON 형식으로 제공합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"}
        )

        # JSON 응답 파싱
        result = json.loads(response.choices[0].message.content.strip())

        print(f"OpenAI API 응답: {result}")

        # 키워드 최대 10개로 제한
        if "keywords" in result:
            result["keywords"] = result["keywords"][:10]

        return result

    except Exception as e:
        print(f"OpenAI API 에러: {e}")
        # 에러 발생 시 기본 응답 반환
        return {
            "keywords": [purpose] if purpose else ["일상", "힐링"],
            "explanation": "오늘 하루를 기록해주셔서 감사해요. 편안하게 감상할 수 있는 영화들을 준비했습니다."
        }


def extract_keywords_batch(items: List[dict]) -> List[Dict[str, any]]:
    """
    여러 일기-purpose 쌍에 대해 일괄 키워드 추출

    Args:
        items: [{"diary_content": "...", "purpose": "..."}, ...] 형태의 리스트

    Returns:
        각 항목에 대한 결과 딕셔너리 리스트
        [{"keywords": [...], "explanation": "..."}, ...]
    """
    results = []
    for item in items:
        result = extract_keywords_from_diary(
            item.get("diary_content", ""),
            item.get("purpose", "")
        )
        results.append(result)

    return results
