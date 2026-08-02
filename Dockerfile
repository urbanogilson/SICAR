ARG VARIANT="3.12"
FROM python:${VARIANT}-slim

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        libglib2.0-0 \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir 'SICAR[paddle] @ git+https://github.com/urbanogilson/SICAR'

WORKDIR /sicar

# Download PaddleOCR models
RUN echo 'from paddleocr import PaddleOCR\nPaddleOCR(lang="en")' | python

ENTRYPOINT ["python"]
