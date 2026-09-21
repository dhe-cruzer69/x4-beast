FROM python:3.12-slim

WORKDIR /app

# System deps for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src
COPY config ./config

RUN pip install --no-cache-dir .

# Create non-root user
RUN useradd -m -u 1000 x4 && mkdir -p /app/data && chown -R x4:x4 /app
USER x4

EXPOSE 8787

CMD ["uvicorn", "x4_beast.api:app", "--host", "0.0.0.0", "--port", "8787"]
