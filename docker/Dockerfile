FROM python:3.7-stretch

#RUN apt-get update && apt-get install -y software-properties-common

# Node
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get update && apt-get install nodejs

### Yarn ###
RUN npm install -g yarn

## Theia
ARG version=latest
WORKDIR /home/theia
ADD $version.package.json ./package.json
ARG GITHUB_TOKEN
RUN yarn --cache-folder ./ycache && rm -rf ./ycache
RUN yarn theia build
EXPOSE 3000
ENV SHELL /bin/bash

RUN apt-get install sudo

RUN echo "python version:" && python --version

RUN pip install pyyaml
RUN apt-get install nano

RUN python3 -m venv /venv
RUN . /venv/bin/activate && pip install pyyaml

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
