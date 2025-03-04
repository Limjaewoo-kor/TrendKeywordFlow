import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from ..services.nlp_service import summarize_text, extract_keywords




async def crawl_tistory(query: str, max_results: int = 3):
    """ Google 검색을 통해 Tistory 블로그 상위 포스팅 URL 및 본문 콘텐츠 크롤링 """

    # Chrome 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # UI 없이 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")  # 크롤링 감지 방지
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )  # 최신 User-Agent 적용

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Google 검색 URL
    search_url = f"https://www.google.com/search?q={query}+site:tistory.com"
    driver.get(search_url)
    time.sleep(3)  # 차단 방지를 위한 대기

    # 검색 결과가 완전히 로딩될 때까지 대기
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.yuRUbf a"))
        )
    except:
        driver.quit()
        return []  # 오류 발생 시 빈 리스트 반환

    # BeautifulSoup으로 검색 결과 파싱
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Google 검색 결과에서 제목과 링크 가져오기
    results = []
    links = []

    for g in soup.select("div.yuRUbf")[:max_results]:
        title_tag = g.select_one("h3")
        link_tag = g.select_one("a")

        if title_tag and link_tag:
            title = title_tag.get_text()
            link = link_tag["href"]
            links.append(link)  # 나중에 개별 페이지 방문을 위해 저장

            results.append({
                "title": title,
                "link": link,
                "content": "내용 가져오는 중...",  #  개별 크롤링 후 업데이트할 예정
                "description": "내용 가져오는 중...",  #  개별 크롤링 후 업데이트할 예정
                "platform": "Tistory"
            })

    #  각 블로그 글 내부 본문 크롤링
    for i, link in enumerate(links):
        try:
            driver.get(link)
            time.sleep(3)  # 페이지 로딩 대기

            # 본문이 완전히 로딩될 때까지 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#content, div.article-view, div.post-content, div.tt_article_useless_p_margin, div.tt_article_useless_p_margin.contents_style"))
            )

            page_soup = BeautifulSoup(driver.page_source, "html.parser")
            content_tag = (
                    page_soup.select_one("div#content div.article-view") or
                    page_soup.select_one("div.article-view") or
                    page_soup.select_one("div.tt_article_useless_p_margin.contents_style") or
                    page_soup.select_one("div.post-content") or
                    page_soup.select_one("article")
            )
            text_content = content_tag.get_text(separator=" ", strip=True) if content_tag else "본문을 가져올 수 없습니다."
            summary = summarize_text(text_content)
            #  검색 결과 리스트에 본문 업데이트
            results[i]["description"] = summary
            results[i]["content"] = text_content

        except Exception as e:
            print(f"크롤링 실패: {link} - {str(e)}")
            results[i]["content"] = "본문 크롤링 실패"

    driver.quit()
    return results




