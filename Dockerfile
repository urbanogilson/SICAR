FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y python3-opencv python-matplotlib tesseract-ocr && \
    pip install --no-cache-dir -r requirements.txt
    

COPY . .

VOLUME [ "/data" ]

CMD [ "python", "./src/start.py" ]