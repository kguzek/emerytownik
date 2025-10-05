FROM ghcr.io/astral-sh/uv:alpine

ADD . /app

WORKDIR /app
RUN uv sync --locked

EXPOSE 8000

WORKDIR /app/machine_learning/data

CMD ["uv", "run", "server.py"]
