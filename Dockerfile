FROM python:3.14-slim@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8
COPY --from=ghcr.io/astral-sh/uv:latest@sha256:32a7bb39b496babbd997b0a39a4d66c126bdaf5661b302bf6f06abda8deca6ff /uv /bin/uv

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY . /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "zutool"]
