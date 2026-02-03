#!/bin/bash

# 모든 플랫폼(특히 Apple Silicon 기반 Mac)에서 x64용 바이너리를 빌드하기 위해 docker 사용
docker run --platform linux/amd64 --rm \
  -v "$(pwd)":/var/task \
  --entrypoint "" public.ecr.aws/lambda/python:3.12 \
  /bin/sh -c "
    pip install -r requirements.txt -t build/ --upgrade && \
    cp src/*.py build/ && \
    cd build && \
    dnf install -y zip && \
    zip -r ../deploy-package.zip . && \
    cd .. && \
    rm -rf build/
  "
