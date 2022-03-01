import secrets
from typing import List, Union, Optional, Dict, Any

from pydantic import AnyHttpUrl, BaseSettings, validator, HttpUrl, EmailStr, PostgresDsn


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600 * 24 * 7 # NOTE: 7 días en segundos.
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    DOMAIN_URL: AnyHttpUrl
    LANGUAGES_PATH: str = "./src/assets/locales"
    FONTS_PATH: str = "./src/assets/fonts"
    # JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

        raise ValueError(v)

    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None
    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0 or v is None:
            return None
        
        return v

    # DATABASE
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_TEMPLATES_DIR: str = "./src/assets/emails/src"
    EMAILS_OPTIONS: Optional[Dict[str, Any]] = None
    @validator("EMAILS_OPTIONS", always=True)
    def set_email_options(cls, v: Optional[str], values: Dict[str, Any]) -> Dict[str, Any]:
        if not v:
            return {
                "host": values.get("SMTP_HOST"),
                "port": values.get("SMTP_PORT"),
                "user": values.get("SMTP_USER"),
                "password": values.get("SMTP_PASSWORD")
            }
        return v

    class Config:
        env_file = '.env'
        case_sensitive = True

settings = Settings()
