ARG VARIANT="3.12"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Install additional OS packages.
RUN apt-get update && apt-get install -y ccache && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install tesseract-ocr

# Install uv (used for dependency management and running tasks).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
