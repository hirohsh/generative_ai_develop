FROM python:3.13-slim-bookworm as base
# uv のインストール
COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/
# 環境変数の設定
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local


FROM public.ecr.aws/lambda/python:3.13 AS production
# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}
# Install the specified packages
RUN pip install -r requirements.txt
# Copy function code
COPY . ${LAMBDA_TASK_ROOT}
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]


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
WORKDIR "/scraper"
