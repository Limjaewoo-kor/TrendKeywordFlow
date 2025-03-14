프로젝트 기능 설명.

1. 크롤링 - (네이버 검색 API 및 셀레니움 사용)
    - 특정 주제를 검색하면 해당 검색어에 해당하는 상위 포스팅 글 3~5개 크롤링하여 DataBase에 저장.
    - 크롤링시 제목, 검색 키워드, 내용, 요약 내용("digit82/kobart-summarization"), 내용의 중요 키워드(KeyBERT(model="all-MiniLM-L6-v2")를 디비에 저장.

2. 언어 모델을 이용한 AI글 생성 - (4가지 언어 모델(KoBART,LGAI-EXAONE,skt/kogpt2,kakaocorp/kanana))
    - 저장된 글 리스트 화면에서 상세화면으로 진입시 해당 글에 대하여 1번에서 저장한 정보를 불러옴.
    -  화면에 제목, 요약내용, 중요키워드를 표출해주며 4가지 언어 모델(KoBART,LGAI-EXAONE,skt/kogpt2,kakaocorp/kanana)을 사용하여
       모델별로 각각 해당 주제에 대하여 글을 생성함. 
    -  부가기능 : 생성 글 복사 및 편집 기능)

3. 특정 키워드의 트렌드 분석 - (네이버 트렌드 분석 API)
   - 다수의 키워드를 입력하여 분석 버튼 클릭시 해당 키워드에 대한 트렌트를 년도/월별 그래프로 시각화 함.


<br><br><br><br>

이미지 설명.
<br><br>
1. 크롤링 기능<br><br>
기존 디비
<img width="1861" alt="디비1" src="https://github.com/user-attachments/assets/a5a5fb95-1f3f-4d60-aa2c-2466b3d0d3ed" /><br><br>
크롤링 성공
<img width="973" alt="디비1_크롤링1" src="https://github.com/user-attachments/assets/05377884-ecf4-4c52-95b6-8f2208b0be7d" /><br><br>
로그
<img width="925" alt="디비1_크롤링2" src="https://github.com/user-attachments/assets/dd186168-1316-47ef-8c8a-2a1fd3c74946" /><br><br>
결과 디비
<img width="1850" alt="디비2" src="https://github.com/user-attachments/assets/600c2a63-54d3-494d-bae3-5009eed19624" /><br><br>

<br><br><br><br>

3. 언어 모델을 이용한 AI글 생성 기능<br><br>
글 리스트
<img width="923" alt="언어모델1" src="https://github.com/user-attachments/assets/ffd77419-9320-42e4-ad0d-c3aa6ce94a0f" /><br><br>
상세 페이지 / AI 글 생성
<img width="1561" alt="언어모델2" src="https://github.com/user-attachments/assets/98fa5b97-4282-4acb-a5d9-23fcb9af7ecd" /><br><br>
로그
<img width="929" alt="언어모델_로그" src="https://github.com/user-attachments/assets/44eb04f2-4fd0-4e09-b5af-cd38cc3e7ecc" /><br><br>

<br><br><br><br>
4. 특정 키워드의 트렌드 분석 기능<br><br>
분석 시작 화면
<img width="1042" alt="트렌드_분석_0" src="https://github.com/user-attachments/assets/174dce57-7f79-4fa6-8e7f-eddeef61f6b4" /><br><br>
분석 결과 화면
<img width="1075" alt="트렌드_분석_1" src="https://github.com/user-attachments/assets/daa817a0-265f-404a-b62b-9cbe1489a281" /><br><br>
<img width="925" alt="트렌드_분석_2" src="https://github.com/user-attachments/assets/0abbe24d-b764-4dca-81a6-6ed22a0e3547" /><br>








