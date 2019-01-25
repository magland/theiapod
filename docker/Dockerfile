FROM gitpod/workspace-full

RUN npm install -g yarn

ARG version=latest

USER root

WORKDIR /home/theia
ADD $version.package.json ./package.json
ARG GITHUB_TOKEN
RUN yarn --cache-folder ./ycache && rm -rf ./ycache
RUN yarn theia build
EXPOSE 3000
ENV SHELL /bin/bash

USER gitpod
RUN pip install pyyaml
RUN pip install jupyterlab

USER root

COPY entrypoint.sh /entrypoint.sh
RUN chown gitpod:gitpod /entrypoint.sh
RUN chown gitpod:gitpod /home
ENTRYPOINT ["/entrypoint.sh"]

USER gitpod

