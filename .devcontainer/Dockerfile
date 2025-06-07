ARG VARIANT="3.10"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Install additional OS packages.
RUN apt-get update && apt-get install -y ccache && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install tesseract-ocr python3-opencv