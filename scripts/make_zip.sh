#!/bin/bash

docker run --platform linux/amd64 --rm \
  -v "$(pwd)":/var/task \
  --entrypoint "" public.ecr.aws/lambda/python:3.12 \
  /bin/sh -c "
    pip install -r requirements.txt -t build/ --upgrade && \
    cp src/*.py build/ && \
    cd build && \
    dnf install -y zip && \
    zip -r ../test-package.zip . && \
    cd .. && \
    rm -rf build/
  "