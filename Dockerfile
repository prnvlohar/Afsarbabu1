FROM python:3

WORKDIR /data

COPY . .

RUN pip install -r requirements.txt

EXPOSE 80



