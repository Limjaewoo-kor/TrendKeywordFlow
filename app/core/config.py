from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()


class NaverSettings(BaseSettings):
    NAVER_CLIENT_ID: str
    NAVER_CLIENT_SECRET: str

    class Config:
        env_file = ".env"
        extra = "allow"  # 추가 필드 허용

naverSettings = NaverSettings()
