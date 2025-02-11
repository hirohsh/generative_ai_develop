FROM python:3.11-slim-bookworm as base
COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /uvx /bin/
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.11
WORKDIR /app

FROM base as builder
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable

FROM base as develop

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
