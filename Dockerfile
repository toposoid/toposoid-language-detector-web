FROM python:3.10

WORKDIR /app
ARG TARGET_BRANCH
ENV DEPLOYMENT=local

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get upgrade -y \
&& apt-get -y install git \
&& curl -LsSf https://astral.sh/uv/install.sh | sh \
&& source ${HOME}/.local/bin/env \
&& git clone https://github.com/toposoid/toposoid-language-detector-web.git \
&& cd toposoid-language-detector-web \
&& git fetch origin ${TARGET_BRANCH} \
&& git checkout ${TARGET_BRANCH} \
&& sed s/__##GIT_BRANCH##__/${TARGET_BRANCH}/g pyproject.toml.template > pyproject.toml \
&& uv sync \
&& uv add git+https://github.com/toposoid/toposoid-python-lib.git@${TARGET_BRANCH}#egg=ToposoidCommon

COPY ./docker-entrypoint.sh /app/
ENTRYPOINT ["/app/docker-entrypoint.sh"]
