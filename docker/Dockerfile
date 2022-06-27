FROM ubuntu:xenial
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install python3-pip python3-dev libmysqlclient-dev -y
RUN apt-get clean

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

RUN mkdir -p /opt/miaou/uploads
WORKDIR /opt/miaou

ADD ./chall/requirements.txt /opt/miaou/requirements.txt
RUN pip3 install -r requirements.txt

COPY ./chall /opt/miaou

RUN useradd -ms /bin/bash user
RUN chown user:user /opt/miaou/uploads

USER user

CMD /wait && python3 run.py
