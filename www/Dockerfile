From python:3.4
RUN apt-get update && apt-get install -y ntp
RUN echo "server pool.ntp.org" >> /etc/ntp.conf
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple/
