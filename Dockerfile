FROM centos/python-38-centos7

ADD . /app

WORKDIR /app
USER root

RUN set -x \
    && mkdir -p ~/.pip \
    && echo '[global]' > ~/.pip/pip.conf \
    && echo 'index-url =  https://mirrors.aliyun.com/pypi/simple/' >> ~/.pip/pip.conf \
    && pip install -r requirements.txt

ENV TZ='Asia/Shanghai'

CMD python3 main.py
