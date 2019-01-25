#!/bin/bash

set -e

git clone $1 /home/project
cd /home/project

if [ -f "/theiapod_init" ]; then
   /theiapod_init
fi

cd /home/theia
yarn theia start /home/project --hostname=0.0.0.0
