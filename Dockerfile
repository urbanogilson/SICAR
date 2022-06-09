FROM python:3

WORKDIR /usr/src/app

RUN apt-get update -y

RUN apt-get install -y tesseract-ocr

RUN apt-get install -y python3-opencv

RUN pip install --upgrade pip

RUN pip install --no-cache-dir git+https://github.com/urbanogilson/SICAR

COPY . .

VOLUME [ "/data" ]

RUN pip list

CMD [ "python", "./examples/docker.py" ]
