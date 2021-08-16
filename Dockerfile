FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y python3-opencv python-matplotlib tesseract-ocr && \
    pip install --no-cache-dir git+https://github.com/urbanogilson/SICAR@v0.2

COPY . .

VOLUME [ "/data" ]

RUN git checkout v0.2

RUN pip list

CMD [ "python", "./examples/docker.py" ]