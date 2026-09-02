FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    FLASK_APP=sample_app.app \
    FLASK_RUN_HOST=0.0.0.0

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

COPY . .
RUN uv sync --locked --no-dev

EXPOSE 5000

CMD ["uv", "run", "flask", "--app", "sample_app.app", "run"]