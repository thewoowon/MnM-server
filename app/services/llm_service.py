"""
OpenAI를 사용한 LLM 서비스
일기와 purpose에서 영화 추천을 위한 키워드를 추출합니다.
"""
from openai import OpenAI
from typing import List
from app.core.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def extract_keywords_from_diary(diary_content: str, purpose: str) -> List[str]:
    """
    일기 내용과 목적(purpose)을 분석하여 영화 추천을 위한 키워드를 추출합니다.

    Args:
        diary_content: 일기 내용
        purpose: 영화를 보려는 목적

    Returns:
        추출된 키워드 리스트 (최대 10개)
    """
    prompt = f"""
당신은 영화 추천 전문가입니다. 사용자의 일기와 영화를 보려는 목적을 분석하여
적합한 영화를 추천하기 위한 키워드를 추출해주세요.

# 일기 내용:
{diary_content}

# 영화를 보려는 목적:
{purpose}

# 지시사항:
1. 일기에서 드러나는 사용자의 감정, 상황, 욕구를 파악하세요
2. 목적을 고려하여 사용자가 어떤 종류의 영화를 원하는지 추론하세요
3. 영화 추천에 적합한 키워드를 최대 10개까지 추출하세요
4. 키워드는 장르, 주제, 감정, 분위기 등을 포함할 수 있습니다
5. 결과는 반드시 쉼표로 구분된 키워드 목록만 출력하세요 (다른 설명 없이)

예시 출력: 희망, 우정, 감동, 로맨스, 코미디
"""

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "당신은 영화 추천을 위한 키워드 추출 전문가입니다. 사용자의 일기와 목적을 분석하여 정확한 키워드만 추출합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=200
        )

        # 응답에서 키워드 추출
        keywords_text = response.choices[0].message.content.strip()

        # 쉼표로 분리하고 정리
        keywords = [k.strip() for k in keywords_text.split(',')]

        # 빈 문자열 제거 및 최대 10개로 제한
        keywords = [k for k in keywords if k][:10]

        return keywords

    except Exception as e:
        print(f"OpenAI API 에러: {e}")
        # 에러 발생 시 기본 키워드 반환 (purpose 기반)
        return [purpose] if purpose else ["일상", "힐링"]


def extract_keywords_batch(items: List[dict]) -> List[List[str]]:
    """
    여러 일기-purpose 쌍에 대해 일괄 키워드 추출

    Args:
        items: [{"diary_content": "...", "purpose": "..."}, ...] 형태의 리스트

    Returns:
        각 항목에 대한 키워드 리스트들
    """
    results = []
    for item in items:
        keywords = extract_keywords_from_diary(
            item.get("diary_content", ""),
            item.get("purpose", "")
        )
        results.append(keywords)

    return results
