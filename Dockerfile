# Dockerfile
ARG VARIANT="3.10"
FROM python:${VARIANT}

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install tesseract-ocr python3-opencv

RUN pip install --upgrade pip

RUN pip install 'download_car[paddle]@git+https://github.com/Malnati/download-car'

WORKDIR /download-car

# Download PaddleOCR models
RUN echo 'from paddleocr import PaddleOCR\nPaddleOCR(lang="en")' | python

ENTRYPOINT ["python"]
