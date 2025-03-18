FROM python:3.13-slim-bookworm as base
# uv のインストール
COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/
# 環境変数の設定
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local

# FROM base AS builder
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --frozen --no-install-project --no-dev --no-editable
# COPY . ${LAMBDA_TASK_ROOT}
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv sync --frozen --no-dev --no-editable


FROM base AS develop
# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# AWS CLI のインストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws
# 作業ディレクトリの設定
WORKDIR "/fastapi_backend"
EXPOSE 8000


# FROM public.ecr.aws/lambda/python:3.13 AS staging
# COPY --from=builder --chown=nonroot:nonroot /fastapi_backend/.venv /fastapi_backend/.venv
# WORKDIR ${LAMBDA_TASK_ROOT}
# EXPOSE 8000
# CMD [ "lambda_function.handler" ]


# FROM public.ecr.aws/lambda/python:3.13 AS production
# COPY --from=builder --chown=nonroot:nonroot /fastapi_backend/.venv /fastapi_backend/.venv
# WORKDIR ${LAMBDA_TASK_ROOT}
# EXPOSE 8000
# CMD ["/fastapi_backend/.venv/bin/fastapi", "run", "app/main.py", "--port", "8000"]
