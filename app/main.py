from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as search_router

app = FastAPI(title="Blog Content Assistant", version="1.0.0", debug=True)
app.include_router(search_router, prefix="/api")

# ✅ CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용 (배포 시 특정 도메인으로 제한 해야함)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


@app.get("/")
async def root():
    import torch

    print("PyTorch Version:", torch.__version__)
    print("CUDA Available:", torch.cuda.is_available())
    print("GPU 이름:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "사용 불가")

    return {"message": "FastAPI 서버가 정상적으로 실행 중입니다!"}

