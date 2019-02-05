FROM python:3.7-stretch

# Node
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get update && apt-get install nodejs

### Yarn ###
RUN npm install -g yarn

RUN apt-get install sudo
RUN pip install pyyaml
RUN apt-get install nano

# Create a python virtual environment
# Ultimately this venv will be owned by the non-root user
# But we do not yet know the UID of that user, so until run-time it will be owned by root
# There is a reason we do a symbolic link from /venv to /venv2
# It is because on some systems, a chown or mv mysteriously takes a very long time
# Whereas copying the files does not take very long.
# Therefore we set it up so that the mv just moves the symbolic link
RUN python3 -m venv /venv && mv /venv /venv2 && ln -s /venv2 /venv 
RUN . /venv/bin/activate && pip install pyyaml

## Theia
ARG version=latest
WORKDIR /home/theia
ADD $version.package.json ./package.json
ARG GITHUB_TOKEN
RUN yarn --cache-folder ./ycache && rm -rf ./ycache
RUN yarn theia build
EXPOSE 3000
ENV SHELL /bin/bash

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
