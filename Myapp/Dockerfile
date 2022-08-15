FROM ubuntu:16.04

ENV PORT 80
ENV HOST 0.0.0.0

EXPOSE 80

RUN apt-get update -y && \
    apt-get install -y python3-pip

COPY ./requirements.txt /app/requirments.txt

WORKDIR /app

RUN pip3 install -r requirments.txt

COPY . /app

ENTRYPOINT ["python3"]

CMD ["app.py"]