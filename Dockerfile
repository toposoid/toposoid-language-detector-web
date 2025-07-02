FROM python:3.10.13

WORKDIR /app
ARG TARGET_BRANCH
ENV DEPLOYMENT=local

RUN cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN apt-get update && apt-get upgrade -y \
&& apt-get -y install git libgl1-mesa-dev cron \
&& git clone https://github.com/toposoid/toposoid-language-detector-web.git \
&& cd toposoid-language-detector-web \
&& git fetch origin ${TARGET_BRANCH} \
&& git checkout ${TARGET_BRANCH} \
&& sed -i s/__##GIT_BRANCH##__/${TARGET_BRANCH}/g requirements.txt \
&& pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
&& rm -f requirements.txt

COPY ./docker-entrypoint.sh /app/
ENTRYPOINT ["/app/docker-entrypoint.sh"]
