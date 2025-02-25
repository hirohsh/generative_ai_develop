import os

# 環境設定を取得
APP_ENV = os.getenv("APP_ENV", "development")

# 本番環境かどうかをチェック
PRODUCTION_FLUG = APP_ENV == "production"
