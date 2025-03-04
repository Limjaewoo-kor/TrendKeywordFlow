from transformers import pipeline,PreTrainedTokenizerFast, BartForConditionalGeneration
from keybert import KeyBERT
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# 필요한 리소스 자동 다운로드
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

# 요약 모델 (Hugging Face의 bart-large-cnn 사용)[영문전용모델]
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# KoBART 요약 모델 로딩[한글전용모델]
tokenizer = PreTrainedTokenizerFast.from_pretrained(
    "digit82/kobart-summarization"
)
model = BartForConditionalGeneration.from_pretrained("digit82/kobart-summarization")


# 키워드 모델
kw_model = KeyBERT(model="all-MiniLM-L6-v2")


def summarize_text(content: str, max_length: int = 130, min_length: int = 30):
    # """영문 게시글 내용을 요약"""
    # summary = summarizer(content, max_length=max_length, min_length=min_length, do_sample=False)
    # return summary[0]['summary_text']

    """한글 게시글 내용을 요약"""
    text = content.replace("\n", " ")

    # 입력 텍스트 길이 제한 (모델 입력 크기 초과 방지)
    if len(text) > 1000:
        text = text[:1000]

    input_ids = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        input_ids,
        num_beams=4,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,  #  요약 길이 조절
        no_repeat_ngram_size=3,  #  3그램 반복 방지
        early_stopping=True  #  반복 방지를 위해 일찍 멈춤 설정
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


def extract_keywords(content: str, top_n: int = 10):
    """게시글의 핵심 키워드 추출"""
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(content)
    filtered_text = " ".join([w for w in words if w.lower() not in stop_words])

    keywords = kw_model.extract_keywords(filtered_text, top_n=top_n, stop_words='english')
    return [kw[0] for kw in keywords]
