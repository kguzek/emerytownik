FROM ghcr.io/astral-sh/uv:python3.12-bookworm

ADD . /app

WORKDIR /app
RUN uv sync --locked

EXPOSE 8000

WORKDIR /app/machine_learning/data

CMD ["uv", "run", "server.py"]
