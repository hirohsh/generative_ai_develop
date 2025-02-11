FROM python:3.11-slim-bookworm as base
# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# uv のインストール
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
# 環境変数の設定
ENV PATH="/root/.cargo/bin:${PATH}" \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.11



FROM base as builder
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable


FROM base as develop
# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# AWS CLI のインストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws
# 作業ディレクトリの設定
WORKDIR /app

FROM gcr.io/distroless/python3-debian12:debug-nonroot as staging
COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv
WORKDIR /app
USER nonroot
CMD ["/app/.venv/bin/hello"]


FROM gcr.io/distroless/python3-debian12:nonroot as production
COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv
WORKDIR /app
USER nonroot
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80"]
