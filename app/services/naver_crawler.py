import aiohttp
from app.core.config import naverSettings

NAVER_CLIENT_ID = naverSettings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = naverSettings.NAVER_CLIENT_SECRET

if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
    raise ValueError("NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET 환경 변수가 설정되지 않았습니다.")


async def crawl_naver(keyword: str, display: int = 3):
    url = f"https://openapi.naver.com/v1/search/blog.json?query={keyword}&display={display}"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()
