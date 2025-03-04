from transformers import BartForConditionalGeneration, AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizerFast
import torch
import os

# 캐시 경로 설정
cache_dir = "C:\\Users\\jaewoo\\PycharmProjects\\TrendKeywordFlow\\model_cache"
offload_dir = os.path.join(cache_dir, "offload")

# 캐시 경로가 없으면 생성
if not os.path.exists(offload_dir):
    os.makedirs(offload_dir)

# GPU 초기화 및 캐시 비우기
if torch.cuda.is_available():
    torch.cuda.init()
    torch.cuda.empty_cache()

# 디바이스 설정 (GPU 우선 사용)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# KoBART 모델과 토크나이저 로드 (1번)
tokenizer1 = AutoTokenizer.from_pretrained('digit82/kobart-summarization', cache_dir=cache_dir)
model_bart = BartForConditionalGeneration.from_pretrained(
    'digit82/kobart-summarization',
    cache_dir=cache_dir,
    low_cpu_mem_usage=True,
    offload_folder=offload_dir,
    device_map="auto"
)
# pad_token_id가 None이면 eos_token_id로 설정
if tokenizer1.pad_token_id is None:
    tokenizer1.pad_token_id = tokenizer1.eos_token_id
    model_bart.config.pad_token_id = tokenizer1.eos_token_id

# EXAONE 모델과 토크나이저 로드 (2번)
model_name = "LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct"
tokenizer2 = AutoTokenizer.from_pretrained(model_name)
model_lg2 = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto"
)
if tokenizer2.pad_token_id is None:
    tokenizer2.pad_token_id = tokenizer2.eos_token_id
    model_lg2.config.pad_token_id = tokenizer2.eos_token_id

# KoGPT2 모델과 토크나이저 로드 (3번)
tokenizer3 = AutoTokenizer.from_pretrained("skt/kogpt2-base-v2", cache_dir=cache_dir)
model_sk2 = AutoModelForCausalLM.from_pretrained(
    "skt/kogpt2-base-v2",
    cache_dir=cache_dir,
    low_cpu_mem_usage=True,
    offload_folder=offload_dir,
    device_map="auto"
)
if tokenizer3.pad_token_id is None:
    tokenizer3.pad_token_id = tokenizer3.eos_token_id
    model_sk2.config.pad_token_id = tokenizer3.eos_token_id

# 카카오 Kanana 모델과 토크나이저 로드 (4번)
model_name_kanana = "kakaocorp/kanana-nano-2.1b-base"
tokenizer4 = AutoTokenizer.from_pretrained(model_name_kanana)
model_kanana = AutoModelForCausalLM.from_pretrained(
    model_name_kanana,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
if tokenizer4.pad_token_id is None:
    tokenizer4.pad_token_id = tokenizer4.eos_token_id
    model_kanana.config.pad_token_id = tokenizer4.eos_token_id


# 템플릿 생성 함수
def generate_ai_template(topic: str, keywords: list, summary: str, chk: int) -> str:
    try:
        print("시작")

        prompt = f"""
        주제: {topic}
        핵심 키워드: {', '.join(keywords)}
        요약: {summary}

        위 정보를 기반으로 다음과 같은 구조의 글 작성 템플릿을 작성하세요:
        1. 서론: 주제 소개 및 흥미 유발
        2. 본론: 핵심 키워드별 상세 설명
        3. 결론: 요약 및 독자에게 전달할 메시지
        """

        # 메시지 형식 (시스템 & 유저)
        lg_messages = [
            {"role": "system", "content": "Complete the matching sentences."},
            {"role": "user", "content": prompt}
        ]
        bart_messages = f"System: Complete the following template.\nUser: {prompt}"
        sk_messages = f"System: Generate a template based on the following information.\nUser: {prompt}"
        kanana_messages = f"System: Create a blog template based on the provided information.\nUser: {prompt}"

        print("중간")
        # `torch.no_grad()`로 메모리 최적화
        with torch.no_grad():
            if chk == 1:
                # KoBART 모델 사용
                input_ids = tokenizer1.encode(bart_messages, return_tensors="pt").to(device)
                attention_mask = input_ids.ne(tokenizer1.pad_token_id).long().to(device)
                summary_ids = model_bart.generate(
                    input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=300,
                    min_length=50,
                    num_beams=4,
                    pad_token_id=tokenizer1.eos_token_id,
                    early_stopping=True
                )
                generated_text = tokenizer1.decode(summary_ids[0], skip_special_tokens=True)
            elif chk == 2:
                # EXAONE 모델 사용
                lg_input_ids = tokenizer2.apply_chat_template(
                    lg_messages,
                    tokenize=True,
                    add_generation_prompt=True,
                    return_tensors="pt"
                )
                attention_mask = lg_input_ids.ne(tokenizer2.pad_token_id).long().to(device)
                summary_ids = model_lg2.generate(
                    lg_input_ids.to(device),
                    attention_mask=attention_mask,
                    max_new_tokens=300,
                    eos_token_id=tokenizer2.eos_token_id,
                    pad_token_id=tokenizer2.eos_token_id,
                    do_sample=False,
                )
                generated_text = tokenizer2.decode(summary_ids[0], skip_special_tokens=True)
            elif chk == 3:
                # KoGPT2 모델 사용
                input_ids = tokenizer3.encode(sk_messages, return_tensors="pt").to(device)
                attention_mask = input_ids.ne(tokenizer3.pad_token_id).long().to(device)
                summary_ids = model_sk2.generate(
                    input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=300,
                    pad_token_id=tokenizer3.eos_token_id,
                    do_sample=True,
                    temperature=0.7
                )
                generated_text = tokenizer3.decode(summary_ids[0], skip_special_tokens=True)
            elif chk == 4:
                # 카카오 Kanana 모델 사용
                input_ids = tokenizer4.encode(kanana_messages, return_tensors="pt").to(device)
                attention_mask = input_ids.ne(tokenizer4.pad_token_id).long().to(device)
                summary_ids = model_kanana.generate(
                    input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=300,
                    pad_token_id=tokenizer4.eos_token_id,
                    do_sample=True,
                    temperature=0.7
                )
                generated_text = tokenizer4.decode(summary_ids[0], skip_special_tokens=True)

        print("끝")
        return generated_text.strip()
    except Exception as e:
        print("에러 발생:", str(e))
        return "에러가 발생했습니다."
