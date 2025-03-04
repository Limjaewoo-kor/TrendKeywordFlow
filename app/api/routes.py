from fastapi import APIRouter, HTTPException, Depends

from ..services.ai_template_generator import generate_ai_template
from ..services.naver_crawler import crawl_naver
from ..services.tistory_crawler import crawl_tistory
from ..services.nlp_service import summarize_text, extract_keywords
from ..schemas.summarize import ContentRequest
from pydantic import BaseModel
from ..services.template_service import generate_template
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..models.blog_post import BlogPost
from ..models.keyword import Keyword
from ..models.summary import Summary
from ..models.template import Template
from ..schemas.post import BlogPostRequest
from app.core.config import naverSettings
import requests
from ..schemas.trend import TrendRequest



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/search/naver")
async def naver_search(keyword: str):
    result = await crawl_naver(keyword)
    return result


@router.get("/search/tistory")
async def tistory_search(keyword: str):
    result = await crawl_tistory(keyword)
    return result


@router.post("/crawl-and-save")
async def crawl_and_save(keyword: str, db: Session = Depends(get_db)):
    """크롤링 후 게시글 자동 저장"""
    try:
        print(f" 크롤링 시작: {keyword}")
        naver_posts = await crawl_naver(keyword)
        print(f"📝 네이버 크롤링 완료: {len(naver_posts)}건 수집 (타입: {type(naver_posts)})")

        #  naver_posts가 dict이면 posts 키에서 리스트 추출
        if isinstance(naver_posts, dict):
            naver_posts = naver_posts.get("items", [])


        tistory_posts = await crawl_tistory(keyword)
        print(f"📝 티스토리 크롤링 완료: {len(tistory_posts)}건 수집 (타입: {type(tistory_posts)})")

        all_posts = naver_posts + tistory_posts
        saved_posts = []

        #  리스트 내 각 게시글에 'link' 키 존재 여부 확인
        for post in all_posts:
            if 'link' not in post:
                print(f" 'link' 키 누락: {post}")
                continue

            print(f" URL 확인 중: {post['link']}")  #  각 URL 출력

            exists = db.query(BlogPost).filter(BlogPost.url == post["link"]).first()
            if exists:
                print(f" 중복 URL: {post['link']} - 저장하지 않음")  #  중복 URL 로그 출력
                continue

            try:
                new_post = BlogPost(
                    title=post.get("title", "제목 없음"),
                    url=post["link"],
                    content=post.get("content", "내용 없음"),
                    description=post.get("description", "설명 없음"),
                    platform=post.get("platform", "Naver"),
                    searchkeyword=keyword
                )
                db.add(new_post)
                db.commit()
                db.refresh(new_post)
                print(f"✅ 저장됨: {post['link']}")  #  저장 성공 로그 출력
                saved_posts.append(new_post)
            except Exception as e:
                db.rollback()
                print(f" 저장 중 오류: {post['link']} - {str(e)}")

        print(f"✅ 저장 완료: {len(saved_posts)}건 저장됨")
        return {"message": f"{len(saved_posts)}개의 게시글이 저장되었습니다.", "posts": saved_posts}

    except Exception as e:
        db.rollback()
        print(f" 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"크롤링 및 저장 중 오류: {str(e)}")



@router.post("/summarize")
async def summarize_endpoint(request: ContentRequest):
    """게시글 내용 요약 엔드포인트"""
    try:
        summary = summarize_text(request.content)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"요약 처리 중 오류: {str(e)}")


@router.post("/keywords")
async def keywords_endpoint(request: ContentRequest):
    """핵심 키워드 추출 엔드포인트"""
    try:
        keywords = extract_keywords(request.content)
        return {"keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"키워드 추출 중 오류: {str(e)}")



class TemplateRequest(BaseModel):
    topic: str
    keywords: list
    summary: str


@router.post("/generate-template/{chk}")
async def generate_template_endpoint(request: TemplateRequest,chk: int):
    """AI 글 템플릿 생성 엔드포인트"""
    try:
        template = generate_ai_template(request.topic, request.keywords, request.summary,chk)
        # template = generate_template(request.topic, request.keywords, request.summary)
        return {"template": template}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"템플릿 생성 중 오류: {str(e)}")


#DB
@router.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    """저장된 모든 게시글 조회"""
    posts = db.query(BlogPost).all()
    return {"posts": posts}


@router.post("/posts")
async def save_post(request: BlogPostRequest, db: Session = Depends(get_db)):
    """게시글 저장 엔드포인트"""
    try:
        post = BlogPost(
            title=request.title,
            url=request.url,
            content=request.content,
            description=request.description,
            searchkeyword=request.keyword,
            platform=request.platform
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        return {"message": "게시글 저장 성공", "post_id": post.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"게시글 저장 중 오류: {str(e)}")


@router.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    """특정 게시글 조회 엔드포인트"""
    post = db.query(BlogPost).filter(BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post


NAVER_CLIENT_ID = naverSettings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = naverSettings.NAVER_CLIENT_SECRET


@router.post("/trend-analysis")
async def analyze_trend(request: TrendRequest):
    """네이버 데이터랩 API를 통한 여러 키워드 비교 트렌드 분석"""
    try:
        if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
            raise HTTPException(status_code=500, detail="네이버 API 키가 설정되지 않았습니다.")

        url = "https://openapi.naver.com/v1/datalab/search"
        headers = {
            "X-Naver-Client-Id": NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
            "Content-Type": "application/json"
        }

        #  여러 키워드를 비교하기위한 keywordGroups 생성
        payload = {
            "startDate": "2024-01-01",
            "endDate": "2024-12-31",
            "timeUnit": "month",
            "keywordGroups": [
                {"groupName": kw, "keywords": [kw]} for kw in request.keywords  #  여러 그룹 생성
            ]
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"네이버 API 호출 실패: {response.text}"
            )

        result = response.json()

        # 비교 결과 가독성을 높이기 위해 반환 형식 개선
        comparison_result = {
            "status": "success",
            "startDate": result.get("startDate"),
            "endDate": result.get("endDate"),
            "results": [
                {
                    "keyword": group["title"],
                    "data": group["data"]
                } for group in result.get("results", [])
            ]
        }

        return comparison_result  # 개선된 형식 반환

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"트렌드 분석 중 오류: {str(e)}")


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.blog_post import BlogPost



class TemplateUpdateRequest(BaseModel):
    template: str

@router.put("/posts/{post_id}/template")
async def update_template(post_id: int, request: TemplateUpdateRequest, db: Session = Depends(get_db)):
    """템플릿 내용 업데이트"""
    try:
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        post.content = request.template  # 템플릿 업데이트
        db.commit()
        db.refresh(post)
        return {"message": "템플릿 업데이트 완료"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"템플릿 업데이트 중 오류 발생: {str(e)}")
