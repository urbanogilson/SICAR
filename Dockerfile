ARG VARIANT="3.12"
FROM python:${VARIANT}-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        libgl1 \
        libglib2.0-0 \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install into a venv outside the runtime /sicar volume mount, and non-editable so
# the package does not depend on the copied sources being present at runtime.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN uv sync --extra paddle --frozen --no-dev --no-editable

# Download PaddleOCR models
RUN echo 'from paddleocr import PaddleOCR\nPaddleOCR(lang="en")' | /opt/venv/bin/python

WORKDIR /sicar
ENTRYPOINT ["/opt/venv/bin/python"]
