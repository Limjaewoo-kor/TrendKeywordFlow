


def generate_template(topic: str, keywords: list, summary: str) -> dict:
    """핵심 키워드와 요약을 기반으로 글 템플릿 생성"""

    keywords_str = ", ".join(keywords)
    template = {
        "title": f"{topic} - {keywords[0]}를 중심으로 살펴보기",
        "introduction": f"이번 글에서는 '{topic}'에 대해 다룹니다. 특히 {keywords_str}와 같은 핵심 키워드를 중심으로 내용을 전개할 예정입니다.",
        "body": f"'{topic}'에 대해 깊이 있게 탐구하며, {keywords_str}와 관련된 핵심 내용을 다룹니다.\n\n"
                f"1. {keywords[0]}의 중요성\n"
                f"2. {keywords[1]}와 {keywords[2]}가 미치는 영향\n"
                f"3. {keywords[3]}와 관련된 최신 동향 분석",
        "conclusion": f"요약하자면, {topic}은(는) {keywords[0]}를 비롯한 다양한 핵심 요소와 밀접한 관련이 있습니다. "
                      f"위 내용을 바탕으로 효과적인 전략을 수립할 수 있습니다.\n\n"
                      f" 핵심 요약: {summary}"
    }
    return template
