#!/bin/bash

git clone $1 /home/project
cd /home/project

#pip install -r requirements.txt

cd /home/theia
yarn theia start /home/project --hostname=0.0.0.0
