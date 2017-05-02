From python:3.4
ADD selenium_sources/sources.list /etc/apt/sources.list
RUN wget mozilla.debian.net/pkg-mozilla-archive-keyring_1.1_all.deb && dpkg -i pkg-mozilla-archive-keyring_1.1_all.deb && apt-get update && apt-get install -y xvfb && apt-get install -y -t jessie-backports firefox
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple/
